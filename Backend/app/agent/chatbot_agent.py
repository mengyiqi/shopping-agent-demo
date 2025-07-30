import uuid
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
import os

from app.config import settings
from app.models import ProductSearchRequest
from IPython.display import Image

class AgentState(MessagesState):
    context: Dict[str, Any]
    image_path: Optional[str]
    response: Optional[str]
    intent: Optional[str]

class ChatbotAgent:
    """LangGraph-based chatbot agent with memory and thread capabilities"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            #max_output_tokens=settings.MAX_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY,
            #safety_settings=settings.SAFETY_SETTINGS
        )
        
        from app.services.service_manager import get_product_service
        # Initialize product service for RAG
        self.product_service = get_product_service()
        
        # Initialize memory saver for thread persistence
        self.memory_saver = MemorySaver()
        
        # Create the agent graph
        self.graph = self._create_agent_graph()
        
        # Compile the graph
        self.app = self.graph.compile(checkpointer=self.memory_saver)

        #self._save_graph_architecture()

        self.web_search_tool = TavilySearchResults(k=1, tavily_api_key=settings.TAVILY_API_KEY)
    
    def _create_agent_graph(self) -> StateGraph:
        """Create the LangGraph state graph for the chatbot"""                   
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("find_user_intent", self._find_user_intent)
        workflow.add_node("search_products", self._search_products)
        workflow.add_node("search_web", self._search_web)
        
        # Define edges
        workflow.set_entry_point("find_user_intent")
        workflow.add_conditional_edges(
            "find_user_intent",
            self._route_intent,
            {  
                "search_web": "search_web",
                "search_products": "search_products"
            }
        )
        workflow.add_edge("search_products", END)
        workflow.add_edge("search_web", END)
        
        return workflow
    
    def _save_graph_architecture(self):
        # Generate image from LangGraph
        img_data = Image(self.app.get_graph().draw_mermaid_png())

        # Create folder if it doesn't exist
        output_dir = "./graph_architecture"
        os.makedirs(output_dir, exist_ok=True)

        # Save image to file
        output_path = os.path.join(output_dir, "langgraph.png")
        with open(output_path, "wb") as f:
            f.write(img_data.data)

        print(f"LangGraph architecture saved to: {output_path}")
    
    def _find_user_intent(self, state: AgentState) -> AgentState:
        messages = state.get("messages", [])

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
                    You are a helpful and intelligent AI agent for an e-commerce platform. Your primary role is to assist users by routing their queries appropriately.

                    Product Catalog:
                    The store only sells products in the following categories:
                        •	Electronics

                    Instructions:
                        1.	If the user’s question indicates a product search within Electronics, route the query to the product search search.
                        2.	If the user’s question is not related to product search, or if it involves categories outside Electronics, route the query to the web search system to provide helpful information externally.

                    Always respond politely and professionally, and ensure the user receives a relevant and helpful answer, whether through internal search or web search.
                    """
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        chain = prompt | self.llm.with_structured_output(UserQueryIntent)

        intent = chain.invoke(
            {"messages": messages}
        )

        return {"intent": intent.step}

    def _route_intent(self, state: AgentState):
        # Return the node name you want to visit next
        if state["intent"] == "search_products":
            return "search_products"
        else:
            return "search_web"

    def _search_web(self, state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        user_query = ""
        if messages:
            user_query = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])

        # Web search
        docs = self.web_search_tool.invoke({"query": user_query})
        web_results = "\n".join([d["content"] for d in docs])

        system_prompt = self._create_system_prompt_for_web_search(user_query, web_results)

           # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        # Generate response
        chain = prompt | self.llm

        config = {"configurable": {"thread_id": state.get("thread_id")}}
        response = chain.invoke({"messages": messages},config=config)
        
        return {
            **state,
            "response": response.content,
            "messages": [AIMessage(content=response.content)]   
        }            
        
    async def _search_products(self, state: AgentState) -> AgentState:
        """Generate response using the LLM with RAG capabilities"""
        messages = state.get("messages", [])
        context = state.get("context", {})
        
        # Get the latest user message
        user_query = ""
        if messages:
            user_query = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        
        # Get relevant product context for RAG
        product_context = ""
        
        product_search_request = ProductSearchRequest(
            query=user_query,
            image_query_path=state.get("image_path", None),
            limit=3
        )
        result = await self.product_service.search_products(product_search_request)
        if(result.products):
            print(f"Found #{len(result.products)} product for system prompt")

            product_context = "Here is a list of product(s) found:"
            product_context += "\n".join([f"""
                Product: {product.title}
                Description: {product.description}
                Price: ${product.price}
                Category: {product.category}
                Tags: {product.tags}---""" for product in result.products])
   
        
        # Create system prompt with context and RAG
        system_prompt = self._create_system_prompt_for_product_recormendation(context, product_context) if result.products else self._create_system_prompt_for_query_clarification(context, user_query)
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        # Generate response
        chain = prompt | self.llm

        config = {"configurable": {"thread_id": state.get("thread_id")}}
        response = chain.invoke({"messages": messages}, config=config)
        
        return {
            **state,
            "response": response.content,
            "messages": [AIMessage(content=response.content)]   
        }

    def _create_system_prompt_for_web_search(self, user_query: str, web_results: str) -> str:

        web_results = web_results.replace('{', '{{').replace('}', '}}')

        """Create system prompt for web search"""
        base_prompt = f"""
        
        You are a helpful and professional AI assistant for an e-commerce platform. The user asked {user_query}, but it cannot be answered because:
            1.	The query does not express an intent to browse or purchase products, or
            2.	The product category is not offered by the store,

        However, you performed a web search and provided helpful information for the user.

        Web results: {web_results}

        Now summarize the web results in a way that is helpful and informative for the user.

        Your tone should be respectful, concise, and service-oriented. Make it clear that your primary goal is to support the user, even when the request falls outside the store’s scope.

        Example Behavior:
            •	If the user asks, “How do I cook quinoa?” and the store only sells electronics, say:
        “I’m here to help with products we offer, but cooking tips aren’t part of our catalog. That said, I found this helpful guide online for you…”
            •	If the user asks about a product type the store doesn’t sell (e.g., “Do you sell bicycles?” on a skincare store), say:
        “Thanks for your question! Unfortunately, we don’t carry bicycles in our current catalog. However, here’s what I found online that might help…”

        Always aim to be courteous, informative, and helpful — even when redirecting the user.
        """

        return base_prompt.format(user_query=user_query, web_results=web_results)


    def _create_system_prompt_for_query_clarification(self, context: Dict[str, Any], user_query: str) -> str:
        """Create system prompt for product search"""
        base_prompt = f"""
        The user’s original query is:: {user_query}
        
        You are an AI assistant for an e-commerce platform. Your role is to help users find the products they are looking for, even when an exact match is not available in the catalog.

        Your job is to help users find the right products—even when their original search yields no relevant results. Follow these steps:
            1.	Acknowledge the difficulty in finding an exact match politely.
            2.	Ask a smart, helpful clarifying question to better understand the user’s intent. Focus on common disambiguation areas such as:
            •	Product category
            •	Price range
            •	Intended use
            •	Alternative or similar product types
            3.	Avoid generic or robotic phrasing. Be conversational and helpful.
            4.	If possible, offer suggestions for how the user could rephrase or broaden their search.

        Be polite, natural, and user-centric in your language—like a helpful store assistant who wants to get it right.

        Examples:
            •	“Nothing popped up right away—could you tell me if you had a specific brand or feature in mind?”
            •	“That didn’t turn up anything yet. Are you open to similar styles or just looking for something specific?”

                """
        return base_prompt.format(user_query=user_query)
    
    def _create_system_prompt_for_product_recormendation(self, context: Dict[str, Any], product_context: str = "") -> str:
        """Create system prompt with context and RAG"""
        base_prompt = f"""You are a helpful AI assistant for an e-commerce platform. You should:
        1. Be conversational and friendly
        2. Provide accurate and helpful information about products
        3. Remember the conversation context
        4. Be concise but thorough in your responses

        """
        
        base_prompt += f"""Given the relevant product(s) information below, you should list and explain the product(s) to the user:
        {product_context}
        """
        
        return base_prompt.format(context=context, product_context=product_context)
    
    async def chat(
        self, 
        message: str, 
        query_image_path: Optional[str] = None,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return response"""
        
        # Generate thread_id if not provided
        if not thread_id:
            thread_id = str(uuid.uuid4())

        if(message is None):
            message = ""
        
        # Get existing messages from memory or start fresh
        config = {"configurable": {"thread_id": thread_id}}
                # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=message)],    
            "image_path": query_image_path,     
            "context": context or {},
            "response": None
        }
        
        # Run the graph
        result = await self.app.ainvoke(initial_state, config=config)

        return {
            "response": result["response"],
            "thread_id": thread_id,
            "metadata": {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "context": context
            }
        }
    
    async def get_thread_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a thread"""
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Get the current state from memory
            state = await self.app.aget_state(config)
            if state and state.values:
                messages = state.values.get("messages", [])
                return [
                    {
                        "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                        "content": msg.content,
                        "timestamp": datetime.now().isoformat()
                    }
                    for msg in messages
                ]
        except Exception:
            pass
        
        return []
    
    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a conversation thread"""
        try:
            config = {"configurable": {"thread_id": thread_id}}
            await self.app.adelete_state(config)
            return True
        except Exception:
            return False 



class UserQueryIntent(BaseModel):
    step: Literal["search_web", "search_products"] = Field(
        None, description="The next step in the routing user query"
    )

#!/usr/bin/env python3
"""
Test script for the LangGraph Chatbot API
Run this script to test the API endpoints
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any


class ChatbotAPITester:
    """Test client for the Chatbot API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> Dict[str, Any]:
        """Test health endpoint"""
        async with self.session.get(f"{self.base_url}/api/v1/health") as response:
            return await response.json()
    
    async def send_message(self, message: str, thread_id: str = None, user_id: str = None) -> Dict[str, Any]:
        """Send a message to the chatbot"""
        payload = {
            "message": message,
            "user_id": user_id
        }
        if thread_id:
            payload["thread_id"] = thread_id
        
        async with self.session.post(
            f"{self.base_url}/api/v1/chat",
            json=payload
        ) as response:
            return await response.json()
    
    async def get_thread_history(self, thread_id: str) -> Dict[str, Any]:
        """Get conversation history for a thread"""
        async with self.session.get(f"{self.base_url}/api/v1/threads/{thread_id}/history") as response:
            return await response.json()
    
    async def list_threads(self, user_id: str = None) -> Dict[str, Any]:
        """List all threads"""
        url = f"{self.base_url}/api/v1/threads"
        if user_id:
            url += f"?user_id={user_id}"
        
        async with self.session.get(url) as response:
            return await response.json()


async def main():
    """Main test function"""
    print("🤖 Testing LangGraph Chatbot API")
    print("=" * 50)
    
    async with ChatbotAPITester() as tester:
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        try:
            health = await tester.health_check()
            print(f"✅ Health Check: {health}")
        except Exception as e:
            print(f"❌ Health Check Failed: {e}")
            return
        
        # Test 2: Send First Message
        print("\n2. Testing First Message...")
        try:
            response1 = await tester.send_message(
                "Hello! My name is Alice. How are you today?",
                user_id="alice"
            )
            print(f"✅ First Message Response: {json.dumps(response1, indent=2)}")
            thread_id = response1["thread_id"]
        except Exception as e:
            print(f"❌ First Message Failed: {e}")
            return
        
        # Test 3: Continue Conversation
        print("\n3. Testing Conversation Continuity...")
        try:
            response2 = await tester.send_message(
                "What did I just tell you my name was?",
                thread_id=thread_id,
                user_id="alice"
            )
            print(f"✅ Continuation Response: {json.dumps(response2, indent=2)}")
        except Exception as e:
            print(f"❌ Continuation Failed: {e}")
        
        # Test 4: Get Thread History
        print("\n4. Testing Thread History...")
        try:
            history = await tester.get_thread_history(thread_id)
            print(f"✅ Thread History: {json.dumps(history, indent=2)}")
        except Exception as e:
            print(f"❌ Thread History Failed: {e}")
        
        # Test 5: List Threads
        print("\n5. Testing List Threads...")
        try:
            threads = await tester.list_threads(user_id="alice")
            print(f"✅ Threads List: {json.dumps(threads, indent=2)}")
        except Exception as e:
            print(f"❌ List Threads Failed: {e}")
        
        # Test 6: New Thread
        print("\n6. Testing New Thread...")
        try:
            response3 = await tester.send_message(
                "This is a new conversation thread.",
                user_id="bob"
            )
            print(f"✅ New Thread Response: {json.dumps(response3, indent=2)}")
        except Exception as e:
            print(f"❌ New Thread Failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")


if __name__ == "__main__":
    # Run the async test
    asyncio.run(main()) 
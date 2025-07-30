import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState(uuidv4());
  const [userId] = useState(uuidv4()); // Static user ID for the session
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startNewChat = () => {
    setMessages([]);
    setThreadId(uuidv4());
    setInputMessage('');
    setSelectedImage(null);
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    // Reset the file input
    const fileInput = document.getElementById('image-input');
    if (fileInput) {
      fileInput.value = '';
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() && !selectedImage) {
      return;
    }

    const userMessage = {
      id: uuidv4(),
      type: 'user',
      text: inputMessage,
      image: selectedImage ? URL.createObjectURL(selectedImage) : null,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('message', inputMessage);
      formData.append('thread_id', threadId);
      formData.append('user_id', userId);
      
      if (selectedImage) {
        formData.append('query_image', selectedImage);
      }

      const response = await fetch('http://127.0.0.1:8888/api/v1/chat', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Process escaped characters and markup in the response
      const processedResponse = (data.response || 'Thank you for your message. I\'m here to help you find the perfect products!')
        // Handle escaped newlines
        .replace(/\\n/g, '\n')  // Convert \n to actual newlines
        .replace(/\\r\\n/g, '\n')  // Convert \r\n to newlines
        .replace(/\\r/g, '\n')  // Convert \r to newlines
        // Handle other escaped characters
        .replace(/\\t/g, '\t')  // Convert \t to tabs
        .replace(/\\"/g, '"')   // Convert \" to quotes
        .replace(/\\'/g, "'")   // Convert \' to apostrophes
        // Handle HTML entities
        .replace(/&lt;/g, '<')  // Convert &lt; to <
        .replace(/&gt;/g, '>')  // Convert &gt; to >
        .replace(/&amp;/g, '&') // Convert &amp; to &
        .replace(/&quot;/g, '"') // Convert &quot; to "
        .replace(/&#39;/g, "'")  // Convert &#39; to '
        .replace(/&nbsp;/g, ' ') // Convert &nbsp; to space
        // Handle common HTML tags (convert to plain text)
        .replace(/<br\s*\/?>/gi, '\n')  // Convert <br> tags to newlines
        .replace(/<p[^>]*>/gi, '\n')    // Convert <p> tags to newlines
        .replace(/<\/p>/gi, '\n')       // Convert </p> tags to newlines
        .replace(/<div[^>]*>/gi, '\n')  // Convert <div> tags to newlines
        .replace(/<\/div>/gi, '\n')     // Convert </div> tags to newlines
        // Remove other HTML tags
        .replace(/<[^>]*>/g, '')
        // Clean up multiple consecutive newlines
        .replace(/\n\s*\n\s*\n/g, '\n\n')
        // Process markdown formatting
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold: **text** -> <strong>text</strong>
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic: *text* -> <em>text</em>
        .replace(/__(.*?)__/g, '<strong>$1</strong>')      // Bold: __text__ -> <strong>text</strong>
        .replace(/_(.*?)_/g, '<em>$1</em>')                // Italic: _text_ -> <em>text</em>
        .replace(/~~(.*?)~~/g, '<del>$1</del>')            // Strikethrough: ~~text~~ -> <del>text</del>
        .replace(/`(.*?)`/g, '<code>$1</code>')            // Inline code: `text` -> <code>text</code>
        // Trim whitespace
        .trim();
      
      const aiMessage = {
        id: uuidv4(),
        type: 'ai',
        text: processedResponse,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: uuidv4(),
        type: 'ai',
        text: 'Sorry, I encountered an error. Please try again later.',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputMessage('');
      setSelectedImage(null);
      // Reset the file input
      const fileInput = document.getElementById('image-input');
      if (fileInput) {
        fileInput.value = '';
      }
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <div className="chatbot-container">
        <div className="chatbot-header">
          <h1>🛍️ Product Shopping Agent</h1>
          <button className="new-chat-btn" onClick={startNewChat}>
            Start New Chat
          </button>
        </div>

        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Welcome to Product Search! 🎉</h2>
              <p>Ask me anything about products, upload images, or describe what you're looking for.</p>
              <p>I'm here to help you discover amazing products!</p>
            </div>
          )}
          
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type} ${message.isError ? 'error' : ''}`}>
              <div className="message-content">
                <div className="message-header">
                  <span className="message-sender">
                    {message.type === 'user' ? 'You' : 'AI Assistant'}
                  </span>
                  <span className="message-time">{message.timestamp}</span>
                </div>
                
                {message.image && (
                  <div className="message-image">
                    <img src={message.image} alt="User uploaded" />
                  </div>
                )}
                
                <div 
                  className="message-text"
                  dangerouslySetInnerHTML={{ __html: message.text }}
                />
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message ai">
              <div className="message-content">
                <div className="message-header">
                  <span className="message-sender">AI Assistant</span>
                  <span className="message-time">{new Date().toLocaleTimeString()}</span>
                </div>
                <div className="message-text">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <div className="input-wrapper">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Press Enter to send)"
              className="message-input"
              rows="1"
            />
            
            <div className="input-actions">
              <label htmlFor="image-input" className="image-upload-btn">
                📷
                <input
                  id="image-input"
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  style={{ display: 'none' }}
                />
              </label>
              
              <button
                onClick={sendMessage}
                disabled={isLoading || (!inputMessage.trim() && !selectedImage)}
                className="send-btn"
              >
                {isLoading ? '⏳' : '➤'}
              </button>
            </div>
          </div>
          
          {selectedImage && (
            <div className="selected-image">
              <img src={URL.createObjectURL(selectedImage)} alt="Selected" />
              <button onClick={removeImage} className="remove-image-btn">
                ✕
              </button>
              <span className="image-name">{selectedImage.name}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 
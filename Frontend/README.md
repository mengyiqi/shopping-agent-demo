# Product Search Chatbot

A modern, responsive ReactJS chatbot UI for product search with image upload capabilities and real-time chat functionality.

## 🚀 Features

### Chat Capabilities
- **Real-time Chat Interface**: Back-and-forth messaging between user and AI
- **Image Upload Support**: Upload images alongside text messages
- **Thread Management**: Each chat session has a unique UUID thread ID
- **Message History**: Maintains chronological chat history per session
- **New Chat Sessions**: Start fresh conversations with new thread IDs

### User Interface
- **Modern Design**: Clean, gradient-based UI with smooth animations
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Loading States**: Visual feedback during API calls with typing indicators
- **Error Handling**: Graceful error messages for failed requests
- **Auto-scroll**: Automatically scrolls to latest messages

### Technical Features
- **FormData API Integration**: Proper multipart/form-data handling for images
- **UUID Generation**: Automatic thread and user ID generation
- **Keyboard Shortcuts**: Enter to send messages, Shift+Enter for new lines
- **File Validation**: Image file type validation and preview

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## 📡 Backend API Integration

The chatbot is configured to work with the following API endpoint:

- **Base URL**: `http://127.0.0.1:8888/`
- **Chat Endpoint**: `POST http://127.0.0.1:8888/api/v1/chat`
- **Content Type**: `multipart/form-data`

### API Parameters
- `message` (string): User message text
- `thread_id` (string): UUID for chat session
- `user_id` (string): Static user identifier
- `query_image` (file, optional): Uploaded image file

### Expected Response Format
```json
{
  "response": "AI response message here"
}
```

## 🎯 Usage

### Starting a Chat
1. The app automatically generates a new chat session on load
2. Type your message in the input field
3. Optionally upload an image using the camera icon
4. Press Enter or click the send button

### Image Upload
1. Click the 📷 camera icon
2. Select an image file from your device
3. The image will be previewed below the input
4. Click the ✕ button to remove the image
5. Send your message with or without text

### New Chat Session
- Click "Start New Chat" to begin a fresh conversation
- This clears the current chat history and generates a new thread ID

## 🎨 Customization

### Styling
The app uses CSS custom properties and modern design patterns. Key styling files:
- `src/App.css`: Main component styles
- `src/index.css`: Global styles and reset

### Configuration
Modify the API endpoint in `src/App.js`:
```javascript
const response = await fetch('http://127.0.0.1:8888/api/v1/chat', {
  method: 'POST',
  body: formData,
});
```

## 📱 Responsive Design

The chatbot is fully responsive and optimized for:
- **Desktop**: Full-featured interface with side-by-side layout
- **Tablet**: Adapted layout with optimized touch targets
- **Mobile**: Single-column layout with mobile-friendly interactions

## 🔧 Development

### Project Structure
```
src/
├── App.js          # Main chatbot component
├── App.css         # Component styles
├── index.js        # React entry point
└── index.css       # Global styles
```

### Key Dependencies
- **React 18.2.0**: Modern React with hooks
- **uuid 9.0.0**: UUID generation for thread management
- **react-scripts 5.0.1**: Development and build tools

### Available Scripts
- `npm start`: Start development server
- `npm build`: Build for production
- `npm test`: Run tests
- `npm eject`: Eject from Create React App

## 🚨 Error Handling

The app includes comprehensive error handling:
- **Network Errors**: Displays user-friendly error messages
- **File Validation**: Ensures only image files are uploaded
- **API Failures**: Graceful degradation with retry options
- **Loading States**: Prevents multiple simultaneous requests

## 🔒 Security Considerations

- No sensitive data is stored locally
- File uploads are validated for image types only
- API calls use proper error handling
- User IDs are generated per session

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chatbot functionality.

---

**Note**: This is a frontend-only implementation. You'll need to set up the backend API at `http://127.0.0.1:8888/api/v1/chat` to handle the chat requests and return appropriate responses. 
# LangGraph Chat UI

A modern web-based chat interface for your LangGraph agent with authentication.

## 🚀 Features

- **Web-based Interface**: Beautiful, responsive chat interface
- **Real-time Communication**: WebSocket-based real-time messaging
- **User Authentication**: Supabase-based login/signup system
- **Session Management**: Persistent chat sessions
- **Modern UI**: Clean, modern design with emojis and smooth animations
- **Mobile Responsive**: Works on desktop and mobile devices

## 📋 Prerequisites

1. **LangGraph Server**: Your LangGraph server must be running on `http://localhost:2024`
2. **Supabase Setup**: You need a Supabase project with authentication enabled
3. **Environment Variables**: Create a `.env` file with your Supabase credentials

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the same directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SECRET_KEY=your_flask_secret_key
   ```

3. **Start the Chat UI**:
   ```bash
   python run_chat_ui.py
   ```

## 🎯 Usage

1. **Start the Application**:
   ```bash
   python run_chat_ui.py
   ```

2. **Open Your Browser**:
   Navigate to `http://localhost:5001`

3. **Authentication**:
   - Sign up with your email and password
   - Or login if you already have an account
   - Check your email to confirm your account (for new signups)

4. **Start Chatting**:
   - Type your messages in the chat input
   - Press Enter or click Send
   - View real-time AI responses

## 📁 File Structure

```
chatbot_auth/
├── app.py              # Original CLI chat application
├── chat_ui.py          # New web-based chat UI
├── run_chat_ui.py      # Startup script for chat UI
├── requirements.txt    # Python dependencies
├── README_CHAT_UI.md   # This file
├── .env               # Environment variables (create this)
└── templates/         # HTML templates (auto-generated)
    ├── index.html     # Login/signup page
    └── chat.html      # Chat interface page
```

## 🔧 Configuration

### Environment Variables

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anonymous key
- `SECRET_KEY`: Flask session secret key (optional, defaults to 'your-secret-key-here')

### LangGraph Server

The chat UI expects your LangGraph server to be running on `http://localhost:2024` with:
- An assistant named "agent"
- Authentication enabled
- The same authentication token system as your original app.py

## 🎨 UI Features

### Login/Signup Page
- Clean, modern design with gradient background
- Toggle between login and signup forms
- Real-time form validation
- Success/error message display

### Chat Interface
- Real-time messaging with WebSocket
- Message timestamps
- User and AI message differentiation
- Typing indicators
- Connection status display
- Auto-scrolling to latest messages
- Responsive design for mobile devices

### Message Features
- Support for Enter to send (Shift+Enter for new line)
- Auto-resizing text input
- Message length limits
- Error handling and display

## 🔒 Security

- Session-based authentication
- CSRF protection
- Secure WebSocket connections
- Environment variable configuration
- Input validation and sanitization

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**:
   - Make sure your LangGraph server is running on `http://localhost:2024`
   - Check that authentication is properly configured

2. **Authentication Error**:
   - Verify your Supabase credentials in the `.env` file
   - Ensure your Supabase project has authentication enabled

3. **Dependencies Error**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Port Already in Use**:
   - Change the port in `chat_ui.py` or stop other services using port 5001

### Debug Mode

The application runs in debug mode by default. You can see detailed error messages and logs in the terminal.

## 🔄 Integration with Original App

The chat UI is designed to work alongside your original `app.py`:

- **Same Authentication**: Uses the same Supabase authentication system
- **Same LangGraph Server**: Connects to the same LangGraph server
- **Same Assistant**: Uses the same "agent" assistant
- **Independent Operation**: Can run simultaneously with the CLI version

## 🚀 Deployment

For production deployment:

1. **Set Production Environment**:
   ```python
   # In chat_ui.py, change debug=True to debug=False
   socketio.run(app, host='0.0.0.0', port=5000, debug=False)
   ```

2. **Use a Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 chat_ui:app
   ```

3. **Set Secure Environment Variables**:
   - Use strong SECRET_KEY
   - Ensure HTTPS in production
   - Configure proper CORS settings

## 📱 Mobile Support

The chat interface is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Tablet browsers

## 🤝 Contributing

To extend the chat UI:

1. **Add New Features**: Modify `chat_ui.py` and the HTML templates
2. **Customize Styling**: Edit the CSS in the HTML templates
3. **Add New Routes**: Add new Flask routes for additional functionality
4. **Extend WebSocket Events**: Add new Socket.IO events for real-time features

## 📄 License

This chat UI is part of your LangGraph project and follows the same license terms. 
#!/usr/bin/env python3
"""
Simple script to run the LangGraph Chat UI
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chat_ui import app, socketio

if __name__ == "__main__":
    print("🚀 Starting LangGraph Chat UI...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("🔐 Make sure your LangGraph server is running on http://localhost:2024")
    print("🔑 Make sure your .env file has SUPABASE_URL and SUPABASE_ANON_KEY")
    print("-" * 60)
    
    try:
        socketio.run(app, host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Chat UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting Chat UI: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt") 
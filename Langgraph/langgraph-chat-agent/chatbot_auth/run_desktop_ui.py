#!/usr/bin/env python3
"""
Simple script to run the LangGraph Desktop Chat UI
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from desktop_ui import run_app

if __name__ == "__main__":
    print("🚀 Starting LangGraph Desktop Chat UI...")
    print("🖥️  A modern desktop chat interface will open")
    print("🔐 Make sure your LangGraph server is running on http://localhost:2024")
    print("🔑 Make sure your .env file has SUPABASE_URL and SUPABASE_ANON_KEY")
    print("-" * 60)
    
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n👋 Desktop UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting Desktop UI: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt") 
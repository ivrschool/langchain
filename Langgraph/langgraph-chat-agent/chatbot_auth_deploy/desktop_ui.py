# ui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
import asyncio
import threading
import httpx
import os
from dotenv import load_dotenv
from langgraph_sdk import get_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
API_URL = "http://localhost:2024"  # Your LangGraph dev server


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LangGraph Chatbot")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        self.token = None
        self.client = None
        self.thread_id = None

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

        self.build_login_ui()

    def build_login_ui(self):
        self.clear_window()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="📧 Email:", anchor="w").pack(fill="x", pady=(0, 5))
        self.email_entry = tk.Entry(frame, width=40)
        self.email_entry.pack(pady=(0, 10))

        tk.Label(frame, text="🔐 Password:", anchor="w").pack(fill="x", pady=(0, 5))
        self.password_entry = tk.Entry(frame, width=40, show="*")
        self.password_entry.pack(pady=(0, 15))

        button_frame = tk.Frame(frame)
        button_frame.pack()

        tk.Button(button_frame, text="Login", width=15, command=self.handle_login).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sign Up", width=15, command=self.handle_signup).pack(side=tk.LEFT, padx=5)

    def build_chat_ui(self):
        self.clear_window()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        chat_frame = tk.Frame(self.root)
        chat_frame.grid(row=0, column=0, sticky="nsew")

        self.chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD)
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_box.insert(tk.END, "🤖 Welcome to LangGraph Chatbot!\n\n")
        self.chat_box.config(state=tk.DISABLED)

        input_frame = tk.Frame(self.root)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = tk.Entry(input_frame)
        self.input_entry.grid(row=0, column=0, sticky="ew")
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        tk.Button(input_frame, text="Send", command=self.send_message).grid(row=0, column=1, padx=5)

        # Logout Button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 10))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    async def login_user(self, email, password):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
                json={"email": email, "password": password},
                headers={"apikey": SUPABASE_ANON_KEY},
            )
            if res.status_code != 200:
                raise Exception(res.json().get("error_description", "Login failed."))
            return res.json()["access_token"]

    async def signup_user(self, email, password):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{SUPABASE_URL}/auth/v1/signup",
                json={"email": email, "password": password},
                headers={"apikey": SUPABASE_ANON_KEY},
            )
            if res.status_code != 200:
                raise Exception(res.json().get("msg", "Signup failed."))

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        async def do_login():
            try:
                self.token = await self.login_user(email, password)
                self.client = get_client(url=API_URL, headers={"Authorization": f"Bearer {self.token}"})
                thread = await self.client.threads.create()
                self.thread_id = thread["thread_id"]
                self.root.after(0, self.build_chat_ui)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Login Failed", str(e)))

        asyncio.run_coroutine_threadsafe(do_login(), self.loop)

    def handle_signup(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        async def do_signup():
            try:
                await self.signup_user(email, password)
                self.root.after(0, lambda: messagebox.showinfo(
                    "Signup Success", "Check your email to confirm your account before logging in."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Signup Failed", str(e)))

        asyncio.run_coroutine_threadsafe(do_signup(), self.loop)

    def send_message(self):
        user_msg = self.input_entry.get().strip()
        if not user_msg:
            return

        self.append_chat("You", user_msg)
        self.input_entry.delete(0, tk.END)

        async def get_response():
            try:
                res = await self.client.runs.wait(
                    thread_id=self.thread_id,
                    assistant_id="agent",
                    input={"messages": [{"role": "user", "content": user_msg}]},
                    config={"configurable": {"recursion_limit": 50}},
                    checkpoint_during=True,
                )
                reply = res["messages"][-1]["content"]
                self.root.after(0, lambda: self.append_chat("Agent", reply))
            except Exception as e:
                self.root.after(0, lambda: self.append_chat("Error", f"❌ {str(e)}"))

        asyncio.run_coroutine_threadsafe(get_response(), self.loop)

    def append_chat(self, speaker, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{speaker}: {message}\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def logout(self):
        self.token = None
        self.client = None
        self.thread_id = None
        self.build_login_ui()


def run_app():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()

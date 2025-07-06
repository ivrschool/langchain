const SUPABASE_URL = "https://YOUR_PROJECT.supabase.co";
const SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY";
const LANGGRAPH_API = "http://localhost:2024";  // or your backend URL

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let token = null;
let thread_id = null;

// Handle Login
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    showMessage("auth-message", "❌ " + error.message);
    return;
  }

  token = data.session.access_token;
  console.log("✅ Logged in. Token:", token);

  await startChat();
}

// Handle Signup
async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const { error } = await supabase.auth.signUp({ email, password });

  if (error) {
    showMessage("auth-message", "❌ " + error.message);
  } else {
    showMessage("auth-message", "✅ Check your email to confirm your account.");
  }
}

// Start Chat Session
async function startChat() {
  try {
    document.getElementById("auth-box").style.display = "none";
    document.getElementById("chat-box").style.display = "block";

    const res = await fetch(`${LANGGRAPH_API}/threads`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
    });

    if (!res.ok) {
      const errorBody = await res.text();
      throw new Error(`Thread creation failed: ${res.status} ${errorBody}`);
    }

    const data = await res.json();
    thread_id = data.thread_id;
    console.log("✅ Created thread:", thread_id);
  } catch (err) {
    console.error("🚨 Error in startChat:", err);
    showMessage("auth-message", "❌ Failed to start chat: " + err.message);
    document.getElementById("auth-box").style.display = "block";
    document.getElementById("chat-box").style.display = "none";
  }
}

// Send a message to the bot
async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("you", message);
  input.value = "";

  try {
    const runRes = await fetch(`${LANGGRAPH_API}/runs/wait`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        thread_id: thread_id,
        assistant_id: "agent",
        input: {
          messages: [{ role: "user", content: message }]
        },
        config: {
          configurable: { recursion_limit: 50 }
        },
        checkpoint_during: true
      }),
    });

    if (!runRes.ok) {
      const errorBody = await runRes.text();
      throw new Error(`Run failed: ${runRes.status} ${errorBody}`);
    }

    const runData = await runRes.json();
    const reply = runData.messages.at(-1).content;
    appendMessage("agent", reply);
  } catch (err) {
    console.error("❌ Error sending message:", err);
    appendMessage("error", "❌ " + err.message);
  }
}

// Append message to chat UI
function appendMessage(role, text) {
  const history = document.getElementById("chat-history");
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = `${role === "you" ? "You" : role === "agent" ? "Agent" : "Error"}: ${text}`;
  history.appendChild(div);
  history.scrollTop = history.scrollHeight;
}

// Show message under auth form
function showMessage(id, message) {
  document.getElementById(id).textContent = message;
}

// Logout
function logout() {
  token = null;
  thread_id = null;
  document.getElementById("chat-history").innerHTML = "";
  document.getElementById("auth-box").style.display = "block";
  document.getElementById("chat-box").style.display = "none";
}

"""
Orphixa AI — Flask Web API
Run: python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, request, jsonify, render_template_string
from orphixa import OrphixaAI

app = Flask(__name__)
bot = OrphixaAI()

# ─────────────────────────────────────────────────────────
#  INLINE HTML TEMPLATE  (no separate template file needed)
# ─────────────────────────────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Orphixa AI</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #0f0f1a;
      color: #e0e0e0;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
    header {
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      padding: 16px 24px;
      border-bottom: 1px solid #2a2a4a;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    header h1 { font-size: 1.4rem; color: #7ee8fa; }
    header span { font-size: 0.8rem; color: #888; background: #2a2a4a;
                  padding: 3px 8px; border-radius: 12px; }
    #chat {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .msg { max-width: 72%; padding: 12px 16px; border-radius: 18px;
           line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap; }
    .user { background: #2563eb; color: #fff; align-self: flex-end;
            border-bottom-right-radius: 4px; }
    .bot  { background: #1e1e35; color: #d0d0f0; align-self: flex-start;
            border: 1px solid #2a2a4a; border-bottom-left-radius: 4px; }
    .sender { font-size: 0.72rem; margin-bottom: 4px; opacity: 0.6; }
    .bot .sender  { color: #7ee8fa; }
    .user .sender { color: #93c5fd; text-align: right; }
    footer {
      padding: 16px 24px;
      background: #12121f;
      border-top: 1px solid #2a2a4a;
      display: flex;
      gap: 10px;
    }
    #input {
      flex: 1;
      padding: 12px 16px;
      border-radius: 24px;
      border: 1px solid #3a3a5a;
      background: #1e1e35;
      color: #e0e0e0;
      font-size: 0.95rem;
      outline: none;
    }
    #input:focus { border-color: #7ee8fa; }
    button {
      padding: 12px 20px;
      border-radius: 24px;
      border: none;
      background: #2563eb;
      color: #fff;
      cursor: pointer;
      font-size: 0.95rem;
      transition: background 0.2s;
    }
    button:hover { background: #1d4ed8; }
    .typing { color: #7ee8fa; font-size: 0.85rem; opacity: 0.7; }
  </style>
</head>
<body>
  <header>
    <h1>🤖 Orphixa AI</h1>
    <span>Intelligent Chatbot v1.0</span>
  </header>

  <div id="chat">
    <div class="msg bot">
      <div class="sender">Orphixa</div>
      Hey there! I'm Orphixa, your AI assistant. How can I help you today?
    </div>
  </div>

  <footer>
    <input id="input" type="text" placeholder="Type a message..." autocomplete="off" />
    <button onclick="sendMessage()">Send ➤</button>
  </footer>

  <script>
    const chat  = document.getElementById('chat');
    const input = document.getElementById('input');

    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });

    function addMsg(text, role) {
      const wrap = document.createElement('div');
      wrap.className = 'msg ' + role;
      const sender = document.createElement('div');
      sender.className = 'sender';
      sender.textContent = role === 'user' ? 'You' : 'Orphixa';
      wrap.appendChild(sender);
      wrap.appendChild(document.createTextNode(text));
      chat.appendChild(wrap);
      chat.scrollTop = chat.scrollHeight;
    }

    async function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      addMsg(text, 'user');
      input.value = '';

      try {
        const res  = await fetch('/chat', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify({ message: text }),
        });
        const data = await res.json();
        addMsg(data.response, 'bot');
      } catch {
        addMsg('⚠️ Could not reach Orphixa. Please check the server.', 'bot');
      }
    }
  </script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    response = bot.respond(user_message)
    return jsonify({"response": response, "intent": "detected"})


@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": list(bot.memory.history)})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "bot": "Orphixa AI", "version": "1.0.0"})


# ─────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  🤖  Orphixa AI Web Server starting...")
    print("  📡  Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=True, port=5000)

# web_chat.py - Web-based AI Chat with Cost Tracking
# 
# Web interface for AI chat with real-time cost monitoring
# Requires: https://github.com/robertprast/goop
# Dependencies: pip install openai
# Setup: Follow goop setup instructions, then run this script

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from openai import OpenAI

# Configure for your goop proxy setup
# Default goop proxy runs on localhost:8080
client = OpenAI(base_url="http://localhost:8080/openai-proxy/v1", api_key="your-api-key")

# Vertex AI Pricing (as of January 2025) - verify current rates at cloud.google.com
# Update these rates based on your region and current Google Cloud pricing
MODEL_PRICING = {
    "vertex/gemini-2.0-flash-lite-001": {
        "input_per_1k": 0.000075,
        "output_per_1k": 0.0003,
        "name": "Gemini 2.0 Flash Lite",
        "description": "Fastest (0.51s)",
        "speed": "fastest"
    },
    "vertex/gemini-2.5-flash-preview-05-20": {
        "input_per_1k": 0.00015,
        "output_per_1k": 0.0006,
        "name": "Gemini 2.5 Flash Preview",
        "description": "Newest (0.68s)",
        "speed": "fast"
    },
    "vertex/gemini-2.0-flash-001": {
        "input_per_1k": 0.00015,
        "output_per_1k": 0.0006,
        "name": "Gemini 2.0 Flash",
        "description": "Reliable (0.83s)",
        "speed": "medium"
    },
    "vertex/gemini-2.5-pro-preview-05-06": {
        "input_per_1k": 0.0003,
        "output_per_1k": 0.0012,
        "name": "Gemini 2.5 Pro Preview",
        "description": "Most Capable (1.26s)",
        "speed": "slower"
    }
}

# Session tracking
session_cost = 0.0
message_count = 0

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate cost for a single request"""
    if model not in MODEL_PRICING:
        model = "vertex/gemini-2.0-flash-001"  # Fallback
    
    pricing = MODEL_PRICING[model]
    input_cost = (prompt_tokens / 1000) * pricing["input_per_1k"]
    output_cost = (completion_tokens / 1000) * pricing["output_per_1k"]
    return input_cost + output_cost

# AI Chat Web Interface with embedded CSS
HTML_PAGE = '''<!DOCTYPE html>
<html>
<head>
    <title>AI Neural Interface</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'VT323', 'Courier New', monospace;
            background: #000000;
            color: #00ff41;
            height: 100vh;
            overflow: hidden;
            text-shadow: 0 0 3px #00ff41;
            font-size: 18px;
            line-height: 1.6;
        }
        
        .container {
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: #000000;
            position: relative;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent 0px,
                    rgba(0, 255, 65, 0.03) 1px,
                    transparent 2px,
                    transparent 4px
                );
            pointer-events: none;
            z-index: 1;
        }
        
        .header {
            padding: 20px;
            background: #000000;
            border-bottom: 2px solid #00ff41;
            position: relative;
            z-index: 2;
        }
        
        .header h1 {
            font-size: 36px;
            font-weight: 400;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 15px;
            text-shadow: 0 0 8px #00ff41;
            animation: flicker 4s infinite;
        }
        
        @keyframes flicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
            51% { opacity: 1; }
            52% { opacity: 0.8; }
            53% { opacity: 1; }
        }
        
        .status-line {
            font-size: 16px;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
            opacity: 0.9;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            padding: 15px;
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid #00ff41;
        }
        
        .metric {
            text-align: center;
            padding: 10px 5px;
            border: 1px solid transparent;
            transition: all 0.3s ease;
        }
        
        .metric:hover {
            border-color: #00ff41;
            background: rgba(0, 255, 65, 0.1);
        }
        
        .metric-label {
            font-size: 14px;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            opacity: 0.8;
        }
        
        .metric-value {
            font-size: 20px;
            font-weight: 400;
            color: #00ff41;
            font-family: 'VT323', monospace;
            text-shadow: 0 0 6px #00ff41;
        }
        
        .model-panel {
            padding: 15px 20px;
            background: #000000;
            border-bottom: 1px solid #00ff41;
        }
        
        .model-label {
            font-size: 16px;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }
        
        .model-select {
            width: 100%;
            padding: 15px 20px;
            background: #000000;
            border: 2px solid #00ff41;
            color: #00ff41;
            font-family: 'VT323', monospace;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-shadow: 0 0 3px #00ff41;
        }
        
        .model-select:focus {
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
            background: rgba(0, 255, 65, 0.05);
        }
        
        .model-select option {
            background: #000000;
            color: #00ff41;
            padding: 10px;
        }
        
        .terminal {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #000000;
            position: relative;
            z-index: 2;
        }
        
        .terminal::-webkit-scrollbar { width: 8px; }
        .terminal::-webkit-scrollbar-track { background: #000000; }
        .terminal::-webkit-scrollbar-thumb { 
            background: #00ff41; 
            border: 1px solid #00ff41;
        }
        .terminal::-webkit-scrollbar-thumb:hover { 
            background: rgba(0, 255, 65, 0.8);
        }
        
        .msg {
            margin: 20px 0;
            font-family: 'VT323', monospace;
            font-size: 18px;
            line-height: 1.6;
            opacity: 0;
            animation: typeIn 0.5s ease forwards;
        }
        
        @keyframes typeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .msg.user-msg {
            color: #ffff00;
            text-shadow: 0 0 4px #ffff00;
            margin-left: 40px;
        }
        
        .msg.ai-msg {
            color: #00ff41;
            text-shadow: 0 0 4px #00ff41;
        }
        
        .msg.error-msg {
            color: #ff0000;
            text-shadow: 0 0 4px #ff0000;
            animation: errorFlash 0.5s ease;
        }
        
        @keyframes errorFlash {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .msg-header {
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
            display: block;
            opacity: 0.9;
        }
        
        .msg-content {
            margin-left: 25px;
            white-space: pre-wrap;
        }
        
        .timestamp {
            font-size: 14px;
            opacity: 0.7;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .input-panel {
            padding: 20px;
            background: #000000;
            border-top: 2px solid #00ff41;
            display: flex;
            gap: 15px;
            align-items: center;
            position: relative;
            z-index: 2;
        }
        
        .prompt {
            color: #00ff41;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 0 0 8px #00ff41;
        }
        
        .neural-input {
            flex: 1;
            padding: 15px 20px;
            background: transparent;
            border: 2px solid #00ff41;
            color: #00ff41;
            font-size: 16px;
            font-family: 'VT323', monospace;
            transition: all 0.3s ease;
            text-shadow: 0 0 5px #00ff41;
        }
        
        .neural-input:focus {
            outline: none;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
            background: rgba(0, 255, 65, 0.05);
        }
        
        .neural-input::placeholder {
            color: rgba(0, 255, 65, 0.5);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .execute-btn {
            padding: 15px 25px;
            background: transparent;
            color: #00ff41;
            border: 2px solid #00ff41;
            cursor: pointer;
            font-family: 'VT323', monospace;
            font-size: 16px;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            text-shadow: 0 0 5px #00ff41;
        }
        
        .execute-btn:hover {
            background: rgba(0, 255, 65, 0.1);
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        }
        
        .execute-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }
        
        .cursor {
            display: inline-block;
            background: #00ff41;
            width: 2px;
            height: 1em;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .warning { 
            color: #ffff00 !important; 
            text-shadow: 0 0 8px #ffff00 !important; 
        }
        
        .danger { 
            color: #ff0000 !important; 
            text-shadow: 0 0 8px #ff0000 !important; 
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .header { padding: 15px; }
            .header h1 { font-size: 24px; letter-spacing: 2px; }
            .metrics { 
                grid-template-columns: repeat(2, 1fr); 
                gap: 10px; 
                padding: 10px; 
            }
            .terminal { padding: 15px; }
            .msg { font-size: 14px; margin: 10px 0; }
            .input-panel { 
                padding: 15px; 
                gap: 10px;
                flex-direction: column;
            }
            .neural-input, .execute-btn { 
                font-size: 14px; 
                padding: 12px 15px; 
            }
            .execute-btn { 
                width: 100%;
                margin-top: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        
        <div class="header">
            <h1>AI Neural Interface</h1>
            <div class="status-line">ARTIFICIAL INTELLIGENCE SYSTEM :: ONLINE</div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">LAST QUERY COST</div>
                    <div class="metric-value" id="last-cost">$0.000000</div>
                </div>
                <div class="metric">
                    <div class="metric-label">SESSION COST</div>
                    <div class="metric-value" id="session-cost">$0.000000</div>
                </div>
                <div class="metric">
                    <div class="metric-label">TOTAL QUERIES</div>
                    <div class="metric-value" id="message-count">0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">AVERAGE COST</div>
                    <div class="metric-value" id="avg-cost">$0.000000</div>
                </div>
            </div>
        </div>
        
        <div class="model-panel">
            <div class="model-label">NEURAL MODEL SELECTION</div>
            <select class="model-select" id="model-select">
                <option value="vertex/gemini-2.0-flash-lite-001">GEMINI 2.0 FLASH LITE :: RESPONSE TIME: 0.51s</option>
                <option value="vertex/gemini-2.5-flash-preview-05-20">GEMINI 2.5 FLASH PREVIEW :: RESPONSE TIME: 0.68s</option>
                <option value="vertex/gemini-2.0-flash-001">GEMINI 2.0 FLASH :: RESPONSE TIME: 0.83s</option>
                <option value="vertex/gemini-2.5-pro-preview-05-06">GEMINI 2.5 PRO PREVIEW :: RESPONSE TIME: 1.26s</option>
            </select>
        </div>
        
        <div class="terminal" id="terminal">
            <div class="msg ai-msg">
                <div class="msg-header">SYSTEM :: INITIALIZATION</div>
                <div class="msg-content">ARTIFICIAL INTELLIGENCE SYSTEM ONLINE
VERTEX AI NEURAL NETWORKS ACTIVE
AWAITING USER INPUT<span class="cursor"></span></div>
                <div class="timestamp">READY</div>
            </div>
        </div>
        
        <div class="input-panel">
            <span class="prompt">></span>
            <input type="text" class="neural-input" id="neural-input" 
                   placeholder="ENTER QUERY..." 
                   onkeypress="if(event.key==='Enter') executeQuery()">
            <button class="execute-btn" id="execute-btn" onclick="executeQuery()">EXECUTE</button>
        </div>
    </div>

    <script>
        let queryCount = 0;
        let sessionCost = 0;

        async function executeQuery() {
            const input = document.getElementById('neural-input');
            const executeBtn = document.getElementById('execute-btn');
            const modelSelect = document.getElementById('model-select');
            
            const query = input.value.trim();
            if (!query) return;
            
            input.disabled = true;
            executeBtn.disabled = true;
            executeBtn.textContent = 'Processing...';
            
            addMessage('User', query, 'user-msg');
            input.value = '';
            
            scrollToBottom();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: query,
                        model: modelSelect.value
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    addMessage('Neural Network', data.response, 'ai-msg', data.model);
                    updateMetrics(data.cost_info);
                } else {
                    addMessage('System Error', data.error, 'error-msg');
                }
                
            } catch (error) {
                addMessage('System Error', 'Interface communication failure: ' + error.message, 'error-msg');
            } finally {
                input.disabled = false;
                executeBtn.disabled = false;
                executeBtn.textContent = 'Execute';
                input.focus();
                scrollToBottom();
            }
        }
        
        function addMessage(sender, message, className, model = '') {
            const terminal = document.getElementById('terminal');
            const msgDiv = document.createElement('div');
            msgDiv.className = `msg ${className}`;
            
            const timestamp = new Date().toLocaleTimeString();
            const modelInfo = model ? ` :: ${model.replace('vertex/gemini-', '').toUpperCase()}` : '';
            
            msgDiv.innerHTML = `
                <div class="msg-header">${sender}${modelInfo}</div>
                <div class="msg-content">${message.replace(/\\n/g, '<br>')}</div>
                <div class="timestamp">${timestamp}</div>
            `;
            
            terminal.appendChild(msgDiv);
        }
        
        function updateMetrics(costInfo) {
            document.getElementById('last-cost').textContent = `$${costInfo.last_cost.toFixed(6)}`;
            document.getElementById('session-cost').textContent = `$${costInfo.session_cost.toFixed(6)}`;
            document.getElementById('message-count').textContent = costInfo.message_count;
            document.getElementById('avg-cost').textContent = `$${costInfo.avg_cost.toFixed(6)}`;
            
            const sessionEl = document.getElementById('session-cost');
            const lastEl = document.getElementById('last-cost');
            
            sessionEl.classList.remove('warning', 'danger');
            lastEl.classList.remove('warning', 'danger');
            
            if (costInfo.session_cost > 0.01) {
                sessionEl.classList.add('danger');
            } else if (costInfo.session_cost > 0.005) {
                sessionEl.classList.add('warning');
            }
            
            if (costInfo.last_cost > 0.002) {
                lastEl.classList.add('danger');
            } else if (costInfo.last_cost > 0.001) {
                lastEl.classList.add('warning');
            }
        }
        
        function scrollToBottom() {
            const terminal = document.getElementById('terminal');
            setTimeout(() => {
                terminal.scrollTop = terminal.scrollHeight;
            }, 100);
        }
        
        if (window.innerWidth > 768) {
            document.getElementById('neural-input').focus();
        }
    </script>
</body>
</html>'''

class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/chat.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data['message']
                model = data['model']
                
                print(f"User: {message}")
                print(f"Using model: {model}")
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    max_tokens=500,
                    temperature=0.7
                )
                
                ai_message = response.choices[0].message.content
                usage = response.usage
                
                global session_cost, message_count
                message_cost = calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
                session_cost += message_cost
                message_count += 1
                avg_cost = session_cost / message_count if message_count > 0 else 0
                
                print(f"AI: {ai_message}")
                print(f"Cost: ${message_cost:.6f} | Session: ${session_cost:.6f} | Tokens: {usage.total_tokens}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = {
                    "success": True,
                    "response": ai_message,
                    "model": model,
                    "cost_info": {
                        "last_cost": message_cost,
                        "session_cost": session_cost,
                        "message_count": message_count,
                        "avg_cost": avg_cost,
                        "tokens": usage.total_tokens
                    }
                }
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                print(f"Error: {e}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_data = {
                    "success": False,
                    "error": str(e)
                }
                self.wfile.write(json.dumps(error_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def main():
    try:
        print("Testing connection to goop proxy...")
        response = client.chat.completions.create(
            model="vertex/gemini-2.0-flash-lite-001",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("Connection to goop proxy working!")
    except Exception as e:
        print(f"Cannot connect to goop proxy: {e}")
        print("Make sure your goop proxy is running on port 8080")
        return
    
    port = 8000
    server = HTTPServer(('0.0.0.0', port), ChatHandler)
    
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Starting AI Neural Interface")
    print(f"Local access: http://localhost:{port}")
    print(f"Network access: http://{local_ip}:{port}")
    print("Press Ctrl+C to disconnect")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nInterface disconnected")
        server.server_close()

if __name__ == "__main__":
    main()
# web_chat.py

Web-based AI Chat Interface with Real-Time Cost Tracking for Goop Proxy

## Overview

A cyberpunk-themed web application that provides a browser-based chat interface for your [goop proxy](https://github.com/robertprast/goop) with real-time Vertex AI cost monitoring. Features a retro terminal aesthetic with live cost metrics, model selection, and responsive design.

## Features

- **Web-based interface** - Chat with AI through your browser
- **Real-time cost tracking** - Live cost metrics displayed on the interface
- **Multiple model support** - Switch between Gemini models during chat
- **Cyberpunk UI** - Retro terminal design with green-on-black aesthetic
- **Mobile responsive** - Works on desktop, tablet, and mobile devices
- **Live metrics dashboard** - Monitor costs, token usage, and session statistics
- **Network accessible** - Share the interface across your local network
- **No external dependencies** - Self-contained Python web server

## Requirements

### Software
- Python 3.6 or higher
- [goop proxy](https://github.com/robertprast/goop) installed and running

### Python Dependencies
```bash
pip install openai
```

## Setup

1. **Install and configure goop proxy**
   - Follow the setup instructions at https://github.com/robertprast/goop
   - Ensure your goop proxy is running on `http://localhost:8080`

2. **Configure the script**
   - Open `web_chat.py`
   - Replace `"your-api-key"` with your actual API key
   - Verify the `base_url` matches your goop proxy setup (default: `http://localhost:8080/openai-proxy/v1`)

3. **Update pricing (optional)**
   - The script includes Vertex AI pricing as of January 2025
   - Verify current rates at https://cloud.google.com/vertex-ai/pricing
   - Update the `MODEL_PRICING` dictionary if needed

## Usage

### Start the Web Server
```bash
python web_chat.py
```

### Access the Interface
After starting, you'll see:
```
Testing connection to goop proxy...
Connection to goop proxy working!
Starting AI Neural Interface
Local access: http://localhost:8000
Network access: http://192.168.1.100:8000
Press Ctrl+C to disconnect
```

### Using the Web Interface

1. **Open your browser** to `http://localhost:8000`
2. **Select a model** from the dropdown menu
3. **Type your message** in the input field
4. **Press Enter** or click "EXECUTE" to send
5. **Monitor costs** in the real-time metrics dashboard

### Available Models

The interface provides four Gemini models:

- **Gemini 2.0 Flash Lite** - Fastest response (0.51s), lowest cost
- **Gemini 2.5 Flash Preview** - Latest features, experimental
- **Gemini 2.0 Flash** - Most reliable, production-ready
- **Gemini 2.5 Pro Preview** - Most capable, highest cost

## Interface Features

### Real-Time Metrics Dashboard
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ LAST QUERY COST │   SESSION COST  │  TOTAL QUERIES  │  AVERAGE COST   │
│    $0.000045    │    $0.000156    │        3        │    $0.000052    │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Chat Interface
- **User messages** appear in yellow
- **AI responses** appear in green
- **Error messages** appear in red
- **Timestamps** for each message
- **Model information** displayed with responses

### Cost Warnings
- **Yellow warning** when session cost exceeds $0.005
- **Red danger** when session cost exceeds $0.01
- **High cost alerts** for expensive individual messages

## Network Access

The web server binds to `0.0.0.0:8000`, making it accessible across your local network:

- **Local access**: `http://localhost:8000`
- **Network access**: `http://[your-ip]:8000`
- **Mobile access**: Use the network IP on mobile devices

### Security Note
The server is only accessible on your local network. For production use, implement proper authentication and HTTPS.

## Customization

### Change the Port
Edit the `port` variable in the `main()` function:
```python
port = 8000  # Change to your preferred port
```

### Modify the Interface Theme
The HTML and CSS are embedded in the `HTML_PAGE` variable. You can customize:
- Colors and styling
- Layout and fonts
- Text and labels
- Animations and effects

### Add Custom Models
Update the `MODEL_PRICING` dictionary:
```python
MODEL_PRICING = {
    "vertex/your-custom-model": {
        "input_per_1k": 0.001,
        "output_per_1k": 0.002,
        "name": "Your Custom Model",
        "description": "Custom (1.0s)",
        "speed": "medium"
    }
}
```

### Cost Thresholds
Modify warning thresholds in the JavaScript:
```javascript
if (costInfo.session_cost > 0.01) {
    sessionEl.classList.add('danger');
} else if (costInfo.session_cost > 0.005) {
    sessionEl.classList.add('warning');
}
```

## Troubleshooting

### Connection Issues
```
Cannot connect to goop proxy: [error details]
```
**Solutions:**
- Ensure goop proxy is running: `http://localhost:8080`
- Check that the proxy is configured for Vertex AI
- Verify your API key is correct
- Test the proxy directly with curl or browser

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solutions:**
- Change the port number in the script
- Kill any existing process using port 8000: `lsof -ti:8000 | xargs kill`
- Use `netstat -an | grep 8000` to check port usage

### Browser Compatibility
The interface works best with modern browsers. For older browsers:
- Disable CSS animations
- Simplify the styling
- Remove advanced CSS features

### Mobile Issues
If the interface doesn't work well on mobile:
- The responsive CSS should handle most devices
- Force desktop mode if needed
- Consider increasing font sizes for better readability

## File Structure

The script is self-contained with embedded HTML/CSS/JavaScript:
```
web_chat.py
├── Python web server (BaseHTTPRequestHandler)
├── OpenAI client configuration
├── Cost calculation functions
├── Embedded HTML interface
├── CSS styling (cyberpunk theme)
└── JavaScript for real-time updates
```

## API Endpoints

The web server provides two endpoints:

- **GET /** - Serves the HTML interface
- **POST /chat** - Handles chat messages and returns JSON responses

### Chat API Format
**Request:**
```json
{
    "message": "Your message here",
    "model": "vertex/gemini-2.0-flash-lite-001"
}
```

**Response:**
```json
{
    "success": true,
    "response": "AI response text",
    "model": "vertex/gemini-2.0-flash-lite-001",
    "cost_info": {
        "last_cost": 0.000045,
        "session_cost": 0.000156,
        "message_count": 3,
        "avg_cost": 0.000052,
        "tokens": 67
    }
}
```

## Performance Notes

- **Memory usage**: Minimal, session data stored in global variables
- **Concurrent users**: Single-threaded server, one user at a time
- **Session persistence**: Data resets when server restarts
- **Response time**: Depends on selected Gemini model (0.5s - 1.3s)

## License

This script is part of the goop-utilities collection. See the main repository for licensing information.

## Contributing

Found a bug or want to add a feature? Please contribute to the main [goop-utilities](https://github.com/yourusername/goop-utilities) repository.

## Related Tools

- `chat_with_costs.py` - Terminal-based chat interface
- `verify_models.py` - Check available Vertex AI models
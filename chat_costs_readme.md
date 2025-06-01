# chat_with_costs.py

AI Chat with Real-Time Cost Estimation for Goop Proxy

## Overview

An interactive terminal-based chat application that connects to your [goop proxy](https://github.com/robertprast/goop) and provides real-time cost tracking for Vertex AI API usage. Monitor your AI spending as you chat, with support for multiple Gemini models and detailed cost analysis.

## Features

- **Real-time cost tracking** - See the exact cost of each message as you chat
- **Multiple model support** - Choose between Gemini 2.0 Flash Lite, 2.5 Flash Preview, and 2.0 Flash
- **Session tracking** - Monitor total costs, token usage, and message counts for your current session
- **Historical logging** - All usage is logged to `chat_costs.log` for later analysis
- **Cost warnings** - Get alerts when messages or sessions exceed cost thresholds
- **Model switching** - Change AI models mid-conversation
- **Cost analysis** - Review historical usage patterns and monthly projections

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
   - Open `chat_with_costs.py`
   - Replace `"your-api-key"` with your actual API key or test.
   - Verify the `base_url` matches your goop proxy setup (default: `http://localhost:8080/openai-proxy/v1`)

3. **Update pricing (optional)**
   - The script includes Vertex AI pricing as of January 2025
   - Verify current rates at https://cloud.google.com/vertex-ai/pricing
   - Update the `MODEL_PRICING` dictionary if needed

## Usage

### Basic Chat
```bash
python chat_with_costs.py
```

### Choose Your Options
When you run the script, you'll see:
```
AI Chat with Cost Tracking
Built for goop proxy: https://github.com/robertprast/goop

Options:
1. Start chat
2. View cost analysis

Choose (1 or 2, Enter for chat):
```

### Model Selection
```
Available Models:
1. Gemini 2.0 Flash Lite
   Fastest (0.56s) | ~$0.000038 per 100 tokens
   Best for quick chat, high-volume usage

2. Gemini 2.5 Flash Preview
   Fast (0.70s) | ~$0.000075 per 100 tokens
   Latest features, experimental

3. Gemini 2.0 Flash
   Reliable (2.04s) | ~$0.000075 per 100 tokens
   Most reliable, production-ready

Select model (1-3) or press Enter for fastest:
```

### Chat Interface
```
You: Hello, how are you?
AI is thinking...
AI: Hello! I'm doing well, thank you for asking. How are you doing today?
   Cost: $0.000045 | Session: $0.000045 | Tokens: 67 | Msg #1
```

### Available Commands
- `quit`, `exit`, `bye`, `q` - Exit the chat
- `switch` - Change to a different AI model
- `costs` - Display current session cost summary

## Cost Information

### Real-Time Display
Each message shows:
- **Cost**: Cost of the current message
- **Session**: Total cost for this chat session
- **Tokens**: Number of tokens used in this message
- **Msg #**: Message number in the session

### Cost Warnings
- **Session warning**: Appears when session cost exceeds $0.01
- **High cost message**: Appears when a single message costs more than $0.001

### Example Output
```
Cost Summary:
This session: $0.000156
Total tokens: 234
Messages: 3
Avg per message: $0.000052
Models used: 1
```

## Historical Analysis

Choose option 2 from the main menu to see:
- Total spending across all sessions
- Cost breakdown by model
- Token usage statistics
- Monthly cost projections
- Usage patterns

## File Output

The script creates `chat_costs.log` which contains:
```json
{"timestamp": "2025-06-01T10:30:00", "model": "vertex/gemini-2.0-flash-lite-001", "prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150, "cost_usd": 0.000067, "session_total": 0.000067}
```

## Troubleshooting

### Connection Issues
```
Cannot connect to goop proxy: [error details]
```
**Solutions:**
- Ensure goop proxy is running: check `http://localhost:8080` in your browser
- Verify the proxy is configured correctly for Vertex AI
- Check that your API key is valid

### Model Access Issues
```
Unknown model vertex/gemini-2.0-flash-lite-001, using default pricing
```
**Solutions:**
- Use the `verify_models.py` script to check available models
- Update the `MODEL_PRICING` dictionary with your accessible models
- Ensure your Google Cloud project has access to the Gemini models

### High Costs
The script includes built-in warnings, but monitor usage carefully:
- Flash Lite models are most cost-effective for general chat
- Longer conversations increase context size and costs
- Preview models may have different pricing

## Configuration

### Custom Pricing
Update the `MODEL_PRICING` dictionary:
```python
MODEL_PRICING = {
    "vertex/your-model-name": {
        "input_per_1k": 0.000075,
        "output_per_1k": 0.0003,
        "name": "Your Model Name",
        "speed": "Fast",
        "description": "Model description"
    }
}
```

### Different Proxy Setup
If your goop proxy runs on a different port or host:
```python
client = OpenAI(base_url="http://your-host:your-port/openai-proxy/v1", api_key="your-api-key")
```

## License

This script is part of the goop-utilities collection. See the main repository for licensing information.

## Contributing

Found a bug or want to add a feature? Please contribute to the main [goop-utilities](https://github.com/yourusername/goop-utilities) repository.

## Related Tools

- `web_chat.py` - Web-based chat interface
- `verify_models.py` - Check available Vertex AI models
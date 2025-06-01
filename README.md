# goop-utilities

A comprehensive collection of Python utilities that enhance your [goop](https://github.com/robertprast/goop) AI proxy with cost monitoring, web interfaces, and model verification tools.

## Overview

These tools add cost tracking, performance monitoring, and user-friendly interfaces to your goop proxy setup. Whether you prefer terminal-based chat, web interfaces, or need to verify model access, this collection has you covered.

## Requirements

- Python 3.6 or higher
- [goop proxy](https://github.com/robertprast/goop) installed and running
- `pip install openai`

## Quick Start

1. **Set up goop proxy** following the [official instructions](https://github.com/robertprast/goop)
2. **Verify model access**: `python verify_models.py`
3. **Start chatting**: `python chat_with_costs.py` or `python web_chat.py`

## Tools Included

### 🔍 verify_models.py
**Model Access Verification and Performance Testing**

Diagnose which Vertex AI models you have access to and benchmark their performance through your goop proxy.

**Purpose**: Verify model availability and measure response times  
**Output**: Detailed report of working models with performance metrics  
**Use case**: Run this first to discover your available models before using other tools

```bash
python verify_models.py
```

**Key Features:**
- Tests 10+ Gemini and PaLM models automatically
- Measures response times and token usage for each model
- Provides recommendations for fastest, cheapest, and newest models
- Exports results to `working_models.txt` for reference
- Includes troubleshooting guidance for common setup issues

**Sample Output:**
```
WORKING MODELS (3):
 1. vertex/gemini-1.5-flash-002    (0.51s) - Cheapest option
 2. vertex/gemini-2.0-flash-001    (0.83s) - Most reliable
 3. vertex/gemini-2.0-flash-lite   (0.45s) - Fastest response
```

---

### 💬 chat_with_costs.py
**Terminal Chat Interface with Real-Time Cost Tracking**

Interactive command-line chat application with live cost monitoring for every message and conversation.

**Purpose**: Chat with AI models while tracking costs in real-time  
**Interface**: Terminal/command-line based  
**Best for**: Developers, power users, and automated workflows

```bash
python chat_with_costs.py
```

**Key Features:**
- Real-time cost calculation and display for each message
- Support for multiple Gemini models with easy switching
- Session cost tracking with running totals and averages
- Historical usage logging to `chat_costs.log`
- Cost warnings when spending exceeds thresholds
- Model performance comparison (speed vs cost)

**Sample Interaction:**
```
You: What's the weather like?
AI: I don't have access to current weather data...
   Cost: $0.000045 | Session: $0.000123 | Tokens: 67 | Msg #3
```

**Commands:**
- `switch` - Change AI model mid-conversation
- `costs` - Display session cost summary
- `quit` - Exit and save cost log

---

### 🌐 web_chat.py
**Web-Based Chat Interface with Cost Dashboard**

Modern web application with cyberpunk-themed UI, real-time cost metrics, and mobile-responsive design.

**Purpose**: Browser-based AI chat with visual cost monitoring  
**Interface**: Web browser (localhost:8000)  
**Best for**: Visual users, sharing across devices, and demonstrations

```bash
python web_chat.py
# Open http://localhost:8000 in your browser
```

**Key Features:**
- Cyberpunk-themed terminal aesthetic with green-on-black styling
- Live cost dashboard with 4 key metrics displayed prominently
- Mobile-responsive design that works on phones and tablets
- Model selector dropdown with response time information
- Network accessibility (share across local network devices)
- Visual cost warnings with color-coded alerts

**Interface Elements:**
```
┌─────────────────────────────────────────────────────────────┐
│ LAST QUERY: $0.000045 │ SESSION: $0.000156 │ QUERIES: 3    │
└─────────────────────────────────────────────────────────────┘
│ Model: [Gemini 2.0 Flash Lite ▼]                           │
├─────────────────────────────────────────────────────────────┤
│ > Your message here...                    [EXECUTE]         │
└─────────────────────────────────────────────────────────────┘
```

**Access Options:**
- Local: `http://localhost:8000`
- Network: `http://[your-ip]:8000` (for mobile/other devices)

---

## Workflow

### Recommended Usage Order

1. **Start with verification**: Run `verify_models.py` to discover available models
2. **Choose your interface**: 
   - `chat_with_costs.py` for terminal-based usage
   - `web_chat.py` for browser-based interface
3. **Monitor costs**: Both chat tools provide real-time cost tracking
4. **Optimize**: Use verification results to choose the best models for your needs

### Model Selection Guide

Based on verification results:
- **Daily use**: Fastest verified model (usually Flash Lite)
- **Cost optimization**: Cheapest verified model (usually 1.5-flash)
- **Maximum capability**: Most advanced verified model (usually Pro variants)
- **Reliability**: Standard models without "preview" designation

## Configuration

### API Key Setup
Replace `"your-api-key"` in each script with your actual API key:
```python
client = OpenAI(base_url="http://localhost:8080/openai-proxy/v1", api_key="your-actual-key")
```

### Pricing Updates
Verify current Vertex AI pricing at [cloud.google.com/vertex-ai/pricing](https://cloud.google.com/vertex-ai/pricing) and update the `MODEL_PRICING` dictionaries if needed.

### Custom Models
Add your custom models to the pricing dictionaries in each script:
```python
MODEL_PRICING = {
    "vertex/your-custom-model": {
        "input_per_1k": 0.001,
        "output_per_1k": 0.002,
        "name": "Your Custom Model",
        # ... additional config
    }
}
```

## Output Files

- **`working_models.txt`** - Model verification results from verify_models.py
- **`chat_costs.log`** - Detailed usage logs from chat_with_costs.py

## Troubleshooting

### Connection Issues
- Ensure goop proxy is running: `http://localhost:8080`
- Verify your API key is configured correctly
- Check Google Cloud project has Vertex AI API enabled

### Model Access Issues
- Run `verify_models.py` to check available models
- Some preview models require special access or specific regions
- Update model lists based on your verification results

### Cost Tracking Issues
- Verify pricing data is current for your region
- Check that usage data is being returned by the API
- Monitor the generated log files for detailed information

## Contributing

Found a bug or want to add a feature? Please:
1. Fork this repository
2. Create a feature branch
3. Submit a pull request

## Related Projects

- [goop](https://github.com/robertprast/goop) - The AI proxy that powers these utilities
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs) - Official Google Cloud AI platform docs
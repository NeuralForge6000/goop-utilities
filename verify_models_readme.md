# verify_models.py

Vertex AI Model Access Verification for Goop Proxy

## Overview

A diagnostic tool that tests which Vertex AI models you have access to through your [goop proxy](https://github.com/robertprast/goop). This script helps you discover available models, measure their performance, and get recommendations for optimal usage in your AI applications.

## Features

- **Model access verification** - Test which Gemini and PaLM models work with your setup
- **Performance benchmarking** - Measure response times for each model
- **Smart recommendations** - Get suggestions for fastest, cheapest, and newest models
- **Connection testing** - Verify your goop proxy is working correctly
- **Detailed reporting** - Export results to a text file for reference
- **Troubleshooting guidance** - Clear error messages and setup help

## Why Use This Script

Before building AI applications, you need to know:
- Which models your Google Cloud project has access to
- How fast each model responds in your environment
- Which models are best for different use cases
- Whether your goop proxy is configured correctly

This script answers all these questions automatically.

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
   - Verify your Google Cloud project has Vertex AI API enabled

2. **Configure the script**
   - Open `verify_models.py`
   - Replace `"your-api-key"` with your actual API key
   - Verify the `base_url` matches your goop proxy setup

3. **Check Google Cloud access**
   - Ensure your service account has Vertex AI permissions
   - Verify your project has the models enabled in your region

## Usage

### Run the Verification
```bash
python verify_models.py
```

### Sample Output
```
VERTEX AI MODEL VERIFICATION
Testing model access through goop proxy...
============================================================
Testing connection to goop proxy...
Connection successful!

Testing: vertex/gemini-2.0-flash-001
   Standard - Reliable production model
   Testing... SUCCESS (0.83s)
   Response: SUCCESS! Here's an interesting fact: Octopuses have three hearts.
   Tokens: 67 total

Testing: vertex/gemini-1.5-flash-002
   Cheapest - Most cost-effective option
   Testing... SUCCESS (0.51s)
   Response: SUCCESS! Did you know that honey never spoils?
   Tokens: 45 total

Testing: vertex/gemini-2.5-flash-preview-05-20
   Preview - Latest preview features
   Testing... FAILED
   Error: Model not available in your region

============================================================
RESULTS SUMMARY
============================================================

WORKING MODELS (2):
--------------------------------------------------
 1. vertex/gemini-1.5-flash-002
    Cheapest - Most cost-effective option
    Response time: 0.51s

 2. vertex/gemini-2.0-flash-001
    Standard - Reliable production model
    Response time: 0.83s

FAILED MODELS (1):
--------------------------------------------------
• vertex/gemini-2.5-flash-preview-05-20 (Preview) - Model not available in your region...

RECOMMENDATIONS:
--------------------------------------------------
Fastest: vertex/gemini-1.5-flash-002 (0.51s)
Cheapest: vertex/gemini-1.5-flash-002
Newest: vertex/gemini-2.0-flash-001

RECOMMENDED SETUP:
   • Daily use: vertex/gemini-1.5-flash-002
   • Backup: vertex/gemini-2.0-flash-001

Detailed results saved to 'working_models.txt'

Next steps:
   1. Use these working models in chat applications
   2. Update MODEL_PRICING in other scripts with working models
   3. Set up cost monitoring for your usage
   4. Test the models in chat_with_costs.py or web_chat.py
```

## Models Tested

The script tests these model categories:

### Standard Models
- **vertex/gemini-2.0-flash-001** - Production-ready, reliable
- **vertex/gemini-1.5-flash-002** - Cost-effective, fast
- **vertex/gemini-1.5-pro-002** - Advanced reasoning capabilities
- **vertex/gemini-2.0-flash-lite-001** - Fastest response times

### Preview Models
- **vertex/gemini-2.5-flash-preview-05-20** - Latest features
- **vertex/gemini-2.5-pro-preview-05-06** - Most advanced

### Legacy Models
- **vertex/chat-bison-001** - Older PaLM-based chat model
- **vertex/text-bison-001** - Text completion
- **vertex/code-bison-001** - Code-specialized

### Alternative Formats
- **gemini-2.0-flash-001** - Without vertex/ prefix
- **google/gemini-2.0-flash-001** - With google/ prefix

## Output Files

### working_models.txt
The script creates a detailed report file:
```
WORKING VERTEX AI MODELS
==============================

Models verified through goop proxy:

vertex/gemini-1.5-flash-002
  Cheapest - Most cost-effective option
  Response time: 0.51s

vertex/gemini-2.0-flash-001
  Standard - Reliable production model
  Response time: 0.83s

Usage in other scripts:
Update MODEL_PRICING dictionary with these working models
```

## Integration with Other Scripts

After running verification, update your other goop-utilities scripts:

### chat_with_costs.py
```python
MODEL_PRICING = {
    "vertex/gemini-1.5-flash-002": {
        "input_per_1k": 0.000075,
        "output_per_1k": 0.0003,
        "name": "Gemini 1.5 Flash",
        "speed": "Fastest (0.51s)",
        "description": "Most cost-effective verified model"
    },
    # Add other working models...
}
```

### web_chat.py
Update the MODEL_PRICING dictionary and HTML select options with your verified models.

## Troubleshooting

### Connection Failures
```
Connection failed: Connection refused
```
**Solutions:**
- Ensure goop proxy is running: `http://localhost:8080`
- Check the proxy logs for errors
- Verify your goop configuration files
- Test the proxy directly: `curl http://localhost:8080/health`

### Authentication Errors
```
Error: 401 Unauthorized
```
**Solutions:**
- Verify your API key is correct
- Check your Google Cloud service account permissions
- Ensure Vertex AI API is enabled in your project
- Verify your goop proxy authentication configuration

### Model Access Errors
```
Error: Model not available in your region
```
**Solutions:**
- Some models are region-specific (especially preview models)
- Check Google Cloud Console for available models in your region
- Preview models may require allowlist access
- Try alternative model versions

### Timeout Errors
```
Error: Request timeout
```
**Solutions:**
- Increase the timeout value in the script
- Check your internet connection
- Verify Google Cloud service status
- Try testing with fewer models at once

## Customization

### Add Custom Models
Edit the `priority_models` list:
```python
priority_models = [
    ("your/custom-model", "Custom", "Your model description"),
    # Add more models...
]
```

### Modify Test Parameters
```python
response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": "Your test message"}],
    max_tokens=50,    # Adjust token limit
    timeout=15        # Adjust timeout
)
```

### Change Output Format
Modify the results display or file output format in the `main()` function.

## Understanding Results

### Response Times
- **< 0.5s**: Excellent for real-time applications
- **0.5-1.0s**: Good for interactive use
- **1.0-2.0s**: Acceptable for batch processing
- **> 2.0s**: May indicate network or configuration issues

### Model Recommendations
- **Daily use**: Fastest working model for regular tasks
- **Backup**: Second-fastest for redundancy
- **Experimentation**: Newest or most capable for testing

### Cost Implications
Use verification results to choose cost-effective models:
- **1.5-flash models**: Typically cheapest
- **2.0-flash models**: Balanced cost/performance
- **Pro models**: Most expensive but most capable

## Security Notes

- The script only makes test API calls with minimal content
- No sensitive data is logged or transmitted
- Results are saved locally in plain text
- API keys should be kept secure and not shared

## Performance Tips

- Run verification periodically as model availability changes
- Test during off-peak hours for more consistent results
- Save results and compare performance over time
- Use fastest models for development, optimize for production

## License

This script is part of the goop-utilities collection. See the main repository for licensing information.

## Contributing

Found a bug or want to add a feature? Please contribute to the main [goop-utilities](https://github.com/yourusername/goop-utilities) repository.

## Related Tools

- `chat_with_costs.py` - Terminal chat interface using verified models
- `web_chat.py` - Web interface using verified models
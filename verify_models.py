# verify_models.py - Test Vertex AI Model Access
# 
# Verify which Vertex AI models you have access to through goop proxy
# Requires: https://github.com/robertprast/goop
# Dependencies: pip install openai
# Setup: Follow goop setup instructions, then run this script

from openai import OpenAI
import time

# Configure for your goop proxy setup
# Default goop proxy runs on localhost:8080
client = OpenAI(base_url="http://localhost:8080/openai-proxy/v1", api_key="your-api-key")

# Priority models - most likely to work and most useful
# Update this list based on your Google Cloud project's model access
priority_models = [
    # Standard Gemini models (high priority)
    ("vertex/gemini-2.0-flash-001", "Standard", "Reliable production model"),
    ("vertex/gemini-1.5-flash-002", "Cheapest", "Most cost-effective option"), 
    ("vertex/gemini-1.5-pro-002", "Smartest", "Best reasoning capabilities"),
    ("vertex/gemini-2.0-flash-lite-001", "Fastest", "Fastest response times"),
    
    # Preview models (if available in your region)
    ("vertex/gemini-2.5-flash-preview-05-20", "Preview", "Latest preview features"),
    ("vertex/gemini-2.5-pro-preview-05-06", "Advanced Preview", "Most advanced preview model"),
    
    # Legacy models (for compatibility testing)
    ("vertex/chat-bison-001", "Legacy", "Older PaLM-based model"),
    ("vertex/text-bison-001", "Text", "Text completion model"),
    ("vertex/code-bison-001", "Code", "Code-specialized model"),
    
    # Alternative formats to test proxy compatibility
    ("gemini-2.0-flash-001", "Alt Format", "Without vertex/ prefix"),
    ("google/gemini-2.0-flash-001", "Alt Format 2", "With google/ prefix"),
]

def test_model_detailed(model_name, description, use_case):
    """Test a model with detailed output"""
    print(f"\nTesting: {model_name}")
    print(f"   {description} - {use_case}")
    print(f"   Testing... ", end="", flush=True)
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user", 
                "content": f"Hello! I'm testing {model_name}. Please respond with 'SUCCESS' and tell me one interesting fact."
            }],
            max_tokens=50,
            timeout=15
        )
        
        duration = time.time() - start_time
        content = response.choices[0].message.content.strip()
        
        print(f"SUCCESS ({duration:.2f}s)")
        print(f"   Response: {content}")
        
        # Try to get usage info if available
        if hasattr(response, 'usage') and response.usage:
            print(f"   Tokens: {response.usage.total_tokens} total")
        
        return True, content, duration
        
    except Exception as e:
        print(f"FAILED")
        print(f"   Error: {str(e)[:100]}")
        return False, str(e), 0

def main():
    print("VERTEX AI MODEL VERIFICATION")
    print("Testing model access through goop proxy...")
    print("=" * 60)
    
    # Test connection first
    print("Testing connection to goop proxy...")
    try:
        # Quick connection test
        test_response = client.chat.completions.create(
            model="vertex/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
            timeout=10
        )
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure goop proxy is running on http://localhost:8080")
        print("Check your API key configuration")
        return
    
    working_models = []
    failed_models = []
    
    for model, tag, description in priority_models:
        success, result, duration = test_model_detailed(model, tag, description)
        
        if success:
            working_models.append((model, tag, description, duration))
        else:
            failed_models.append((model, tag, result))
        
        # Brief pause between tests
        time.sleep(1)
    
    # Results Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    if working_models:
        print(f"\nWORKING MODELS ({len(working_models)}):")
        print("-" * 50)
        
        # Sort by speed for recommendations
        working_models.sort(key=lambda x: x[3])  # Sort by duration
        
        for i, (model, tag, desc, duration) in enumerate(working_models, 1):
            print(f"{i:2d}. {model}")
            print(f"    {tag} - {desc}")
            print(f"    Response time: {duration:.2f}s")
            print()
    
    if failed_models:
        print(f"\nFAILED MODELS ({len(failed_models)}):")
        print("-" * 50)
        for model, tag, error in failed_models:
            print(f"• {model} ({tag}) - {error[:60]}...")
    
    # Recommendations
    if working_models:
        print("\nRECOMMENDATIONS:")
        print("-" * 50)
        
        fastest = min(working_models, key=lambda x: x[3])
        print(f"Fastest: {fastest[0]} ({fastest[3]:.2f}s)")
        
        cheapest_candidates = [m for m in working_models if "1.5-flash" in m[0] or "bison" in m[0]]
        if cheapest_candidates:
            print(f"Cheapest: {cheapest_candidates[0][0]}")
        
        newest_candidates = [m for m in working_models if "2.5" in m[0]]
        if newest_candidates:
            print(f"Newest: {newest_candidates[0][0]}")
        
        print(f"\nRECOMMENDED SETUP:")
        print(f"   • Daily use: {working_models[0][0]}")
        if len(working_models) > 1:
            print(f"   • Backup: {working_models[1][0]}")
        if len(working_models) > 2:
            print(f"   • Experimentation: {working_models[2][0]}")
    
    # Save working models with UTF-8 encoding
    if working_models:
        with open("working_models.txt", "w", encoding='utf-8') as f:
            f.write("WORKING VERTEX AI MODELS\n")
            f.write("=" * 30 + "\n\n")
            f.write("Models verified through goop proxy:\n\n")
            for model, tag, desc, duration in working_models:
                f.write(f"{model}\n")
                f.write(f"  {tag} - {desc}\n")
                f.write(f"  Response time: {duration:.2f}s\n\n")
            
            f.write("Usage in other scripts:\n")
            f.write("Update MODEL_PRICING dictionary with these working models\n")
        
        print(f"\nDetailed results saved to 'working_models.txt'")
    
    if not working_models:
        print("\nTROUBLESHOoting:")
        print("- Verify goop proxy is running and configured correctly")
        print("- Check your Google Cloud project has Vertex AI API enabled")
        print("- Ensure your service account has proper permissions")
        print("- Try updating your API key")
    else:
        print(f"\nNext steps:")
        print(f"   1. Use these working models in chat applications")
        print(f"   2. Update MODEL_PRICING in other scripts with working models")
        print(f"   3. Set up cost monitoring for your usage")
        print(f"   4. Test the models in chat_with_costs.py or web_chat.py")

if __name__ == "__main__":
    main()
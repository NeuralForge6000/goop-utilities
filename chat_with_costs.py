# chat_with_costs.py - AI Chat with Real-Time Cost Estimation
# 
# Chat application with cost tracking for goop proxy
# Requires: https://github.com/robertprast/goop
# Dependencies: pip install openai
# Setup: Follow goop setup instructions, then run this script

from openai import OpenAI
import json
import datetime
from dataclasses import dataclass
from typing import Dict, List
import os

# Configure for your goop proxy setup
# Default goop proxy runs on localhost:8080
client = OpenAI(base_url="http://localhost:8080/openai-proxy/v1", api_key="your-api-key")

# Vertex AI Pricing (as of January 2025) - verify current rates at cloud.google.com
# Update these rates based on your region and current Google Cloud pricing
MODEL_PRICING = {
    "vertex/gemini-2.0-flash-lite-001": {
        "input_per_1k": 0.000075,   # Cheapest option
        "output_per_1k": 0.0003,
        "name": "Gemini 2.0 Flash Lite",
        "speed": "Fastest (0.56s)",
        "description": "Best for quick chat, high-volume usage"
    },
    "vertex/gemini-2.5-flash-preview-05-20": {
        "input_per_1k": 0.00015,    # Preview pricing
        "output_per_1k": 0.0006,
        "name": "Gemini 2.5 Flash Preview", 
        "speed": "Fast (0.70s)",
        "description": "Latest features, experimental"
    },
    "vertex/gemini-2.0-flash-001": {
        "input_per_1k": 0.00015,    # Standard pricing
        "output_per_1k": 0.0006,
        "name": "Gemini 2.0 Flash",
        "speed": "Reliable (2.04s)", 
        "description": "Most reliable, production-ready"
    }
}

@dataclass
class ChatCosts:
    session_cost: float = 0.0
    total_tokens: int = 0
    message_count: int = 0
    model_usage: Dict[str, float] = None
    
    def __post_init__(self):
        if self.model_usage is None:
            self.model_usage = {}

class CostTracker:
    def __init__(self):
        self.session_costs = ChatCosts()
        self.load_historical_costs()
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a single request"""
        if model not in MODEL_PRICING:
            print(f"Unknown model {model}, using default pricing")
            model = "vertex/gemini-2.0-flash-001"  # Fallback to known model
        
        pricing = MODEL_PRICING[model]
        input_cost = (prompt_tokens / 1000) * pricing["input_per_1k"]
        output_cost = (completion_tokens / 1000) * pricing["output_per_1k"]
        total_cost = input_cost + output_cost
        
        return total_cost
    
    def track_usage(self, model: str, prompt_tokens: int, completion_tokens: int) -> dict:
        """Track usage and return cost info"""
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        
        # Update session totals
        self.session_costs.session_cost += cost
        self.session_costs.total_tokens += (prompt_tokens + completion_tokens)
        self.session_costs.message_count += 1
        
        # Track per-model usage
        if model not in self.session_costs.model_usage:
            self.session_costs.model_usage[model] = 0.0
        self.session_costs.model_usage[model] += cost
        
        # Log to file for historical tracking
        self.log_usage(model, prompt_tokens, completion_tokens, cost)
        
        return {
            "request_cost": cost,
            "session_cost": self.session_costs.session_cost,
            "session_tokens": self.session_costs.total_tokens,
            "message_count": self.session_costs.message_count,
            "cost_per_message": self.session_costs.session_cost / self.session_costs.message_count if self.session_costs.message_count > 0 else 0
        }
    
    def log_usage(self, model: str, prompt_tokens: int, completion_tokens: int, cost: float):
        """Log usage to file for historical tracking"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": cost,
            "session_total": self.session_costs.session_cost
        }
        
        try:
            with open("chat_costs.log", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Could not log usage: {e}")
    
    def load_historical_costs(self):
        """Load historical costs from log file"""
        try:
            if os.path.exists("chat_costs.log"):
                total_historical = 0.0
                with open("chat_costs.log", "r") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            total_historical = entry.get("session_total", 0.0)
                        except:
                            continue
                if total_historical > 0:
                    print(f"Historical total costs: ${total_historical:.6f}")
        except Exception:
            pass
    
    def get_cost_summary(self) -> str:
        """Get formatted cost summary"""
        if self.session_costs.message_count == 0:
            return "No usage yet"
        
        summary = f"""
Cost Summary:
This session: ${self.session_costs.session_cost:.6f}
Total tokens: {self.session_costs.total_tokens:,}
Messages: {self.session_costs.message_count}
Avg per message: ${self.session_costs.cost_per_message:.6f}
Models used: {len(self.session_costs.model_usage)}"""
        
        return summary

def select_model() -> str:
    """Let user select which model to use"""
    print("\nAvailable Models:")
    models = list(MODEL_PRICING.keys())
    
    for i, model in enumerate(models, 1):
        info = MODEL_PRICING[model]
        cost_estimate = (info["input_per_1k"] + info["output_per_1k"]) * 0.1  # Rough estimate for 100 tokens
        print(f"{i}. {info['name']}")
        print(f"   {info['speed']} | ~${cost_estimate:.6f} per 100 tokens")
        print(f"   {info['description']}")
    
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(models)}) or press Enter for fastest: ").strip()
            if not choice:
                return models[0]  # Default to fastest (flash-lite)
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(models):
                return models[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            print("Please enter a valid number")

def chat():
    print("AI Chat with Cost Tracking")
    print("=" * 50)
    
    # Initialize cost tracker
    cost_tracker = CostTracker()
    
    # Let user select model
    selected_model = select_model()
    model_info = MODEL_PRICING[selected_model]
    
    print(f"\nUsing: {model_info['name']}")
    print(f"Speed: {model_info['speed']}")
    print(f"Input: ${model_info['input_per_1k']}/1K tokens | Output: ${model_info['output_per_1k']}/1K tokens")
    print(f"{model_info['description']}")
    
    print("\nCommands: 'quit', 'exit', 'bye' to exit | 'switch' to change model | 'costs' for summary")
    print("=" * 70)
    
    conversation_history = []
    
    try:
        while True:
            try:
                user_message = input("\nYou: ")
                
                # Handle special commands
                if user_message.lower().strip() in ['quit', 'exit', 'bye', 'q']:
                    print(cost_tracker.get_cost_summary())
                    print("\nThanks for chatting! Cost log saved to 'chat_costs.log'")
                    break
                
                if user_message.lower().strip() == 'switch':
                    selected_model = select_model()
                    model_info = MODEL_PRICING[selected_model]
                    print(f"Switched to: {model_info['name']}")
                    continue
                
                if user_message.lower().strip() == 'costs':
                    print(cost_tracker.get_cost_summary())
                    continue
                
                if not user_message.strip():
                    print("Please enter a message, or type 'quit' to exit.")
                    continue
                
                # Add to conversation history
                conversation_history.append({"role": "user", "content": user_message})
                
                # Keep conversation history reasonable
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-20:]
                
                print("AI is thinking...", end="", flush=True)
                
                # Get AI response
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=conversation_history,
                    max_tokens=500,
                    temperature=0.7
                )
                
                ai_message = response.choices[0].message.content
                conversation_history.append({"role": "assistant", "content": ai_message})
                
                # Calculate and track costs
                usage = response.usage
                cost_info = cost_tracker.track_usage(
                    selected_model,
                    usage.prompt_tokens,
                    usage.completion_tokens
                )
                
                # Clear thinking message and show response
                print(f"\rAI: {ai_message}")
                
                # Show cost information
                print(f"   Cost: ${cost_info['request_cost']:.6f} | "
                      f"Session: ${cost_info['session_cost']:.6f} | "
                      f"Tokens: {usage.total_tokens} | "
                      f"Msg #{cost_info['message_count']}")
                
                # Show warnings for high costs
                if cost_info['session_cost'] > 0.01:  # 1 cent
                    print(f"   WARNING: Session cost exceeded $0.01")
                
                if cost_info['request_cost'] > 0.001:  # 0.1 cent per message
                    print(f"   HIGH COST: Message cost ${cost_info['request_cost']:.6f}")
                
            except KeyboardInterrupt:
                print(cost_tracker.get_cost_summary())
                print("\nChat interrupted. Cost log saved!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Continuing chat... (type 'quit' to exit)")
                
    except Exception as e:
        print(f"\nFatal error: {e}")
    
    print(f"\nChat session ended.")
    print(f"Costs logged to: chat_costs.log")

def show_cost_analysis():
    """Analyze historical costs from log file"""
    try:
        if not os.path.exists("chat_costs.log"):
            print("No cost history found. Start chatting to generate data!")
            return
        
        costs_by_model = {}
        total_cost = 0
        total_tokens = 0
        message_count = 0
        
        with open("chat_costs.log", "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    model = entry["model"]
                    cost = entry["cost_usd"]
                    tokens = entry["total_tokens"]
                    
                    if model not in costs_by_model:
                        costs_by_model[model] = {"cost": 0, "tokens": 0, "messages": 0}
                    
                    costs_by_model[model]["cost"] += cost
                    costs_by_model[model]["tokens"] += tokens
                    costs_by_model[model]["messages"] += 1
                    
                    total_cost += cost
                    total_tokens += tokens
                    message_count += 1
                    
                except:
                    continue
        
        print("\nCOST ANALYSIS")
        print("=" * 50)
        print(f"Total spent: ${total_cost:.6f}")
        print(f"Total tokens: {total_tokens:,}")
        print(f"Total messages: {message_count}")
        print(f"Average per message: ${total_cost/message_count:.6f}" if message_count > 0 else "")
        
        print(f"\nCost by Model:")
        for model, stats in costs_by_model.items():
            model_name = MODEL_PRICING.get(model, {}).get("name", model)
            print(f"- {model_name}")
            print(f"  ${stats['cost']:.6f} | {stats['tokens']:,} tokens | {stats['messages']} messages")
        
        # Monthly projection
        if message_count > 0:
            avg_daily = total_cost  # Assuming this is daily usage
            monthly_projection = avg_daily * 30
            print(f"\nMonthly projection: ${monthly_projection:.2f}")
            if monthly_projection > 10:
                print("WARNING: High projected monthly cost!")
        
    except Exception as e:
        print(f"Error analyzing costs: {e}")

def main():
    print("AI Chat with Cost Tracking")
    print("Built for goop proxy: https://github.com/robertprast/goop")
    print("\nOptions:")
    print("1. Start chat")
    print("2. View cost analysis")
    
    choice = input("Choose (1 or 2, Enter for chat): ").strip()
    
    if choice == "2":
        show_cost_analysis()
    else:
        # Test connection first
        try:
            response = client.chat.completions.create(
                model="vertex/gemini-2.0-flash-lite-001",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print("Connection to goop proxy working")
            chat()
        except Exception as e:
            print(f"Cannot connect to goop proxy: {e}")
            print("Make sure goop proxy is running on http://localhost:8080")
            print("Follow setup instructions: https://github.com/robertprast/goop")

if __name__ == "__main__":
    main()
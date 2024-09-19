#this helper class will monitor the LLM for taken usage and estimate the cost

import openai

class LLMUsageMonitor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def estimate_cost(self, model, prompt_tokens, completion_tokens):
        # Estimate cost based on model and token usage
        cost_per_million_prompt_tokens = {
            "gpt-4o": 100,    
        }
        cost_per_million_completion_tokens = {
            "gpt-4o": 300,
        }
        
        prompt_cost = (prompt_tokens / 1_000_000) * cost_per_million_prompt_tokens.get(model, 0)
        completion_cost = (completion_tokens / 1_000_000) * cost_per_million_completion_tokens.get(model, 0)
        
        total_cost = prompt_cost + completion_cost
        return total_cost
    
    def monitor_usage(self, model, prompt_tokens, completion_tokens):
        # Monitor usage and estimate cost
        cost = self.estimate_cost(model, prompt_tokens, completion_tokens)
        print(f"Estimated cost: ${cost:.2f}")

# Example usage
if __name__ == "__main__":
    api_key = "your_openai_api_key"

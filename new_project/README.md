# Advanced AI Model Switching System

🚀 **Intelligent routing between Google Gemini and OpenRouter models with automatic switching, performance monitoring, and fallback mechanisms.**

## Features

- **Automatic Model Selection**: Chooses the best performing model based on response time and success rate
- **Dual Provider Support**: Seamlessly switches between Google Gemini and OpenRouter
- **Performance Monitoring**: Tracks response times, success rates, and error counts for each model
- **Fallback Mechanisms**: Automatically tries alternative models if primary choice fails
- **Provider Preference**: Option to prefer a specific provider when needed
- **Async Support**: Built with asyncio for efficient concurrent requests

## Models Supported

### Google Gemini
- `gemini-1.5-flash` (fast, efficient)
- `gemini-1.5-pro` (balanced performance)
- `gemini-1.0-pro` (standard performance)

### OpenRouter
- `openai/gpt-4o` (powerful OpenAI model)
- `openai/gpt-4o-mini` (cost-effective OpenAI model)
- `anthropic/claude-3.5-sonnet` (Anthropic's advanced model)
- `google/gemini-pro-vision` (Google's multimodal model)
- `mistralai/mistral-7b-instruct` (open-source model)
- `perplexity/pplx-7b-chat` (Perplexity model)
- `cohere/command-r-plus` (Cohere model)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

> **Note**: You can get your Gemini API key from [Google AI Studio](https://aistudio.google.com/) and OpenRouter API key from [OpenRouter](https://openrouter.ai/keys).

## Usage

### Basic Usage

```python
import asyncio
from main import ModelSwitcher

async def main():
    # Initialize the model switcher
    switcher = ModelSwitcher()
    
    # Generate a response with automatic model selection
    response = await switcher.generate_response("Explain quantum computing in simple terms.")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### With Provider Preference

```python
# Prefer a specific provider
response = await switcher.generate_response(
    "Your prompt here",
    preferred_provider="gemini"  # or "openrouter"
)
```

### Performance Statistics

```python
# Get performance statistics for all models
stats = switcher.get_performance_stats()
for model, stat in stats.items():
    print(f"{model}: {stat['success_rate']*100:.1f}% success, "
          f"{stat['avg_response_time']:.3f}s avg time")
```

## How It Works

The system uses an intelligent algorithm to select the best model based on:

1. **Response Time**: Average time taken by each model to respond
2. **Success Rate**: Percentage of successful requests for each model
3. **Error Rate**: Frequency of errors for each model
4. **Availability**: Whether the model's API key is properly configured

The algorithm calculates a performance score for each model: `score = avg_response_time * (1 + error_rate)`, then selects the model with the lowest score (best performance).

## Error Handling & Fallbacks

- If the primary selected model fails, the system automatically tries other available models
- Each model failure is tracked to improve future selection decisions
- The system maintains separate performance metrics for each provider

## Performance Monitoring

The system tracks the following metrics for each model:

- Average response time
- Total requests made
- Success rate
- Error count
- Success count

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is for educational and research purposes. Please use AI models responsibly and in accordance with their respective terms of service. Be mindful of API usage costs and rate limits.
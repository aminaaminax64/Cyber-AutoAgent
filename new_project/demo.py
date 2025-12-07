#!/usr/bin/env python3
"""
Demo script for the Advanced AI Model Switching System
This script demonstrates the functionality without making actual API calls
"""

import asyncio
import os
from main import ModelSwitcher


async def demo_without_api_keys():
    """Demo showing the system when no API keys are configured"""
    print("🚀 Advanced AI Model Switching System - Demo")
    print("=" * 60)
    print("ℹ️  This demo runs without API keys to show the system structure")
    print()
    
    # Initialize the model switcher (without API keys)
    switcher = ModelSwitcher()
    
    print("📋 Available Models:")
    print(f"   Google Gemini: {len(switcher.gemini_models)} models")
    for model in switcher.gemini_models:
        print(f"     - {model}")
    
    print(f"   OpenRouter: {len(switcher.openrouter_models)} models")
    for model in switcher.openrouter_models:
        print(f"     - {model}")
    
    print()
    print("📊 Performance Tracking Setup:")
    print("   - Response time tracking")
    print("   - Success/failure rate monitoring")
    print("   - Automatic model selection algorithm")
    print("   - Fallback mechanisms")
    
    print()
    print("🔄 Model Selection Algorithm:")
    print("   - Considers response time and error rate")
    print("   - Uses performance score: time * (1 + error_rate)")
    print("   - Requires minimum requests before using response time")
    print("   - Supports provider preference")
    
    print()
    print("⚡ Async Support:")
    print("   - Built with asyncio for efficient concurrent requests")
    print("   - Non-blocking API calls")
    print("   - Timeout handling")
    
    print()
    print("🔧 Configuration:")
    print("   - Centralized config.py for easy customization")
    print("   - Environment variable support")
    print("   - Customizable model lists")
    print("   - Adjustable performance parameters")


async def demo_with_mock_api_keys():
    """Demo showing how the system works with API keys set"""
    print("\n" + "=" * 60)
    print("🎯 Demo with Mock API Keys")
    print("=" * 60)
    
    # Temporarily set mock API keys for demonstration
    os.environ["GEMINI_API_KEY"] = "mock-gemini-key"
    os.environ["OPENROUTER_API_KEY"] = "mock-openrouter-key"
    
    # Initialize the model switcher with mock keys
    switcher = ModelSwitcher()
    
    print("📋 Models Available with API Keys:")
    print(f"   Google Gemini: {len(switcher.gemini_models)} models")
    for model in switcher.gemini_models:
        print(f"     - {model}")
    
    print(f"   OpenRouter: {len(switcher.openrouter_models)} models")
    for model in switcher.openrouter_models:
        print(f"     - {model}")
    
    print()
    print("💡 Key Features:")
    print("   • Automatic switching between providers")
    print("   • Performance-based model selection")
    print("   • Intelligent fallback mechanisms")
    print("   • Real-time performance monitoring")
    print("   • Provider preference option")
    print("   • Configurable settings")
    
    # Clean up mock keys
    del os.environ["GEMINI_API_KEY"]
    del os.environ["OPENROUTER_API_KEY"]


def show_usage_example():
    """Show usage examples in the README format"""
    print("\n" + "=" * 60)
    print("📝 Usage Examples")
    print("=" * 60)
    
    example_code = '''
# Basic usage
from main import ModelSwitcher
import asyncio

async def main():
    switcher = ModelSwitcher()
    response = await switcher.generate_response("Your prompt here")
    print(response)

# With provider preference
response = await switcher.generate_response(
    "Your prompt here", 
    preferred_provider="gemini"  # or "openrouter"
)

# Get performance stats
stats = switcher.get_performance_stats()
for model, stat in stats.items():
    print(f"{model}: {stat['success_rate']*100:.1f}% success")
'''
    print(example_code)


def show_benefits():
    """Show the benefits of this system"""
    print("=" * 60)
    print("🌟 Benefits of This System")
    print("=" * 60)
    
    benefits = [
        "🔄 Automatic switching between Google Gemini and OpenRouter",
        "📊 Performance monitoring and optimization",
        "🛡️  Fallback mechanisms for high availability", 
        "⚡ Async support for efficient concurrent requests",
        "⚙️  Highly configurable with centralized settings",
        "📈 Real-time performance metrics tracking",
        "🎯 Intelligent model selection based on success rate and speed",
        "🔄 Load balancing across multiple providers/models",
        "🔒 Environment variable support for API keys",
        "📝 Comprehensive logging and error handling"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")


async def main():
    """Main demo function"""
    await demo_without_api_keys()
    await demo_with_mock_api_keys()
    show_usage_example()
    show_benefits()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("📋 To use with real API keys, set GEMINI_API_KEY and OPENROUTER_API_KEY")
    print("📖 See README.md for complete setup instructions")


if __name__ == "__main__":
    asyncio.run(main())
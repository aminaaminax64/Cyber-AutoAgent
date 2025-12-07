#!/usr/bin/env python3
"""
Example usage of the Advanced AI Model Switching System
"""

import asyncio
from main import ModelSwitcher


async def example_basic_usage():
    """Example of basic usage with automatic model selection"""
    print("=== Basic Usage Example ===")
    
    # Initialize the model switcher
    switcher = ModelSwitcher()
    
    # Test prompt
    prompt = "Explain the benefits of renewable energy in 3 bullet points."
    
    print(f"Input: {prompt}")
    
    # Generate response with automatic model selection
    response = await switcher.generate_response(prompt)
    
    if response:
        print(f"Output: {response}")
    else:
        print("Failed to get response")
    
    print()


async def example_with_provider_preference():
    """Example of using provider preference"""
    print("=== Provider Preference Example ===")
    
    switcher = ModelSwitcher()
    
    prompt = "Write a short poem about technology."
    
    print(f"Input: {prompt}")
    print("Preferred provider: gemini")
    
    # Generate response preferring Gemini
    response = await switcher.generate_response(prompt, preferred_provider="gemini")
    
    if response:
        print(f"Output: {response}")
    else:
        print("Failed to get response")
    
    print()


async def example_performance_stats():
    """Example of checking performance statistics"""
    print("=== Performance Statistics Example ===")
    
    switcher = ModelSwitcher()
    
    # Make a few requests to generate some data
    test_prompts = [
        "What is artificial intelligence?",
        "How does solar power work?",
        "Explain blockchain technology in simple terms."
    ]
    
    for prompt in test_prompts:
        await switcher.generate_response(prompt)
    
    # Get and display performance statistics
    stats = switcher.get_performance_stats()
    
    print("Performance Statistics:")
    for model, stat in stats.items():
        if stat['total_requests'] > 0:  # Only show models that were used
            print(f"  {model}:")
            print(f"    Success Rate: {stat['success_rate']*100:.1f}%")
            print(f"    Avg Response Time: {stat['avg_response_time']:.3f}s")
            print(f"    Total Requests: {stat['total_requests']}")
            print(f"    Errors: {stat['error_count']}")
            print()


async def example_fallback_mechanism():
    """Example demonstrating the fallback mechanism"""
    print("=== Fallback Mechanism Example ===")
    
    switcher = ModelSwitcher()
    
    # Test with a complex prompt
    prompt = "Compare and contrast machine learning and traditional programming approaches. Include at least 5 key differences."
    
    print(f"Input: {prompt}")
    
    response = await switcher.generate_response(prompt)
    
    if response:
        print(f"Output: {response[:200]}...")  # Show first 200 chars
    else:
        print("Failed to get response")
    
    print()


async def run_all_examples():
    """Run all examples sequentially"""
    print("🚀 Advanced AI Model Switching System - Examples")
    print("=" * 60)
    
    await example_basic_usage()
    await example_with_provider_preference()
    await example_performance_stats()
    await example_fallback_mechanism()
    
    print("✅ All examples completed!")


if __name__ == "__main__":
    asyncio.run(run_all_examples())
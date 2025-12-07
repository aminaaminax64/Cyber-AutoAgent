#!/usr/bin/env python3
"""
Advanced AI Model Switching System
==================================
This project provides automatic switching between Google Gemini and OpenRouter models,
with performance monitoring, fallback mechanisms, and intelligent routing based on
model availability and response quality.
"""

import asyncio
import json
import logging
import os
import random
import time
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
import google.generativeai as genai
from dotenv import load_dotenv

from config import (
    DEFAULT_GEMINI_MODELS,
    DEFAULT_OPENROUTER_MODELS,
    OPENROUTER_API_URL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TIMEOUT,
    MAX_RESPONSE_TIMES_TO_TRACK,
    MIN_REQUESTS_FOR_SELECTION
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelSwitcher:
    """
    Intelligent model switching system that automatically routes requests between
    Google Gemini and OpenRouter based on availability, performance, and cost.
    """
    
    def __init__(self):
        # Initialize Google Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_models = DEFAULT_GEMINI_MODELS[:]
        else:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.gemini_models = []
        
        # Initialize OpenRouter
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_models = DEFAULT_OPENROUTER_MODELS[:]
        
        # Performance tracking
        self.response_times = {}
        self.error_counts = {}
        self.success_counts = {}
        
        # Initialize tracking dictionaries
        all_models = self.gemini_models + self.openrouter_models
        for model in all_models:
            self.response_times[model] = []
            self.error_counts[model] = 0
            self.success_counts[model] = 0
    
    async def generate_with_gemini(self, prompt: str, model_name: str = "gemini-1.5-flash") -> Optional[str]:
        """
        Generate response using Google Gemini API
        """
        try:
            start_time = time.time()
            
            model = genai.GenerativeModel(model_name)
            response = await model.generate_content_async(prompt)
            
            response_time = time.time() - start_time
            
            # Update performance metrics
            self.response_times[model_name].append(response_time)
            # Keep only the last N response times to avoid memory issues
            if len(self.response_times[model_name]) > MAX_RESPONSE_TIMES_TO_TRACK:
                self.response_times[model_name] = self.response_times[model_name][-MAX_RESPONSE_TIMES_TO_TRACK:]
            self.success_counts[model_name] += 1
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning(f"Gemini response was empty for model {model_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error with Gemini model {model_name}: {str(e)}")
            self.error_counts[model_name] += 1
            return None
    
    async def generate_with_openrouter(self, prompt: str, model_name: str) -> Optional[str]:
        """
        Generate response using OpenRouter API
        """
        try:
            start_time = time.time()
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": DEFAULT_TEMPERATURE,
                "max_tokens": DEFAULT_MAX_TOKENS
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_time = time.time() - start_time
                        
                        # Update performance metrics
                        self.response_times[model_name].append(response_time)
                        # Keep only the last N response times to avoid memory issues
                        if len(self.response_times[model_name]) > MAX_RESPONSE_TIMES_TO_TRACK:
                            self.response_times[model_name] = self.response_times[model_name][-MAX_RESPONSE_TIMES_TO_TRACK:]
                        self.success_counts[model_name] += 1
                        
                        return result['choices'][0]['message']['content'].strip()
                    else:
                        logger.error(f"OpenRouter API error {response.status}: {await response.text()}")
                        self.error_counts[model_name] += 1
                        return None
                        
        except Exception as e:
            logger.error(f"Error with OpenRouter model {model_name}: {str(e)}")
            self.error_counts[model_name] += 1
            return None
    
    def get_best_model(self, preferred_provider: str = None) -> Tuple[str, str]:
        """
        Select the best model based on performance metrics and availability
        Returns (model_name, provider)
        """
        available_models = []
        
        # Add available Gemini models
        if self.gemini_api_key:
            for model in self.gemini_models:
                # Only consider response time if we have enough requests for this model
                if len(self.response_times.get(model, [])) >= MIN_REQUESTS_FOR_SELECTION:
                    avg_response_time = sum(self.response_times.get(model, [])) / len(self.response_times.get(model, [1])) if self.response_times.get(model) else float('inf')
                else:
                    # If not enough requests, use a default value to not bias early selections
                    avg_response_time = 1.0  # 1 second default
                
                error_rate = self.error_counts.get(model, 0) / max(1, self.success_counts.get(model, 0) + self.error_counts.get(model, 0))
                
                # Score based on response time and error rate
                score = avg_response_time * (1 + error_rate)
                available_models.append((model, 'gemini', score))
        
        # Add available OpenRouter models
        if self.openrouter_api_key:
            for model in self.openrouter_models:
                # Only consider response time if we have enough requests for this model
                if len(self.response_times.get(model, [])) >= MIN_REQUESTS_FOR_SELECTION:
                    avg_response_time = sum(self.response_times.get(model, [])) / len(self.response_times.get(model, [1])) if self.response_times.get(model) else float('inf')
                else:
                    # If not enough requests, use a default value to not bias early selections
                    avg_response_time = 1.0  # 1 second default
                
                error_rate = self.error_counts.get(model, 0) / max(1, self.success_counts.get(model, 0) + self.error_counts.get(model, 0))
                
                # Score based on response time and error rate
                score = avg_response_time * (1 + error_rate)
                available_models.append((model, 'openrouter', score))
        
        if not available_models:
            raise ValueError("No models available - check API keys")
        
        # Sort by score (lower is better)
        available_models.sort(key=lambda x: x[2])
        
        # If preferred provider is specified, prioritize models from that provider
        if preferred_provider:
            preferred_models = [m for m in available_models if m[1] == preferred_provider]
            if preferred_models:
                return preferred_models[0][0], preferred_models[0][1]
        
        # Return the best overall model
        best_model, provider, _ = available_models[0]
        return best_model, provider
    
    async def generate_response(self, prompt: str, preferred_provider: str = None) -> Optional[str]:
        """
        Main method to generate a response, automatically selecting the best available model
        """
        try:
            # Get the best model based on performance metrics
            model_name, provider = self.get_best_model(preferred_provider)
            
            logger.info(f"Using {provider} model: {model_name}")
            
            if provider == 'gemini':
                return await self.generate_with_gemini(prompt, model_name)
            elif provider == 'openrouter':
                return await self.generate_with_openrouter(prompt, model_name)
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            # Fallback: try another available model
            return await self.fallback_generation(prompt)
    
    async def fallback_generation(self, prompt: str) -> Optional[str]:
        """
        Fallback method to try other models if primary fails
        """
        logger.info("Trying fallback models...")
        
        # Get all available models sorted by performance
        all_models = []
        if self.gemini_api_key:
            for model in self.gemini_models:
                all_models.append((model, 'gemini'))
        if self.openrouter_api_key:
            for model in self.openrouter_models:
                all_models.append((model, 'openrouter'))
        
        # Shuffle to try different models randomly as fallback
        random.shuffle(all_models)
        
        for model_name, provider in all_models:
            logger.info(f"Trying fallback: {provider} - {model_name}")
            
            try:
                if provider == 'gemini':
                    result = await self.generate_with_gemini(prompt, model_name)
                elif provider == 'openrouter':
                    result = await self.generate_with_openrouter(prompt, model_name)
                
                if result:
                    logger.info(f"Fallback successful with {provider} - {model_name}")
                    return result
            except Exception as e:
                logger.error(f"Fallback failed for {provider} - {model_name}: {str(e)}")
                continue
        
        logger.error("All fallback attempts failed")
        return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for all models
        """
        stats = {}
        
        for model in self.gemini_models + self.openrouter_models:
            responses = self.response_times.get(model, [])
            avg_time = sum(responses) / len(responses) if responses else 0
            total_requests = self.success_counts.get(model, 0) + self.error_counts.get(model, 0)
            success_rate = self.success_counts.get(model, 0) / total_requests if total_requests > 0 else 0
            
            stats[model] = {
                'avg_response_time': round(avg_time, 3),
                'total_requests': total_requests,
                'success_rate': round(success_rate, 3),
                'error_count': self.error_counts.get(model, 0),
                'success_count': self.success_counts.get(model, 0)
            }
        
        return stats


async def main():
    """
    Main function demonstrating the model switching system
    """
    print("🚀 Starting Advanced AI Model Switching System")
    print("=" * 50)
    
    # Initialize the model switcher
    switcher = ModelSwitcher()
    
    # Test prompts
    test_prompts = [
        "Explain quantum computing in simple terms.",
        "Write a creative story about a robot learning to paint.",
        "What are the latest developments in renewable energy?",
        "How does machine learning differ from traditional programming?"
    ]
    
    print("\n📊 Performance Statistics (before testing):")
    stats = switcher.get_performance_stats()
    for model, stat in stats.items():
        print(f"  {model}: {stat['success_rate']*100:.1f}% success, "
              f"{stat['avg_response_time']:.3f}s avg time")
    
    print(f"\n🧪 Testing with {len(test_prompts)} different prompts:")
    print("-" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nPrompt {i}: {prompt[:50]}...")
        
        # Generate response with automatic model selection
        response = await switcher.generate_response(prompt)
        
        if response:
            print(f"✅ Response: {response[:100]}...")
        else:
            print("❌ Failed to get response")
    
    print(f"\n📊 Performance Statistics (after testing):")
    stats = switcher.get_performance_stats()
    for model, stat in stats.items():
        if stat['total_requests'] > 0:  # Only show models that were used
            print(f"  {model}: {stat['success_rate']*100:.1f}% success, "
                  f"{stat['avg_response_time']:.3f}s avg time, "
                  f"{stat['total_requests']} reqs")


if __name__ == "__main__":
    asyncio.run(main())
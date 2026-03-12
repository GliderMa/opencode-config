#!/usr/bin/env python3
import sys
import os
from pathlib import Path

skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

from model_routing import load_provider_config

print("=== Testing environment variable support ===\n")

print("Test 1: Load from config file (no env var)")
try:
    provider = load_provider_config("volcengine-plan")
    print(f"  baseUrl: {provider['baseUrl']}")
    masked_key = provider['apiKey'][:20] + "..." if len(provider['apiKey']) > 20 else provider['apiKey']
    print(f"  apiKey: {masked_key}")
    print("  Status: SUCCESS")
except Exception as e:
    print(f"  Error: {e}")

print("\nTest 2: Load from environment variable")
os.environ["VOLCENGINE_PLAN_API_KEY"] = "test-key-from-environment"
try:
    provider = load_provider_config("volcengine-plan")
    print(f"  baseUrl: {provider['baseUrl']}")
    print(f"  apiKey: {provider['apiKey']}")
    print("  Status: SUCCESS")
    if provider['apiKey'] == "test-key-from-environment":
        print("  Environment variable priority: CORRECT")
    else:
        print("  Environment variable priority: FAILED")
except Exception as e:
    print(f"  Error: {e}")

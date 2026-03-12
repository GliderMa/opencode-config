#!/usr/bin/env python3
import json
import sys
from pathlib import Path

skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

import requests
from model_routing import load_model_routing, load_provider_config, normalize_model_spec

PROVIDER_TIMEOUT = 30

def test_model_with_response_format(provider, model_spec, use_response_format):
    model = model_spec['model']
    url = f"{provider['baseUrl']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {provider['apiKey']}",
        "Content-Type": "application/json",
    }
    temperature = model_spec.get('temperature', 0.4)
    thinking = model_spec.get('thinking')

    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个测试助手。只输出JSON。"
            },
            {"role": "user", "content": "请输出JSON: {\"status\":\"ok\"}"},
        ],
        "temperature": temperature,
    }
    if use_response_format:
        body["response_format"] = {"type": "json_object"}
    if thinking is not None:
        body["thinking"] = {"type": "enabled" if thinking else "disabled"}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=PROVIDER_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return True, content[:50], None
    except Exception as e:
        return False, None, str(e)[:200]

def main():
    data = load_model_routing()
    print("=== 测试 response_format 支持 ===\n")

    for capability_name, capability in data.get("capabilities", {}).items():
        print(f"[{capability_name}]")
        provider_name = capability.get('provider')
        provider = load_provider_config(provider_name)

        for slot_name in ['primary', 'secondary', 'tertiary']:
            slot_value = capability.get(slot_name)
            if not slot_value or isinstance(slot_value, str):
                continue

            model_spec = normalize_model_spec(slot_value)
            model = model_spec['model']

            success_with_rf, _, error_with_rf = test_model_with_response_format(provider, model_spec, True)
            success_without_rf, _, _ = test_model_with_response_format(provider, model_spec, False)

            if success_with_rf:
                print(f"   {model}: supportsResponseFormat = true")
            elif success_without_rf:
                print(f"   {model}: supportsResponseFormat = false (不支持JSON格式)")
            else:
                print(f"   {model}: 失败 (错误: {error_with_rf[:50]})")

if __name__ == "__main__":
    main()

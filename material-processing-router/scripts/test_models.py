#!/usr/bin/env python3
import json
import sys
from pathlib import Path

skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))

import requests
from model_routing import load_model_routing, resolve_task_route, load_provider_config, normalize_model_spec

PROVIDER_TIMEOUT = 30

def test_model(provider, model_spec):
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
                "content": "你是一个测试助手。"
            },
            {"role": "user", "content": "请回复：测试成功"},
        ],
        "temperature": temperature,
    }
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
    print("=== 测试所有配置的模型 ===\n")

    for capability_name, capability in data.get("capabilities", {}).items():
        print(f"[能力] {capability_name}")
        print(f"   Provider: {capability.get('provider')}")

        for slot_name in ['primary', 'secondary', 'tertiary']:
            slot_value = capability.get(slot_name)
            if not slot_value:
                continue

            if isinstance(slot_value, str):
                print(f"   {slot_name}: {slot_value} (字符串引用，跳过测试)")
                continue

            model_spec = normalize_model_spec(slot_value)
            provider_name = capability.get('provider')

            try:
                provider = load_provider_config(provider_name)
                success, content, error = test_model(provider, model_spec)

                if success:
                    print(f"   [OK] {slot_name}: {model_spec['model']} - 成功")
                    print(f"      响应: {content}")
                else:
                    print(f"   [FAIL] {slot_name}: {model_spec['model']} - 失败")
                    print(f"      错误: {error}")
            except Exception as e:
                print(f"   [WARN] {slot_name}: {model_spec['model']} - 配置错误")
                print(f"      错误: {str(e)[:200]}")
        print()

if __name__ == "__main__":
    main()

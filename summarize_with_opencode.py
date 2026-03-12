#!/usr/bin/env python3
"""
使用OpenCode配置的模型总结文件内容
"""

import requests
import json
import sys
import os

VOLCENGINE_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions"
API_KEY = "API_KEY"
MODEL = "glm-4.7"

def summarize_file(file_path: str, max_chars: int = 100) -> str:
    """
    使用LLM总结文件内容

    Args:
        file_path: 文件路径
        max_chars: 最大字数限制

    Returns:
        总结后的文本
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""请总结以下文件内容，要求：
1. 总结不超过{max_chars}个中文字符
2. 准确概括核心内容
3. 简洁明了

文件内容：
{content}

总结："""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    response = requests.post(VOLCENGINE_BASE_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    result = response.json()
    summary = result["choices"][0]["message"]["content"].strip()

    if len(summary) > max_chars:
        summary = summary[:max_chars] + "..."

    return summary


if __name__ == "__main__":
    default_file = "AI_Project/数据及算法.md"
    file_path = sys.argv[1] if len(sys.argv) > 1 else default_file

    try:
        summary = summarize_file(file_path, max_chars=100)
        print("文件总结（100字以内）：")
        print(summary)
        print(f"\n实际字数：{len(summary)}")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

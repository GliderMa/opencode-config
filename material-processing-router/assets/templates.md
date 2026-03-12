# Configuration Templates

## model-routing.json Template

```json
{
  "capabilities": {
    "longform-analysis": {
      "provider": "volcengine-plan",
      "primary": {
        "model": "deepseek-v3.2",
        "supportsResponseFormat": true,
        "thinking": true,
        "temperature": 0.3
      },
      "secondary": {
        "model": "glm-4.7",
        "supportsResponseFormat": true,
        "thinking": true,
        "temperature": 0.3
      },
      "tertiary": "openclaw:main",
      "fallback": "rule"
    },
    "concise-summarization": {
      "provider": "volcengine-plan",
      "primary": {
        "model": "kimi-k2.5",
        "supportsResponseFormat": true,
        "thinking": false,
        "temperature": 0.4
      },
      "secondary": {
        "model": "deepseek-v3.2",
        "supportsResponseFormat": true,
        "thinking": false,
        "temperature": 0.4
      },
      "fallback": "rule"
    },
    "information-review": {
      "provider": "volcengine-plan",
      "primary": {
        "model": "kimi-k2.5",
        "supportsResponseFormat": true,
        "thinking": false,
        "temperature": 0.2
      },
      "secondary": {
        "model": "doubao-seed-2.0-lite",
        "supportsResponseFormat": false,
        "thinking": false,
        "temperature": 0.2
      },
      "fallback": "rule"
    }
  },
  "tasks": {
    "daily-diary": {
      "capability": "concise-summarization"
    },
    "bloomberg-weekly": {
      "capability": "longform-analysis",
      "reviewCapability": "information-review"
    }
  }
}
```

## model.json Provider Configuration Template

**Method 1: JSON configuration file**

```json
{
  "models": {
    "providers": {
      "volcengine-plan": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/coding/v3",
        "apiKey": "YOUR_API_KEY_HERE",
        "api": "openai"
      }
    }
  }
}
```

**Method 2: Environment variables (recommended)**

```bash
# Format: <PROVIDER_NAME_UPPERCASE>_API_KEY
export VOLCENGINE_PLAN_API_KEY="your-actual-api-key"
```

**Priority order:**
1. Environment variables (highest priority)
2. Configuration file values (fallback)

## Setup Instructions

1. Place `model-routing.json` in `shared/automation/`
2. Choose API key method:
   - Environment variable (recommended for security)
   - JSON configuration file
3. Test models using scripts in `scripts/`

## Using Skill's model_routing.py

The skill includes its own `scripts/model_routing.py` which can be used:

```python
import sys
from pathlib import Path

skill_dir = Path("/path/to/skill") / "scripts"
sys.path.insert(0, str(skill_dir))

from model_routing import resolve_task_route, load_provider_config
```

Or use your workspace version if it exists.

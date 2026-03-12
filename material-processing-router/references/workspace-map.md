# Workspace Map

## Shared routing layer

- `shared/automation/model-routing.json` - capability and task definitions
- `shared/automation/model_routing.py` - routing loader functions (optional, skill provides its own)

## Provider configuration

### Method 1: Environment variables (recommended)
```bash
export VOLCENGINE_PLAN_API_KEY="your-api-key"
```

### Method 2: Configuration file
- `model.json` - provider configuration at workspace root
- Contains API keys (less secure than environment variables)

**Priority order:**
1. Environment variables (highest priority)
2. Configuration file values (fallback)

## Current tasks using pattern

### Daily Diary Generation
- Task file: `shared/automation/generate_daily_diary.py`
- Nature: concise summarization / rewrite
- Current routing source: `model-routing.json`
- Capability: `concise-summarization`

## Test utilities

Test models and configuration:
- Model availability: `python scripts/test_models.py`
- Response format support: `python scripts/test_response_format.py`
- Environment variable support: `python scripts/test_env_var.py`

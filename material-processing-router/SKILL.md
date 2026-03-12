---
name: material-processing-router
description: Route material-processing and information-analysis tasks through the right LLM path instead of defaulting to the main agent. Use when a task has explicit input material and explicit output shape—such as summarization, longform analysis, extraction, rewriting, tagging, weekly reports, daily diaries, or structured note generation—and you need to choose a capability profile, select primary/secondary/main-agent/rule fallbacks, configure model behavior (response_format support, thinking, temperature), or update task-to-model routing without hardcoding model names inside task scripts.
---

Use this skill when the job is primarily a material-in → result-out transformation.

## Core workflow

1. Decide whether the task is a material-processing task
2. Map the task to a **capability** instead of directly naming a model
3. Let the capability define:
   - Primary model path
   - Backup model path
   - Optional main-agent fallback
   - Final rule fallback
   - Call behavior (supportsResponseFormat, thinking, temperature)
4. Keep version trace in outputs
5. Test with a probe before switching production flows

## What counts as material-processing

- Email/newsletter/communication summarization
- Weekly or daily report generation
- Longform analysis
- Concise summarization
- Structured extraction
- Tagging/classification
- Rewriting source material into a target style

Do **not** use this skill when the task mainly depends on long-lived conversation context, identity continuity, or repeated tool interaction.

## Design rules

- Prefer **capability-level routing** over hardcoded model names
- Keep architecture stable even if models change
- Put model-specific quirks in config when possible
- Always keep a fallback chain
- Preserve output validation and attempt trace

## Setup

### Configuration files

Place these files in your workspace:

1. `shared/automation/model-routing.json` - capability and task definitions
2. `shared/automation/model_routing.py` - routing loader functions (optional, skill provides its own)
3. `model.json` - provider configuration (optional, see environment variables below)

### Environment variables (recommended)

For API key security, use environment variables instead of configuration files:

```bash
# Format: <PROVIDER_NAME_UPPERCASE>_API_KEY
export VOLCENGINE_PLAN_API_KEY="your-api-key-here"

# Run your task
python shared/automation/generate_daily_diary.py
```

**Priority order:**
1. Environment variables (highest priority)
2. Configuration file values (fallback)

See [assets/templates.md](assets/templates.md) for configuration templates.

## Task integration

Import and use routing in your task scripts:

```python
import sys
from pathlib import Path

# Add skill scripts to path (if using skill's model_routing.py)
skill_dir = Path("/path/to/skill") / "scripts"
sys.path.insert(0, str(skill_dir))

from model_routing import resolve_task_route, load_provider_config

route = resolve_task_route("daily-diary")
provider = load_provider_config(route["provider"])
model_spec = route["primary"]
```

## Model management

Use `scripts/routectl.py` to inspect and update routing:

- Show task: `python scripts/routectl.py show <task>`
- Set primary: `python scripts/routectl.py set <task> primary <model> --thinking true --supports-response-format false --temperature 0.3`
- Reset slot: `python scripts/routectl.py reset <task> <slot>`

## Testing

Before production use, test model compatibility:

- Model availability: `python scripts/test_models.py`
- Response format support: `python scripts/test_response_format.py`

See [references/testing.md](references/testing.md) for detailed testing guidance.

## References

- **Architecture and principles**: [references/architecture.md](references/architecture.md)
- **Model compatibility**: [references/models.md](references/models.md)
- **Testing guide**: [references/testing.md](references/testing.md)
- **Migration checklist**: [references/migration-checklist.md](references/migration-checklist.md)

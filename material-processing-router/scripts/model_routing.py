import json
import os
from pathlib import Path


def load_model_routing():
    paths = [
        Path.cwd() / "shared" / "automation" / "model-routing.json",
    ]
    for path in paths:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise ValueError("model-routing.json not found in workspace")


def resolve_task_route(task_name: str):
    data = load_model_routing()
    tasks = data.get("tasks", {})
    route = tasks.get(task_name)
    if not route:
        raise ValueError(f"task route not found: {task_name}")

    capability_name = route.get("capability")
    if not capability_name:
        return route

    capability = data.get("capabilities", {}).get(capability_name)
    if not capability:
        raise ValueError(f"capability not found: {capability_name}")

    merged = dict(capability)
    merged.update(route)
    merged["capability_name"] = capability_name
    return merged


def load_provider_config(provider_name: str):
    config_paths = [
        Path.cwd() / "model.json",
    ]
    
    data = None
    for path in config_paths:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            break
    
    if not data:
        raise ValueError(f"provider config file not found for: {provider_name}")
    
    provider = data.get("models", {}).get("providers", {}).get(provider_name, {})
    if not provider:
        raise ValueError(f"provider not found: {provider_name}")
    
    base_url = provider.get("baseUrl")
    
    env_var_name = provider_name.replace("-", "_").upper() + "_API_KEY"
    api_key = os.environ.get(env_var_name, provider.get("apiKey"))
    
    if not base_url or not api_key:
        raise ValueError(f"provider config incomplete: {provider_name}")
    
    return {
        "name": provider_name,
        "baseUrl": base_url.rstrip("/"),
        "apiKey": api_key,
        "api": provider.get("api"),
    }


def normalize_model_spec(spec):
    if spec is None:
        return None
    if isinstance(spec, str):
        return {"model": spec}
    if isinstance(spec, dict):
        return spec
    raise ValueError(f"invalid model spec: {spec}")

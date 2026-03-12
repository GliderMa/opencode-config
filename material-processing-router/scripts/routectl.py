#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROUTING_PATH = Path.cwd() / 'shared' / 'automation' / 'model-routing.json'


def load_data():
    return json.loads(ROUTING_PATH.read_text(encoding='utf-8'))


def save_data(data):
    ROUTING_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def resolve_task(data, task_name):
    task = data.get('tasks', {}).get(task_name)
    if not task:
        raise SystemExit(f'task not found: {task_name}')
    capability_name = task.get('capability')
    capability = data.get('capabilities', {}).get(capability_name, {}) if capability_name else {}
    merged = dict(capability)
    merged.update(task)
    merged['capability_name'] = capability_name
    return merged


def ensure_capability(data, capability_name):
    caps = data.setdefault('capabilities', {})
    cap = caps.get(capability_name)
    if not cap:
        raise SystemExit(f'capability not found: {capability_name}')
    return cap


def normalize_model_spec(model, thinking=None, supports_response_format=None, temperature=None):
    spec = {'model': model}
    if thinking is not None:
        spec['thinking'] = thinking
    if supports_response_format is not None:
        spec['supportsResponseFormat'] = supports_response_format
    if temperature is not None:
        spec['temperature'] = temperature
    return spec


def parse_optional_args(args):
    out = {}
    i = 0
    while i < len(args):
        key = args[i]
        if key == '--thinking':
            out['thinking'] = args[i + 1].lower() == 'true'
            i += 2
        elif key == '--supports-response-format':
            out['supports_response_format'] = args[i + 1].lower() == 'true'
            i += 2
        elif key == '--temperature':
            out['temperature'] = float(args[i + 1])
            i += 2
        else:
            raise SystemExit(f'unknown arg: {key}')
    return out


def cmd_show(task_name):
    data = load_data()
    print(json.dumps(resolve_task(data, task_name), ensure_ascii=False, indent=2))


def cmd_set(task_name, slot, model, extra):
    data = load_data()
    task = data.get('tasks', {}).get(task_name)
    if not task:
        raise SystemExit(f'task not found: {task_name}')
    capability_name = task.get('capability')
    if slot in ('primary', 'secondary'):
        cap = ensure_capability(data, capability_name)
        cap[slot] = normalize_model_spec(model, **extra)
    elif slot == 'tertiary':
        cap = ensure_capability(data, capability_name)
        cap[slot] = model
    else:
        raise SystemExit(f'unsupported slot: {slot}')
    save_data(data)
    print(json.dumps({'status': 'ok', 'task': task_name, 'slot': slot, 'model': model}, ensure_ascii=False))


def cmd_reset(task_name, slot):
    data = load_data()
    task = data.get('tasks', {}).get(task_name)
    if not task:
        raise SystemExit(f'task not found: {task_name}')
    capability_name = task.get('capability')
    cap = ensure_capability(data, capability_name)
    if slot in cap:
        del cap[slot]
    save_data(data)
    print(json.dumps({'status': 'ok', 'task': task_name, 'slot': slot, 'action': 'removed'}, ensure_ascii=False))


def main(argv):
    if len(argv) < 3:
        raise SystemExit('usage: routectl.py show <task> | set <task> <slot> <model> [--thinking true|false] [--supports-response-format true|false] [--temperature n] | reset <task> <slot>')
    cmd = argv[1]
    if cmd == 'show':
        cmd_show(argv[2])
    elif cmd == 'set':
        if len(argv) < 5:
            raise SystemExit('usage: routectl.py set <task> <slot> <model> [options]')
        extra = parse_optional_args(argv[5:])
        cmd_set(argv[2], argv[3], argv[4], extra)
    elif cmd == 'reset':
        if len(argv) < 4:
            raise SystemExit('usage: routectl.py reset <task> <slot>')
        cmd_reset(argv[2], argv[3])
    else:
        raise SystemExit(f'unknown command: {cmd}')


if __name__ == '__main__':
    main(sys.argv)

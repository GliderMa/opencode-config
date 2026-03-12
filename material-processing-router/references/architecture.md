# Architecture

## Goal

Separate **task type**, **capability type**, and **model choice**.

Instead of writing model names inside each task script, use this stack:

1. Task
2. Capability
3. Model path(s)
4. Fallback chain
5. Output validation + trace

## Stable principle

What should remain stable over time is:
- dedicated model path first
- backup model path second
- optional main-agent fallback later
- rule fallback last

What may change over time is:
- which concrete models serve each role
- whether a model supports `response_format`
- whether a model benefits from `thinking`
- temperature and other call options

## Capability examples

### longform-analysis
Use for:
- newsletter analysis
- long document synthesis
- event evolution summaries
- multi-source thematic reporting

Typical needs:
- stronger structure
- better handling of long inputs
- optional thinking
- model compatibility rules

### concise-summarization
Use for:
- short diaries
- compact summaries
- rewrite-and-compress tasks
- single-document condensation

Typical needs:
- natural language generation
- controlled length
- less need for long reasoning chains

### information-review
Use for:
- content review
- quality checks
- structured validation

Typical needs:
- high accuracy
- lower temperature
- consistent output format

## Fallback design

Recommended order:
1. primary dedicated model
2. secondary dedicated model
3. optional main agent
4. rule fallback

Not every task needs all four levels.

## Output requirements

Outputs should record:
- `summary_mode` or `summary_version`
- `attempt_trace`
- `fallback_reason` when relevant

## Compatibility knobs

Useful per-model settings include:
- `supportsResponseFormat`
- `thinking`
- `temperature`

These should live in config, not in ad-hoc branches spread across task scripts.

## Testing requirements

Before production use:
1. Test model availability
2. Test `response_format` support
3. Verify fallback chain works
4. Validate output structure

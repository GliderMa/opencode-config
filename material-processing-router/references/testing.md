# Testing Guide

## Model Availability Testing

Test whether configured models are accessible and respond correctly:

```bash
python scripts/test_models.py
```

This tests all models in `model-routing.json` with a simple request.

## Response Format Testing

Check which models support `response_format` for structured JSON output:

```bash
python scripts/test_response_format.py
```

This tests both with and without `response_format` parameter to determine support.

## Probe Before Production

Always run probes before switching production flows:

1. Test model availability
2. Verify `response_format` support
3. Check fallback chain behavior
4. Validate output structure

## Expected Test Results

When tests pass, you should see:
- `[OK]` for successful models
- `[FAIL]` with error details for failed models
- Clear indication of `response_format` support status

## Troubleshooting

- **400 Bad Request**: Model may not support `response_format`
- **404 Not Found**: Model name incorrect or not available
- **Connection errors**: Network or API key issues

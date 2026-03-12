# Model Compatibility

## Volcengine Provider Testing Results

### Models Supporting `response_format` (JSON output)

The following models support structured JSON output via `response_format`:

- **ark-code-latest** - ✅ Supports
- **kimi-k2.5** - ✅ Supports
- **glm-4.7** - ✅ Supports
- **minimax-m2.5** - ✅ Supports
- **deepseek-v3.2** - ✅ Supports

### Models NOT Supporting `response_format`

The following models do NOT support structured JSON output:

- **doubao-seed-2.0-code** - ❌ Not supported
- **doubao-seed-2.0-lite** - ❌ Not supported
- **doubao-seed-2.0-pro** - ❌ Not supported

### Important Notes

- Always test model compatibility before production use
- `response_format` support is critical for tasks requiring structured output
- Configure `supportsResponseFormat: false` for non-supporting models in routing config
- Models may change support over time, retest periodically

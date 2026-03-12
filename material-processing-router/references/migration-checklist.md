# Migration Checklist

Use this checklist when moving a new task into the material-processing router.

1. Confirm the task is material-in/result-out and does not primarily need long-lived agent context.
2. Define the expected output shape.
3. Add validation rules.
4. Decide whether the task maps to an existing capability or needs a new one.
5. Add/adjust routing in `shared/automation/model-routing.json`.
6. Ensure model compatibility knobs are declared in config.
7. Keep a fallback chain.
8. Add or reuse a probe script.
9. Run probe validation before switching production flow.
10. Ensure production output records version and trace.

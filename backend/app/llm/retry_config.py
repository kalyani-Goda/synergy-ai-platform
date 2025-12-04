from google.genai import types

# Standard retry configuration for Gemini
retry_config = types.HttpRetryOptions(
    attempts=5,
    initial_delay=1.0,
    max_delay=60.0,
    exp_base=7.0,
    http_status_codes=[503],
)
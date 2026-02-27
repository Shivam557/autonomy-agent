# Prompt Architecture & Safety (Day 1)

- **Location of prompt logic:** `core/draft_service.py`
- **Template store:** `core/templates.json`
- **Adapter interface:** `llm/adapter.py` (production adapters must implement `LLMAdapter.generate`)
- **Sanitization:** strip HTML, remove "ignore previous instructions", truncate `reason` to 800 chars
- **Validation rules:** word count 60–220 words, must contain single explicit ask (regex), must end with confirmation deadline, must not contain banned keywords (lawsuit, sue, court, legal action)
- **Output requirement:** return `{ "body": "...", "preview": "...", "valid": bool, "errors": [] }`

Version templates required: `template_name`, `version`, `prompt`, `max_tokens`, `temperature`.
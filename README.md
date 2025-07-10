A [pre-commit](https://pre-commit.com/) hook that sends the git diff to a LLM, so that it performs a code review on it.

## Usage with ollama

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v1.1.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=ollama"
        - "--ollama_base_url=https://llm.dodges.it"
        - "--model=mistral-small3.2:latest"
```

## Usage with Gemini

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v1.1.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=gemini"
        - "--model=gemini-2.5-flash"
        - "--api_key=YOUR_API_KEY_HERE"
```

## Options

| Option            | Description                           |
| ----------------- | ------------------------------------- |
| --llm             | Either 'ollama' or 'gemini'           |
| --ollama_base_url | The URL of the Ollama server to query |
| --model           | The name of the model to use          |
| --api_key         | Only for Gemini. The API key to use   |
| --debug           | Extra logging for debugging purposes  |

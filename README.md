# README.md

A [pre-commit](https://pre-commit.com/) hook that sends the git diff to a LLM,
so that it performs a code review on it.

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

## Usage with Mistral

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v1.1.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=mistral"
        - "--model=mistral-small"
        - "--api_key=YOUR_API_KEY_HERE"
```

## Options

| Option            | Description                           |
| ----------------- | ------------------------------------- |
| --llm             | 'ollama', 'gemini' or 'mistral'       |
| --ollama_base_url | The URL of the Ollama server to query |
| --model           | The name of the model to use          |
| --api_key         | The API key to use Gemini or Mistral  |
| --debug           | Extra logging for debugging purposes  |
| --temperature     | Inference temperature, [0.0 - 2.0]    |

## Note about context

This hook sends the output of `git diff "HEAD^" "HEAD"` to a LLM
and prompts it to perform a code review on it.

First, this diff can be large. If you are using Gemini, you probably have a
[rate-limit](https://ai.google.dev/gemini-api/docs/rate-limits) in place
that prevents you from sending too many tokens per minute.

Second, only the diff is sent to a LLM, not the whole file. As a result,
the LLM has limited context to work with. This can however be tweaked
by changing [GIT_DIFF_OPTS](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
to include more context lines in the output of `git diff`.

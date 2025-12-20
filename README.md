# README.md

Two [pre-commit](https://pre-commit.com/) hooks:

- `llm-code-review`: sends the git diff to a LLM, so that it performs a code review on it.
- `llm-commit-message`: sends the git diff to a LLM, so that it can suggest a git commit message

## LLM Code Review

The hook can be executed at two different [stages](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages): pre-commit, or pre-merge-commit.

### Usage with ollama

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v2.0.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=ollama"
        - "--ollama_base_url=https://llm.dodges.it"
        - "--model=mistral-small3.2:latest"
```

### Usage with Gemini

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v2.0.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=gemini"
        - "--model=gemini-2.5-flash"
        - "--api_key=YOUR_API_KEY_HERE"
```

### Usage with Mistral

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v2.0.0
  hooks:
    - id: llm-code-review
      args:
        - "--llm=mistral"
        - "--model=mistral-small"
        - "--api_key=YOUR_API_KEY_HERE"
```

### Options

| Option            | Description                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| --llm             | 'ollama', 'gemini' or 'mistral'                                                                                 |
| --ollama_base_url | The URL of the Ollama server to query                                                                           |
| --model           | The name of the model to use                                                                                    |
| --api_key         | The API key to use Gemini or Mistral. This overrides environment variables (GEMINI_API_KEY or MISTRAL_API_KEY). |
| --debug           | Extra logging for debugging purposes                                                                            |
| --temperature     | Inference temperature, [0.0 - 2.0]                                                                              |
| --retries         | How many times LLM should be queried                                                                            |
| --stage           | Either 'pre-commit' (default) or 'pre-merge-commit'                                                             |

### Note about context

This hook sends the output of `git diff --cached` to a LLM
and prompts it to perform a code review on it.

First, this diff can be large. If you are using Gemini, you probably have a
[rate-limit](https://ai.google.dev/gemini-api/docs/rate-limits) in place
that prevents you from sending too many tokens per minute.

Second, only the diff is sent to a LLM, not the whole file. As a result,
the LLM has limited context to work with. This can however be tweaked
by changing [GIT_DIFF_OPTS](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
to include more context lines in the output of `git diff`.

## LLM Commit Message

The hook must be executed at stage `prepare-commit-msg`

### Usage with ollama

```yaml
- repo: https://github.com/qdii/pre-commit-llm-code-review
  rev: v2.0.0
  stages: ["prepare-commit-msg"]
  hooks:
    - id: llm-commit-message
      args:
        - "--llm=ollama"
        - "--ollama_base_url=https://llm.dodges.it"
        - "--model=mistral-small3.2:latest"
```

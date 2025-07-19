# Changelog

## Unreleased

### Added

- Add support to run the code review at merge time (pre-merge-commit)
- Consider environment variables for API key if --api_key is not set

## v1.3.2 (2025-07-13)

### Added

- Add requirements.txt compiled from requirements.in
- Add missing dependency httpx in requirements.in

## v1.3.1 (2025-07-13)

### Changed

- Fix bug where --model was ignored for Mistral

## v1.3.0 (2025-07-13)

### Added

- Support for Mistral AI
- New parameter --retries controls how many times LLM should be queried

### Changed

- Use `git diff --cached` instead of `git diff HEAD^ HEAD`

## v1.2.0 (2025-07-10)

### Added

- New parameter --timeout specifies deadline when querying LLM
- New parameter --temperature controls inference temperature

## v1.1.0 (2025-07-10)

### Added

- Initial version with support for Ollama and Gemini

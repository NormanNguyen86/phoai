# 0002 — Use YAML config with secrets in .env

- **Date:** 2026-11-17
- **Status:** accepted
- **Version:** v0.1

## Context
The API key cannot be committed to version control, and a setting must live in one place only. The project runs on Windows first, then Docker/CI in a later version.

## Options considered
| Option | Pros | Cons |
|---|---|---|
| YAML for configuration, .env only for secrets | Secrets in .env file won't be committed, while YAML file can be shared | Need another file for each environment |
| Set priority: .env > YAML > default | Flexible environment-specific overrides | Need to define and maintain the priority order or effective configuration |
| Environment variables only | Simple and straightforward | Environment variables are not public and can not be committed. |

## Decision
I choose the first option: YAML for configuration, .env only for secrets at the moment. As the project is at an early stage, keep the configuration simple and clear.

## Consequences
- .env.example contains only secrets; environment variables do not override YAML values. 
- every variable in .env.example must be read by code in src/.
- Per-environment configuration uses a separate YAML file.
- If v0.5 (Docker, CI, Hugging Face Spaces) needs to override the configuration, there is another ADR that replaces this ADR.

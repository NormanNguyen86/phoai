# 0001 — Use uv for package and environment management

- **Date:** 2026-11-14
- **Status:** accepted
- **Version:** v0.1

## Context
PhoAI must be reproducible: anyone (a reviewer, or me on another machine) should be able to
recreate the exact environment and get the same behaviour. That needs a declared list of
dependencies plus a lock file with exact versions. Constraints: Python <3.12 / 3.13>, a single
part-time developer, development on Windows, and the same environment must later run in
Docker and CI (v0.5). Runtime dependencies (e.g. pydantic, anthropic) should be kept separate
from development tools (pytest, ruff).

## Options considered
| Option | Pros | Cons |
|---|---|---|
| uv | `uv add` records every dependency in `pyproject.toml` and pins exact versions in `uv.lock`; `uv sync` recreates the environment from the lock file; separates runtime and dev dependencies; very fast | Newer tool, so less familiar to some teams; must be installed separately (also in CI/Docker); `uv pip install` bypasses `pyproject.toml` and is easy to misuse |
| pip + venv + requirements.txt | Built into Python; familiar and easy for beginners | `pip install` records nothing; `pip freeze` must be run by hand and the file can drift from the real environment; no built-in split between runtime and dev dependencies |

## Decision
Use uv, because it records every dependency and locks exact versions, so the environment can be rebuilt with one command (`uv sync`), whether I change machines or someone else wants to run
the project.

## Consequences
- `uv.lock` must be committed whenever dependencies change.
- Every new dependency must be classified: runtime (`uv add`, e.g. pydantic) or development only (`uv add --dev`, e.g. pytest, ruff → `[dependency-groups]`).
- Dependencies are added with `uv add`, never `pip install` or `uv pip install`.
- CI and the Dockerfile (v0.5) must install uv before installing the project.
- Revisit if uv cannot be used in a target deployment environment, or if the project has to
  join a team standardised on another tool.
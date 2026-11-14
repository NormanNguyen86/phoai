# PhoAI — AI Photography Tutor

**Photo critique for beginners where every comment points to evidence on the photo.**

> 🚧 Status: building **v0.1** (CLI critique → validated JSON). See [docs/STATUS.md](docs/STATUS.md).

## Why

Beginner photographers struggle to judge their own photos. Community feedback is inconsistent,
and current AI tools return a paragraph or a score without showing *where* in the photo the
comment comes from, so the advice is hard to understand and act on.

PhoAI returns a structured critique — **Observation → Evidence → Why → What to try** — where
*Evidence* is tied to a region of the image (box/mask) and checked automatically (from v0.3).

## How it works (planned)

```
photo ──► MLLM (versioned prompt) ──► JSON critique (pydantic schema)
                                          │
                                          ▼
                         grounding: evidence phrase → box / mask      (v0.3)
                                          │
                                          ▼
                         verification: is the evidence really there?  (v0.3)
                                          │
                                          ▼
                 output + prompt_version, model_id, schema_version, git_sha
```

## Roadmap

| Version | Theme | Status |
|---|---|---|
| v0.1 | Critique runs on 5 photos, outputs validated JSON | 🚧 in progress |
| v0.2 | Evaluation harness, first measured results | planned |
| v0.3 | Grounding + evidence verification | planned |
| v0.5 | Public demo (Gradio on Hugging Face Spaces), Docker, CI | planned |
| v0.8 | Backend service (FastAPI, PostgreSQL) | planned |

## Quickstart

> Available from v0.1.0.

```bash
uv sync                                   # install dependencies (https://docs.astral.sh/uv/)
cp .env.example .env                      # add your API key
uv run python -m phoai.pipeline photo.jpg # critique one photo
uv run pytest -m "not slow"               # tests (no real API calls)
```

## Results

No results yet. From v0.2, every number here links to a report in `evals/reports/`.

## Engineering practices

This repo is also a record of how the project is run:

- [Project management handbook](docs/PROJECT_MANAGEMENT.md) — versioning, git workflow, release checklist
- [Specs per version](docs/spec-versions/) — scope and definition of done, frozen up front
- [Architecture decision records](docs/adr/) — why each tool and design was chosen
- [JD analysis](docs/jd-analysis.md) — which AI Engineer skills each version demonstrates

## Tech stack
Python 3.13 · uv · pydantic · pytest · ruff — more added per version (see specs).

## Author

Built by Norman Nguyen (Master of AI, UTS). Core modules are written by the author;
AI assistance is used for review and explanation — see the [AI assistance policy](docs/PROJECT_MANAGEMENT.md#96-ai-assisted-development-policy).

## License

[MIT](LICENSE)

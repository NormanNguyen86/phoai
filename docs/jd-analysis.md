# JD analysis — AI Engineer (Australia) → skills PhoAI must prove

Every skill employers commonly ask for should have **one concrete piece of evidence in this repo**
(a file, PR, evaluation report or release tag). This table decides what PhoAI builds and what goes on the CV.

Updated: 2026-11-13 · Review when new JDs are added and before every release.

## How to use
1. Save graduate / junior AI Engineer, ML Engineer and Applied AI job ads in "JD sources" below.
2. For each JD, tick the skills it asks for and update the **JDs** column.
3. Skills many JDs ask for with no evidence yet get priority in the next spec
   (still one theme per version — handbook §6).

## Skills

| # | Area | Skill | JDs | Proven in | Evidence (fill when done) | Status |
|---|---|---|---|---|---|---|
| 1 | Foundations | Clean Python: type hints, package layout, pyproject/uv | | v0.1 | `src/phoai/`, `pyproject.toml` | ⬜ |
| 2 | Foundations | Git workflow: branches, PRs, Conventional Commits, SemVer tags | | v0.1 | PR history, tag `v0.1.0` | ⬜ |
| 3 | LLM | Calling LLM/MLLM APIs with image input | | v0.1 | `critique.py` | ⬜ |
| 4 | LLM | Structured output + validation (pydantic, retry on invalid JSON) | | v0.1 | `schema.py`, `docs/schema.md` | ⬜ |
| 5 | LLM | Versioned prompt engineering with a changelog | | v0.1–v0.2 | `prompts/`, `prompts/CHANGELOG.md` | ⬜ |
| 6 | Evaluation | Evaluation harness, fixed metrics, baseline comparison | | v0.2 | `evals/run.py`, `evals/reports/v0.2.md` | ⬜ |
| 7 | Evaluation | Agreement with human labels (precision/recall, stability) | | v0.2–v0.3 | `evals/human_labels/` | ⬜ |
| 8 | Quality | Unit tests with mocked APIs, pytest, pre-commit, ruff | | v0.2 | `tests/`, `.pre-commit-config.yaml` | ⬜ |
| 9 | Quality | Reproducibility: versioned runs, YAML config, JSON logs | | v0.1–v0.3 | `runs/<run_id>/`, `config/` | ⬜ |
| 10 | CV / multimodal | Grounding: phrase → box/mask (detector/segmenter) | | v0.3 | `grounding.py` | ⬜ |
| 11 | Reliability | Output verification, reducing hallucination | | v0.3 | `verify.py`, image-shuffle report | ⬜ |
| 12 | Operations | Cost/latency tracking, rate limits, caching | | v0.2–v0.5 | `log.jsonl`, cost-per-image report | ⬜ |
| 13 | Deployment | Web demo (Gradio) on Hugging Face Spaces with secrets | | v0.5 | demo link | ⬜ |
| 14 | MLOps | Docker (multi-stage, .dockerignore) | | v0.5 | `Dockerfile` | ⬜ |
| 15 | MLOps | CI/CD with GitHub Actions (lint, test, build) | | v0.5 | `.github/workflows/ci.yml` | ⬜ |
| 16 | Backend | REST API (FastAPI) | | v0.8 | `api/` | ⬜ |
| 17 | Backend | PostgreSQL + migrations (Alembic), pgvector if needed | | v0.8 | `migrations/` | ⬜ |
| 18 | Backend | Observability: Sentry, health checks, tracing (Langfuse) | | v0.8 | dashboard / screenshot | ⬜ |
| 19 | Communication | Technical docs: README, ADRs, devlog | | every version | `README.md`, `docs/adr/` | ⬜ |

Status: ⬜ not started · 🟨 in progress · ✅ evidence exists

## Common JD skills PhoAI does NOT cover (for interview answers)

| Skill | Why not in PhoAI | Covered elsewhere? |
|---|---|---|
| Fine-tuning / training large models | Out of scope for v0.x; uses existing models + evaluation | |
| RAG / vector search | No real product need yet | |
| Large cloud platforms (AWS/GCP/Azure) | HF Spaces → VPS is enough at this scale | |

## JD sources

| # | Saved | Company | Role | Link / file | Key skills |
|---|---|---|---|---|---|
| 1 | | | | | |

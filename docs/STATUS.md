# Status

_Last updated: 2026-11-19 · Overwritten at each status check; history lives in [devlog.md](devlog.md)._

## Current version
**v0.1 — Critique runs on 5 photos** · due 2026-11-22 · spec: [spec-v0.1](spec-versions/spec-v0.1.md)

## Definition of done
| # | Item | State | Evidence |
|---|---|---|---|
| 1 | 5/5 test photos produce schema-valid JSON | ⬜ | Test set in [test-photos.md](test-photos.md); `critique.py` not written yet |
| 2 | Outputs record `prompt_version`, `model_id`, `schema_version` | ⬜ | Fields defined in [schema.md](schema.md) (`RunRecord`); code pending |
| 3 | Unit tests pass without the real API | 🟨 | `tests/test_pipeline.py` (6 pass); schema/critique tests pending |
| 4 | No secrets / raw images / `runs/` committed | 🟨 | `.gitignore` covers `.env`, `data/raw/`, `runs/`; none tracked on 2026-11-19; re-check at release |
| 5 | README explains how to run v0.1 | ⬜ | |
| 6 | ADRs for every row in spec "Tech introduced" | 🟨 | 2/4: 0001 (uv), 0002 (YAML + .env). Left: 0003 pydantic, 0004 Anthropic SDK |
| 7 | Tagged `v0.1.0` with a GitHub Release | ⬜ | |

⬜ not started · 🟨 in progress · ✅ done

## Next tasks (max 3)
1. Get an API key and credit; run one test photo through the API and log `usage.output_tokens`; record the image-input decision (upright PNG made offline, no rotation in the pipeline) in ADR 0004.
2. `schema.py` + `tests/test_schema.py` matching `docs/schema.md`; ADR 0003 (pydantic).
3. `critique.py`: call the model, strip a whole-output code fence, parse, validate, retry (plain retry, no error feedback); `max_tokens` is a separate error; mocked tests; ADR 0004.

## Milestones to due date
| Date | Milestone |
|---|---|
| 2026-11-19 | Schema doc, prompt v1 + changelog merged; ADR 0003 drafted |
| 2026-11-20 | API key and credit ready; `schema.py` + schema tests pass; ADR 0003 |
| 2026-11-21 | `critique.py` + mocked tests; ADR 0004; `pipeline.py` writes `runs/<run_id>/`; 5 photos run; README run section |
| 2026-11-22 | Release checklist passed; `v0.1.0` tagged |

## Blockers / risks
- Three working days left for schema, critique, pipeline, 5-photo run, README and two ADRs. If `critique.py` is not done by the evening of 2026-11-21, decide: move the tag (write the reason in the devlog) or release with DoD 1 not met and say so. Never cut tests or ADRs.
- Need an Anthropic API key and credit (was due 2026-11-18).
- `max_tokens: 2000` may be tight for 2 problems and 2 strengths; log `usage.output_tokens` on the first run.

## Backlog (out of scope for this version)
- Caching, cost limits, eval harness (v0.2)
- RAW image support (convert before sending to the API)
- Auto-orient arbitrary uploads in the pipeline (`ImageOps.exif_transpose`) and move `preprocess.py` into the repo so the test set can be rebuilt (v0.2); in v0.1 the input is an upright PNG made offline
- Validate image content (not only extension), e.g. with Pillow
- Pytest `slow` marker (add with the first e2e test)
- Pass shooting settings (ISO, shutter, aperture) to the model; needed to score the `iso_too_high_for_light` label of `02a`
- Put the photo measurement script in the repo so the numbers in `docs/test-photos.md` can be regenerated (v0.2)
- Use the a/b photo pairs as a comparison set with known answers (v0.2)
- Eval check: flag `what_to_try` text that states a camera setting's current value or says it was wrong (v0.2)
- Send validation errors back to the model on retry; tune prompt and retry after v0.1
- Author fills "None recorded" intents and confirms section 9 of `docs/test-photos.md` before v0.2
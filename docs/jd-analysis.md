# Phân tích JD — AI Engineer (Úc) → kỹ năng PhoAI phải chứng minh

Mục đích: mỗi kỹ năng nhà tuyển dụng hay đòi hỏi phải có **một bằng chứng cụ thể trong repo này**
(file, PR, báo cáo eval, tag release). Bảng này quyết định PhoAI xây gì và kể gì trên CV.

Cập nhật: 12/11/2026 · Rà lại mỗi khi lưu thêm JD mới và trước mỗi release.

## Cách dùng
1. Lưu JD (graduate / junior AI Engineer, ML Engineer, Applied AI) vào bảng "Nguồn JD" bên dưới.
2. Với mỗi JD, đánh dấu kỹ năng nó yêu cầu → cập nhật cột **Số JD**.
3. Kỹ năng nhiều JD đòi nhưng cột **Bằng chứng** còn trống → ưu tiên ở milestone kế tiếp
   (nhưng vẫn theo luật "mỗi phiên bản một chủ đề", sổ tay mục 6).

## Bảng kỹ năng

| # | Nhóm | Kỹ năng | Số JD | PhoAI chứng minh ở | Bằng chứng (điền khi xong) | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | Nền tảng | Python sạch: type hints, cấu trúc package, pyproject/uv | | v0.1 | `src/phoai/`, `pyproject.toml` | ⬜ |
| 2 | Nền tảng | Git workflow: nhánh, PR, Conventional Commits, SemVer tag | | v0.1 | lịch sử PR, tag `v0.1.0` | ⬜ |
| 3 | LLM | Gọi API LLM/MLLM, xử lý ảnh đầu vào | | v0.1 | `critique.py` | ⬜ |
| 4 | LLM | Structured output + validate (pydantic, retry khi JSON lỗi) | | v0.1 | `schema.py`, `docs/schema.md` | ⬜ |
| 5 | LLM | Prompt engineering có version + CHANGELOG | | v0.1–v0.2 | `prompts/`, `prompts/CHANGELOG.md` | ⬜ |
| 6 | Eval | Eval harness, chỉ số cố định, so baseline | | v0.2 | `evals/run.py`, `evals/reports/v0.2.md` | ⬜ |
| 7 | Eval | Đối chiếu với nhãn người (precision/recall, độ ổn định) | | v0.2–v0.3 | `evals/human_labels/` | ⬜ |
| 8 | Chất lượng | Unit test có mock API, pytest, pre-commit, ruff | | v0.2 | `tests/`, `.pre-commit-config.yaml` | ⬜ |
| 9 | Chất lượng | Tái lập kết quả: run có version, config YAML, log JSON | | v0.1–v0.3 | `runs/<run_id>/`, `config/` | ⬜ |
| 10 | CV / Multimodal | Grounding: phrase → box/mask (detector/segmenter) | | v0.3 | `grounding.py` | ⬜ |
| 11 | Độ tin cậy | Kiểm chứng output, giảm hallucination | | v0.3 | `verify.py`, báo cáo image-shuffle | ⬜ |
| 12 | Vận hành | Theo dõi chi phí/độ trễ, giới hạn gọi API, cache | | v0.2–v0.5 | `log.jsonl`, báo cáo chi phí/ảnh | ⬜ |
| 13 | Deploy | Demo web (Gradio) + Hugging Face Spaces + Secrets | | v0.5 | link demo | ⬜ |
| 14 | MLOps | Docker (multi-stage, .dockerignore) | | v0.5 | `Dockerfile` | ⬜ |
| 15 | MLOps | CI/CD GitHub Actions (lint, test, build) | | v0.5 | `.github/workflows/ci.yml` | ⬜ |
| 16 | Backend | REST API (FastAPI) | | v0.8 | `api/` | ⬜ |
| 17 | Backend | PostgreSQL + migration (Alembic), (pgvector nếu cần) | | v0.8 | `migrations/` | ⬜ |
| 18 | Backend | Observability: Sentry, healthcheck, tracing (Langfuse) | | v0.8 | dashboard/screenshot | ⬜ |
| 19 | Giao tiếp | Tài liệu kỹ thuật: README, ADR, devlog | | mọi bản | `README.md`, `docs/adr/` | ⬜ |
| 20 | Nghiên cứu | Đọc paper, thiết kế thí nghiệm, nghiên cứu người dùng | | song song (proposal v3) | báo cáo nghiên cứu | ⬜ |

Trạng thái: ⬜ chưa làm · 🟨 đang làm · ✅ có bằng chứng

## Kỹ năng hay gặp trong JD nhưng PhoAI KHÔNG làm (ghi để trả lời phỏng vấn)

| Kỹ năng | Lý do không làm trong PhoAI | Bù bằng gì (nếu cần) |
|---|---|---|
| Fine-tuning / training model lớn | Ngoài phạm vi v0.x; dùng model có sẵn + eval | (điền) |
| RAG / vector search | Chưa có nhu cầu thật trong sản phẩm | (điền) |
| Cloud lớn (AWS/GCP/Azure) | HF Spaces → VPS là đủ cho quy mô này | (điền) |

## Nguồn JD

| # | Ngày lưu | Công ty | Vị trí | Link / file | Kỹ năng nổi bật |
|---|---|---|---|---|---|
| 1 | | | | | |

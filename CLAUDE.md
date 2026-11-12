# PhoAI — AI Photography Tutor

## Mục tiêu
Critique ảnh cho người mới chụp, mỗi nhận xét có bằng chứng trên ảnh
(Observation → Evidence → Why → What to try). Dự án portfolio AI Engineer:
mục tiêu là sản phẩm chạy được VÀ tôi hiểu từng module.

## Trạng thái hiện tại  (cập nhật mỗi tối CN)
- Đang làm: v0.1 (hạn 22/11) — critique chạy trên 5 ảnh, in JSON. Milestone "v0.1" trên GitHub Issues.
- Repo mới khởi tạo: mới có README, .gitignore, .env.example, docs/. Chưa có code.
- Prompt hiện tại: chưa có (sẽ là prompts/critique_v1.md) · model: sẽ ghi trong config/default.yaml

## Cấu trúc thư mục (đích đến; tạo dần theo phiên bản)
- `src/phoai/`  — critique.py, schema.py (pydantic), grounding.py, verify.py, pipeline.py
- `prompts/`    — critique_vN.md + CHANGELOG.md (không xoá bản cũ)
- `config/`     — default.yaml (model_id, temperature, đường dẫn; KHÔNG có secret)
- `evals/`      — run.py, human_labels/, reports/
- `tests/`      — unit test mock API; tests/fixtures/; test_e2e.py đánh dấu `slow`
- `data/`       — README.md, manifest.csv, annotations.csv; `data/raw/` không commit
- `runs/`, `cache/` — output mỗi lần chạy, không commit
- `notebooks/`  — thử nghiệm, không import vào src/
- `docs/`       — sổ tay, spec, schema, adr/, devlog.md, jd-analysis.md
Chi tiết: docs/SO_TAY_QUAN_LY_PHOAI.md mục 3 (chỉ đọc khi cần — file dài)

## Lệnh
- Cài đặt: `uv sync`
- Chạy: `uv run python -m phoai.pipeline <ảnh>`
- Test: `uv run pytest -m "not slow"`
- Eval (từ v0.2): `uv run python -m evals.run --run runs/<run_id>`
- Format: `uv run ruff format . && uv run ruff check .`

## Luật số 1: tôi tự viết trước – hỏi sau
- Tôi là người học. Module lõi (schema, critique, grounding, verify, evals) TÔI tự viết;
  bạn review, giải thích, đặt câu hỏi. Không viết thay phần lõi trừ khi tôi nói rõ.
- Khi tôi hỏi về phần lõi mà chưa đưa kế hoạch/pseudo-code/giả thuyết: hỏi lại
  "Bạn định làm thế nào?" trước, rồi mới góp ý trên bản của tôi.
- Khi tôi kẹt lỗi: tôi sẽ gửi kèm 1 dòng giả thuyết. Nhận xét giả thuyết đó đúng/sai
  trước, gợi ý hướng; chỉ đưa code sửa khi tôi yêu cầu.
- Đừng viết lại toàn bộ file khi tôi chỉ hỏi. Gợi ý từng đoạn nhỏ.
- Phần phụ (boilerplate, Dockerfile, CI, script vẽ biểu đồ) bạn có thể viết, tôi review.
- Sau mỗi thay đổi: giải thích từng thay đổi và vì sao.

## Quy ước
- Python 3.12, type hints, pydantic cho mọi dữ liệu đi ra/vào model
- Prompt nằm trong prompts/, KHÔNG viết cứng trong code
- Mỗi output lưu kèm prompt_version, model_id, schema_version, git_sha
- Test không gọi API thật — dùng fixture trong tests/fixtures/
- Commit theo Conventional Commits (feat/fix/prompt/eval/docs/test/chore); một commit một ý
- Nhánh ngắn: feat/…, fix/…, prompt/…, docs/…; vào main chỉ qua PR
- Trước khi sửa > 2 file: nêu kế hoạch và chờ tôi đồng ý
- Khi sửa lỗi: nói nguyên nhân gốc trong 1 câu
- Ý tưởng ngoài chủ đề phiên bản hiện tại → ghi Backlog, không làm chen

## Không bao giờ
- Đọc hay in nội dung .env
- Commit data/raw/, runs/, cache/, model weights
- Tự push, tự tag
- Thêm dependency mới mà không hỏi

## Tài liệu
- Sổ tay quản lý: docs/SO_TAY_QUAN_LY_PHOAI.md (đọc mục liên quan khi cần, không đọc cả file)
- Phân tích JD / kỹ năng mục tiêu: docs/jd-analysis.md
- (sắp có) Spec: docs/spec-v0.1.md · Schema: docs/schema.md · ADR: docs/adr/ · Nhật ký: docs/devlog.md

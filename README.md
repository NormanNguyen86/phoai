# PhoAI — AI Photography Tutor

> Nhận xét ảnh cho người mới chụp, **mỗi nhận xét đều chỉ ra bằng chứng trên ảnh**.
> Trạng thái: 🚧 đang xây v0.1 (hạn 22/11/2026).

## Vấn đề

Người mới chụp ảnh khó tự đánh giá ảnh của mình. Góp ý từ cộng đồng thường không nhất quán,
còn các công cụ AI hiện có chỉ trả về đoạn văn hoặc điểm số, không chỉ ra *chỗ nào* trên ảnh
dẫn đến nhận xét đó. Người học vì vậy khó hiểu và khó áp dụng góp ý.

PhoAI tạo critique theo cấu trúc **Observation → Evidence → Why → What to try**,
trong đó *Evidence* được gắn với một vùng cụ thể trên ảnh (box/mask) và được kiểm chứng.

## Kiến trúc (dự kiến)

```
ảnh ──► MLLM (prompt có version) ──► JSON critique (pydantic schema)
                                         │
                                         ▼
                          grounding: evidence_phrase → box/mask   (v0.3)
                                         │
                                         ▼
                          verify: kiểm chứng bằng chứng          (v0.3)
                                         │
                                         ▼
                          output + prompt_version, model_id, schema_version, git_sha
```

| Phiên bản | Hạn | Chủ đề |
|---|---|---|
| v0.1 | 22/11/2026 | Critique chạy trên 5 ảnh, in JSON |
| v0.2 | 04/12/2026 | Có số liệu đầu tiên (eval harness) |
| v0.3 | 18/12/2026 | Grounding + tự kiểm chứng |
| v0.5 | 03/01/2027 | Demo online (Gradio, HF Spaces) |
| v0.8 | sau kỳ nghỉ | Backend (FastAPI, PostgreSQL) |

Chi tiết: [docs/SO_TAY_QUAN_LY_PHOAI.md](docs/SO_TAY_QUAN_LY_PHOAI.md).

## Cách chạy

> Các lệnh dưới đây sẽ dùng được khi có `pyproject.toml` (v0.1).

```bash
# 1. Cài uv: https://docs.astral.sh/uv/
uv sync

# 2. Cấu hình biến môi trường
cp .env.example .env      # rồi điền API key vào .env

# 3. Chạy critique trên một ảnh
uv run python -m phoai.pipeline path/to/photo.jpg

# 4. Test (không gọi API thật)
uv run pytest -m "not slow"
```

## Kết quả

_Chưa có. Từ v0.2, mọi con số đều lấy từ `evals/reports/`._

## Demo

_Sẽ có ở v0.5 (Hugging Face Spaces)._

## Cấu trúc thư mục

Xem mục 3 của [sổ tay quản lý](docs/SO_TAY_QUAN_LY_PHOAI.md#3-cấu-trúc-repo).

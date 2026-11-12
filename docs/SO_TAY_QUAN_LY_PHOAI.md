# Sổ tay quản lý dự án PhoAI

> Đọc lại file này mỗi **tối thứ 7 lúc tổng kết tuần**, và mỗi khi chuẩn bị **tag một release**.
> Ở file kế hoạch, các dòng `🛠 Quản lý:` và `🤖 Claude:` trong cột "Việc cần làm" đều dẫn về các mục của sổ tay này.

Cập nhật lần cuối: 12/11/2026 · Áp dụng cho giai đoạn v0.1 → v0.5 (11/2026 – 01/2027) và chuẩn bị v0.8.

---

## Mục lục

1. Nguyên tắc chung
2. PhoAI lớn dần qua từng phiên bản
3. Cấu trúc repo
4. Git: nhánh, commit, PR, tag
5. Phiên bản và checklist release
6. Giới hạn phạm vi mỗi phiên bản
7. Dữ liệu, prompt, eval: phần riêng của sản phẩm AI
8. Docker, database, CI/CD, môi trường deploy
9. Quản lý Claude trong dự án
10. Mẫu sẵn (CLAUDE.md, SKILL.md, PR template, CHANGELOG, devlog)
11. Nhịp quản lý hằng ngày / hằng tuần / mỗi release

---

## 1. Nguyên tắc chung

1. **Mọi thứ đều nằm trong git**, trừ secrets, dữ liệu lớn và model weights. Server chỉ chạy những gì đã có trong git, không sửa tay trên server.
2. **Prompt là code.** Prompt phải có version, có CHANGELOG, và mỗi lần đổi đều phải được kiểm tra bằng eval.
3. **Mỗi thay đổi đều nhỏ.** Một PR làm một việc, một release có một chủ đề.
4. **Có số liệu thì mới nói là tốt hơn.** Mỗi release có báo cáo eval so với bản trước.
5. **Chậm thì cắt phạm vi**, không cắt giấc ngủ (giống luật 3 trong kế hoạch Norman).
6. **Mình hiểu từng module.** Claude giúp tăng tốc, không viết thay phần mình phải hiểu (xem mục 9).

---

## 2. PhoAI lớn dần qua từng phiên bản

Không xây cả hệ thống ngay từ đầu. Mỗi phiên bản chỉ thêm những thứ thật sự cần:

| Phiên bản | Hạn | Chủ đề | Thêm hạ tầng gì |
|---|---|---|---|
| v0.1 | 22/11 | Critique chạy trên 5 ảnh, in JSON | Repo, `.env`, `pyproject.toml`, config YAML, log |
| v0.2 | 04/12 | Có số liệu đầu tiên | `evals/` (eval harness), pytest, pre-commit, cache |
| v0.3 | 18/12 | Grounding + tự kiểm chứng | Lưu run có version, feature flag, smoke test |
| v0.5 | 03/01 | Demo online | Gradio, HF Spaces + Secrets, giới hạn chi phí, Docker, GitHub Actions |
| v0.8 | sau kỳ nghỉ | Sản phẩm có backend | FastAPI, PostgreSQL, Docker Compose, staging/prod |

Đây cũng là câu chuyện để kể khi phỏng vấn: *"Tôi thêm hạ tầng khi có lý do, không thêm vì trend."*

---

## 3. Cấu trúc repo

```
phoai/
├── CLAUDE.md               # bộ nhớ dự án cho Claude (mục 9)
├── README.md               # vấn đề, kiến trúc, cách chạy, kết quả, link demo
├── CHANGELOG.md            # lịch sử phiên bản
├── pyproject.toml          # dependency + version của dự án (quản lý bằng uv)
├── .env.example            # danh sách biến môi trường, KHÔNG có giá trị thật
├── .gitignore              # .env, data/raw/, runs/, cache/, __pycache__/
├── config/
│   └── default.yaml        # model_id, temperature, đường dẫn... (không có secret)
├── prompts/
│   ├── critique_v1.md
│   ├── critique_v2.md
│   └── CHANGELOG.md        # prompt đổi gì, vì lỗi nào
├── src/phoai/
│   ├── critique.py         # ảnh → model → JSON đã kiểm tra
│   ├── schema.py           # pydantic model (hợp đồng dữ liệu)
│   ├── grounding.py        # evidence_phrase → box/mask
│   ├── verify.py           # module kiểm chứng bằng chứng
│   └── pipeline.py         # 1 lệnh chạy toàn bộ
├── evals/
│   ├── run.py              # python -m evals.run
│   ├── human_labels/       # nhãn chấm tay (commit)
│   └── reports/            # v0.2.md, v0.3.md, model-comparison.md
├── tests/                  # unit test (mock API) + test_e2e.py (slow)
├── data/
│   ├── README.md           # nguồn, license, số lượng, định dạng, quy ước tên
│   ├── manifest.csv        # danh sách ảnh + sha256
│   ├── annotations.csv     # commit được (text nhỏ)
│   └── raw/                # ảnh thật — KHÔNG commit, sao lưu OneDrive
├── runs/                   # output mỗi lần chạy — KHÔNG commit
├── notebooks/              # thử nghiệm, không trộn vào src/
├── docs/
│   ├── SO_TAY_QUAN_LY_PHOAI.md   # file này
│   ├── spec-v0.1.md
│   ├── jd-analysis.md
│   ├── schema.md
│   ├── annotation-guide.md
│   ├── failure-cases.md / failure-taxonomy.md
│   ├── devlog.md           # nhật ký dự án, 1 đoạn/tuần
│   ├── adr/                # 0001-tech-stack.md, 0002-..., quyết định kỹ thuật
│   └── img/                # ảnh dùng cho README
├── app.py                  # Gradio (v0.5) — chỉ gọi pipeline
├── Dockerfile / .dockerignore      # v0.5
├── .github/
│   ├── workflows/ci.yml            # v0.5
│   └── pull_request_template.md
└── .claude/
    ├── settings.json       # quyền của Claude (chặn đọc .env...)
    └── skills/             # skill riêng của dự án (mục 9.4)
```

---

## 4. Git: nhánh, commit, PR, tag

### 4.1 Nhánh

- `main`: luôn chạy được và được bảo vệ (Settings → Branches → bật *Require a pull request before merging*; từ v0.5 bật thêm *Require status checks*).
- Mỗi việc một nhánh ngắn, sống vài ngày:
  - `feat/critique-cli`, `feat/grounding`, `feat/gradio-ui`
  - `fix/json-retry`
  - `prompt/v2`
  - `docs/readme-v05`
- Merge xong thì xoá nhánh.

### 4.2 Commit theo Conventional Commits

```
feat: thêm critique.py đọc ảnh và lưu JSON
fix: retry khi model trả JSON lỗi (Fixes #7)
prompt: v2 yêu cầu evidence_phrase cụ thể hơn
eval: thêm precision/recall theo dimension
docs: README cách chạy v0.1
test: unit test cho schema
chore: cập nhật .gitignore
```

Mỗi commit chỉ chứa một ý. Khi viết `Fixes #số-issue`, GitHub tự đóng issue lúc merge.

### 4.3 Pull Request khi làm một mình

Vẫn mở PR, vì PR là nơi để:
1. Đọc lại toàn bộ diff một lần trước khi merge (bắt được rất nhiều lỗi ngớ ngẩn).
2. Điền checklist trong PR template (mục 10.3).
3. Từ v0.5, chờ CI chạy xanh.

### 4.4 Tag và Release

```bash
git tag -a v0.1.0 -m "v0.1.0: critique chạy trên 5 ảnh"
git push origin v0.1.0
```
Sau đó tạo GitHub Release từ tag và dán mục CHANGELOG tương ứng vào.

### 4.5 Những thứ không bao giờ commit

`.env`, API key, ảnh trong `data/raw/`, `runs/`, `cache/`, model weights, file `.ipynb_checkpoints`.
Lỡ commit API key thì **thu hồi key ngay** trên trang nhà cung cấp. Xoá khỏi git là không đủ, vì key vẫn còn trong lịch sử.

---

## 5. Phiên bản và checklist release

### 5.1 Semantic Versioning `MAJOR.MINOR.PATCH`

- `0.x.y`: sản phẩm chưa ổn định (toàn bộ giai đoạn này).
- Tăng **MINOR** (`0.2.0 → 0.3.0`) khi có tính năng mới, tăng **PATCH** (`0.3.0 → 0.3.1`) khi chỉ sửa lỗi.
- Ngoài version của code, PhoAI có thêm 3 thứ cần version riêng:
  - `prompt_version` (`critique_v2`)
  - `model_id` (tên model chính xác)
  - `schema_version` (cấu trúc JSON output)

  Cả ba được **lưu kèm mỗi kết quả**, nhờ vậy khi có lỗi luôn truy ngược được nguyên nhân.

### 5.2 Checklist release (copy vào PR release)

**Code và cấu hình**
- [ ] `version` trong `pyproject.toml` đã tăng
- [ ] `.env.example` có đủ biến mới
- [ ] Dependency đã pin và file lock được cập nhật
- [ ] (từ v0.8) Migration DB đã chạy thử trên staging

**Phần AI**
- [ ] `prompts/CHANGELOG.md` cập nhật nếu đổi prompt
- [ ] Đã chạy eval: `evals/reports/vX.Y.md` có bảng so sánh với bản trước
- [ ] Đã ghi chi phí/ảnh và độ trễ trung bình

**Tài liệu**
- [ ] `CHANGELOG.md` có mục `[X.Y.0]` (Added / Changed / Fixed / Removed)
- [ ] README cập nhật (cách chạy, kết quả, link demo)
- [ ] ADR mới nếu có quyết định kiến trúc

**Phát hành**
- [ ] Đã chạy smoke test (3 ảnh end-to-end)
- [ ] Biết rõ cách rollback (tag trước là gì)
- [ ] `git tag vX.Y.0` + GitHub Release
- [ ] Đóng Milestone hiện tại, tạo Milestone tiếp theo (≤ 8 issue)
- [ ] Cập nhật file Thành tựu (PHO-xx)

---

## 6. Giới hạn phạm vi mỗi phiên bản

Lỗi lớn nhất của dự án cá nhân là **phạm vi cứ phình mãi**. Các luật sau dùng để chặn điều đó:

1. **Mỗi phiên bản một chủ đề** (bảng ở mục 2). Ý tưởng không thuộc chủ đề thì ghi vào Backlog, không làm chen.
2. **Một Milestone tối đa 8 issue.** Đủ 8 thì khoá milestone, issue mới phải chờ milestone sau.
3. **Tiêu chí "xong" đóng băng từ đầu** (spec 1 trang). Không thêm tiêu chí giữa chừng.
4. **Hạn release cố định.** Đến hạn thì release phần đã xong. Phần chưa xong thì dời sang bản sau có ghi lý do, hoặc chuyển sang "Cắt bớt" trong file Thành tựu.
5. **Không trộn trong một PR**: refactor + tính năng + sửa lỗi.
6. **Feature flag** cho tính năng lớn còn dở (ví dụ `verify_evidence: false` trong config): code vẫn merge vào `main`, chỉ là chưa bật.
7. **Góp ý của người dùng thử không sửa vào bản đã tag.** Góp ý thành Issue, xếp vào milestone sau.
8. **Proposal v3 đóng băng** (luật 4 trong kế hoạch): việc nghiên cứu không được kéo phạm vi sản phẩm theo.

### Bảng GitHub Projects (Kanban)

| Cột | Ý nghĩa |
|---|---|
| Backlog | Ý tưởng, chưa thuộc milestone nào |
| To do | Đã vào milestone hiện tại |
| In progress | Đang làm (**tối đa 2 thẻ cùng lúc**) |
| Done | Đã merge vào main |

Nhãn: `bug`, `prompt`, `eval`, `data`, `grounding`, `ui`, `infra`, `docs`.

---

## 7. Dữ liệu, prompt, eval: phần riêng của sản phẩm AI

### 7.1 Dữ liệu
- Ảnh nằm ngoài git (`data/raw/` + sao lưu OneDrive). Trong git chỉ có `manifest.csv` (tên file + sha256) và `annotations.csv`.
- Dữ liệu công khai: ghi **license và nguồn** vào `data/README.md`, tải bằng script, không commit ảnh.
- Hướng dẫn annotate có version. Đổi hướng dẫn giữa chừng thì ghi ngày đổi.
- Ảnh của người khác (người thử demo, gia đình): cần xin đồng ý trước khi lưu hoặc dùng làm dữ liệu.

### 7.2 Prompt
- Mỗi version là một file riêng, **không xoá bản cũ**.
- `prompts/CHANGELOG.md` ghi theo mẫu: `v2 (20/11): bắt buộc evidence_phrase là danh từ cụ thể — sửa #7, #9`.

### 7.3 Mỗi lần chạy phải tái lập được
Mỗi lần chạy tạo thư mục `runs/<run_id>/` chứa:
`config.yaml` đã dùng · `prompt_version` · `model_id` · `git_sha` · output JSON · `log.jsonl` (latency, token, chi phí).

### 7.4 Eval harness: "unit test" của AI
- Chạy bằng một lệnh: `python -m evals.run --run runs/<run_id>`.
- Các chỉ số cố định, đo ở **mọi** release: tỷ lệ JSON hợp lệ, độ ổn định qua 3 lần chạy, precision/recall theo dimension, tỷ lệ claim–evidence, chi phí/ảnh, độ trễ. Từ v0.3 có thêm kiểm tra đối chứng image-shuffle.
- Khi đổi prompt hoặc model, chạy lại và so với baseline. **Kém hơn thì không release.**
- Mọi con số đưa vào CV đều phải truy được về `evals/reports/`.

---

## 8. Docker, database, CI/CD, môi trường deploy

### 8.1 Môi trường

| Môi trường | Giai đoạn v0.1–v0.5 | Giai đoạn v0.8+ |
|---|---|---|
| Local | Máy cá nhân, `uv run` | `docker compose up` |
| Staging | — (dùng Space riêng tư nếu cần) | VPS, giống hệt prod |
| Production | Hugging Face Spaces | VPS + domain |

Nguyên tắc: **cùng một image cho mọi môi trường**, chỉ khác `.env`.

### 8.2 Docker
- **Image** = bản đóng gói không thay đổi được; **container** = image đang chạy; **registry** (GHCR) = nơi lưu image.
- Đóng gói vào image: code, dependency đã pin, lệnh chạy.
- Không đóng gói: secrets, dữ liệu, weights, ảnh người dùng. Những thứ này đưa vào lúc chạy qua `--env-file` hoặc volume.
- Build multi-stage và có `.dockerignore` (bỏ `data/`, `runs/`, `.env`, `.git`).
- Tag image = `version` + `git SHA` (ví dụ `phoai:0.5.0-3f2a1c9`) để biết chính xác bản nào đang chạy.

### 8.3 Database (từ v0.8)
- PostgreSQL (+ pgvector nếu cần embeddings). Ảnh để ở object storage (S3/R2/MinIO), DB chỉ lưu đường dẫn và metadata.
- **Mọi thay đổi bảng đều qua migration (Alembic)** được commit trong git. Không bao giờ sửa bảng bằng tay trên production.
- Backup tự động hằng ngày, và **đã thử restore ít nhất một lần**.
- Có seed script tạo dữ liệu giả cho local/staging.

### 8.4 CI/CD (GitHub Actions, từ v0.5)

```
PR / push   →  ruff  →  pytest (mock API)  →  build Docker
merge main  →  (v0.8) push image GHCR → deploy staging → smoke test
tag v*      →  deploy production → healthcheck → lỗi thì rollback về tag trước
```

### 8.5 Giám sát
- Log JSON có `request_id`, latency, token, chi phí.
- Đặt spend limit trên trang nhà cung cấp API + giới hạn số lần gọi/ngày trong app.
- (v0.8) Sentry để báo lỗi, UptimeRobot ping `/health`, Langfuse để trace agent.

---

## 9. Quản lý Claude trong dự án

Claude trong dự án này giống một **đồng nghiệp rất nhanh nhưng mỗi sáng lại quên sạch**. Mỗi phiên làm việc bắt đầu với bộ nhớ trống, nên việc của mình là:
(1) cho nó đúng bối cảnh, (2) giao việc nhỏ và rõ, (3) kiểm tra kết quả, (4) ghi lại bài học để lần sau nó không lặp lỗi.

### 9.1 Hai nơi làm việc với Claude

| Nơi | Dùng cho | Bộ nhớ |
|---|---|---|
| **Claude trên claude.ai / desktop**, Project "AI Photography Tutor" | Lên kế hoạch, review proposal, nghiên cứu, viết docs, review thiết kế | Tài liệu trong Project + memory của Project |
| **Claude Code** (terminal / VS Code) trong thư mục repo | Viết/sửa code, chạy test, đọc lỗi, review diff | `CLAUDE.md` + auto memory + skills trong repo |

Quyết định lớn bàn ở Project, rồi chép kết luận vào `docs/adr/` hoặc `docs/devlog.md` trong repo. Như vậy Claude Code cũng đọc được, và đó là **nguồn sự thật duy nhất**.

### 9.2 Context và token: hiểu đúng để không lãng phí

- **Context window** là tất cả những gì Claude đang "nhìn thấy" trong một phiên: CLAUDE.md, các file đã đọc, toàn bộ hội thoại, output của lệnh.
- **Mỗi tin nhắn mới gửi lại toàn bộ context.** Phiên càng dài thì mỗi câu hỏi càng tốn token, và Claude càng dễ lẫn lộn ("context rot").
- Vì vậy:

| Lệnh (Claude Code) | Khi nào dùng |
|---|---|
| `/clear` | Chuyển sang việc **khác hẳn** (hết block, đóng issue). Không tốn gì. |
| `/compact` | Đang dở **cùng một việc** nhưng context đã dài, ví dụ sau một lúc debug lòng vòng. |
| `/context` | Xem cái gì đang chiếm context (CLAUDE.md, file, MCP...). |
| `/usage` (hoặc `/cost`) | Xem token/chi phí đã dùng. |
| `/rewind` (Esc Esc) | Claude đi sai hướng → quay lại, tốt hơn là cứ chồng thêm câu sửa lên. |
| `/memory` | Xem/sửa các file CLAUDE.md và auto memory. |
| `@đường/dẫn/file` | Chỉ thẳng file cần đọc, thay vì để Claude tự đi tìm. |
| Plan mode (Shift+Tab) | Việc lớn: bắt Claude lập kế hoạch trước, mình duyệt rồi mới cho sửa code. |

**Luật token của PhoAI:**
1. **Một block Pomodoro (hoặc một issue) = một phiên Claude.** Hết block thì `/clear`.
2. Mở đầu phiên bằng: *"Đọc @docs/devlog.md (đoạn cuối) và issue #N. Hôm nay làm X. Chỉ đụng vào file Y."*
3. Không dán log dài nghìn dòng. Chỉ dán đoạn lỗi liên quan, hoặc lưu log ra file rồi chỉ Claude đọc.
4. Việc đơn giản (đổi tên, sửa docstring, viết test mẫu) dùng model nhỏ/rẻ hơn. Model mạnh để dành cho thiết kế và debug khó.
5. Muốn khám phá nhiều file thì giao cho **subagent** (nó đọc ở context riêng rồi trả về tóm tắt), tránh làm phình context chính.

### 9.3 CLAUDE.md: bộ nhớ dự án

- Đặt ở thư mục gốc repo, được commit. Claude Code tự đọc file này **mỗi đầu phiên**.
- Đọc mỗi phiên tức là **tốn token mỗi phiên**, nên giữ ngắn: mục tiêu **dưới ~150 dòng** (tài liệu chính thức khuyên dưới 200 dòng).
- Chỉ để những gì Claude không tự suy ra được từ code: mục tiêu, lệnh chạy, quy ước, những điều cấm, trạng thái hiện tại.
- Tài liệu dài thì **trỏ tới** bằng `@docs/schema.md` thay vì chép vào.
- Ghi chú cá nhân không muốn commit thì để trong `CLAUDE.local.md` (thêm vào `.gitignore`).
- Claude Code còn có **auto memory**: tự ghi những điều nó học được từ các lần mình sửa nó. Thỉnh thoảng mở `/memory` đọc lại, xoá các ghi chú sai hoặc cũ.
- **Luật cập nhật**: Claude mắc cùng một lỗi lần thứ 2 thì thêm một dòng vào CLAUDE.md (ví dụ: "Không gọi API thật trong test, luôn dùng fixture trong tests/fixtures/").
- Mẫu đầy đủ ở mục 10.1.

### 9.4 Skills (SKILL.md): quy trình đóng gói thành lệnh

- Skill là một thư mục `.claude/skills/<tên>/` có file `SKILL.md` (frontmatter `name`, `description` + phần hướng dẫn). Tên thư mục trở thành lệnh `/tên`.
- Đầu phiên Claude chỉ đọc phần **description** (rất ít token). Toàn bộ nội dung skill chỉ được nạp khi gọi đến. Vì vậy quy trình dài nên để trong skill thay vì nhồi vào CLAUDE.md.
- `description` quyết định khi nào Claude tự dùng skill, nên viết rõ "dùng khi nào".
- Nên tạo skill khi **một quy trình lặp lại từ lần thứ 2**. Các skill gợi ý cho PhoAI:

| Skill | Làm gì | Tạo khi |
|---|---|---|
| `/release-check` | Chạy checklist mục 5.2, báo mục nào còn thiếu | Release v0.2 |
| `/run-eval` | Chạy eval trên run mới nhất, so với baseline, viết báo cáo | Tuần 5 |
| `/explain-module` | Giải thích một module theo luật "mình phải hiểu": luồng dữ liệu, input/output, 3 câu hỏi tự kiểm tra | Tuần 3 |
| `/devlog` | Tóm tắt phiên làm việc thành 3–5 dòng cho docs/devlog.md | Tuần 3 |

- Mẫu SKILL.md ở mục 10.2.

### 9.5 Quyền và hàng rào an toàn

Trong `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./data/raw/**)"],
    "ask":  ["Bash(git push:*)", "Bash(git tag:*)"]
  }
}
```

- Claude **không được đọc** `.env` và ảnh gốc, và phải **hỏi trước** khi push hoặc tag.
- Luật bắt buộc tuyệt đối (ví dụ không bao giờ commit `.env`) thì dùng **hook** (PreToolUse) để chặn cứng, vì CLAUDE.md chỉ là lời dặn, Claude có thể không tuân theo.
- Từ v0.5 có thể thêm hook chạy `ruff format` mỗi khi Claude sửa file Python.

### 9.6 Quy trình code cùng Claude (gắn với luật "Code với AI" của Norman)

1. **Tự viết bước trước.** Ghi 3–5 dòng kế hoạch hoặc pseudo-code trước khi hỏi.
2. **Kẹt lỗi:** 5 phút tự đọc lỗi + viết 1 dòng giả thuyết → hỏi Claude kèm giả thuyết đó → sửa xong ghi 1 dòng "lỗi thật là…" vào sổ khái niệm.
3. **Giao việc nhỏ, có tiêu chí "xong":** *"Viết hàm `parse_critique(text) -> Critique`. Xong khi 3 test trong tests/test_schema.py qua. Không sửa file khác."*
4. **Việc lớn dùng plan mode**, duyệt kế hoạch xong mới cho Claude viết.
5. **Kiểm tra mọi thứ Claude viết:**
   - Đọc **toàn bộ diff** (`git diff`) trước khi commit, không commit "mù".
   - Chạy test. Code AI viết mà không có test thì chưa tính là xong.
   - Hỏi Claude *"giải thích từng thay đổi và vì sao"*. Có chỗ mình không giải thích lại được thì chưa merge.
   - Việc quan trọng thì nhờ **một phiên Claude mới** (hoặc subagent) review, vì phiên đã viết code thường bỏ qua lỗi của chính nó.
6. **Tỷ lệ tự viết:** module lõi (schema, critique, grounding, eval) tự viết là chính, Claude review. Phần phụ (boilerplate, Dockerfile, CI, script vẽ biểu đồ) có thể để Claude viết, mình review.
7. **Ghi công bằng:** commit có Claude hỗ trợ thì thêm dòng `Co-Authored-By` nếu muốn minh bạch. Khi phỏng vấn, nói rõ phần nào mình thiết kế và phần nào AI hỗ trợ.

### 9.7 Lỗi thường gặp khi dùng Claude và cách xử lý

| Dấu hiệu | Nguyên nhân thường gặp | Xử lý |
|---|---|---|
| Claude "quên" quy ước, làm sai lại | Context quá dài hoặc CLAUDE.md quá dài | `/clear`, rút gọn CLAUDE.md, đưa luật quan trọng lên đầu |
| Sửa lan sang nhiều file không liên quan | Giao việc mơ hồ | Nói rõ "chỉ sửa file X" |
| Sửa đi sửa lại vẫn lỗi | Context đầy các lần thử sai | `/rewind` hoặc `/clear`, mô tả lại vấn đề từ đầu kèm giả thuyết |
| Token tăng nhanh | Phiên dài, đọc nhiều file, log dài | 1 block = 1 phiên, dùng `@file`, subagent |
| Code chạy nhưng mình không hiểu | Để Claude viết hết | `/explain-module`, tự viết lại phần lõi |

---

## 10. Mẫu sẵn

### 10.1 `CLAUDE.md`

```markdown
# PhoAI — AI Photography Tutor

## Mục tiêu
Critique ảnh cho người mới chụp, mỗi nhận xét có bằng chứng trên ảnh
(Observation → Evidence → Why → What to try). Dự án portfolio AI Engineer.

## Trạng thái hiện tại  (cập nhật mỗi tối CN)
- Đang làm: v0.1 — Milestone "v0.1", xem GitHub Issues
- Prompt hiện tại: prompts/critique_v2.md · model: xem config/default.yaml

## Lệnh
- Cài đặt: `uv sync`
- Chạy: `uv run python -m phoai.pipeline <ảnh>`
- Test: `uv run pytest -m "not slow"`
- Eval: `uv run python -m evals.run --run runs/<run_id>`
- Format: `uv run ruff format . && uv run ruff check .`

## Quy ước
- Python 3.12, type hints, pydantic cho mọi dữ liệu đi ra/vào model
- Prompt nằm trong prompts/, KHÔNG viết cứng trong code
- Mỗi output lưu kèm prompt_version, model_id, schema_version, git_sha
- Test không gọi API thật — dùng fixture trong tests/fixtures/
- Commit theo Conventional Commits; không tự push, không tự tag

## Cách làm việc với tôi
- Tôi là người học: module lõi (schema, critique, grounding, evals) tôi tự viết,
  bạn review và giải thích. Đừng viết lại toàn bộ file khi tôi chỉ hỏi.
- Trước khi sửa > 2 file: nêu kế hoạch và chờ tôi đồng ý.
- Khi sửa lỗi: nói nguyên nhân gốc trong 1 câu.

## Không bao giờ
- Đọc hay in nội dung .env
- Commit data/raw/, runs/, cache/
- Thêm dependency mới mà không hỏi

## Tài liệu
- Spec: @docs/spec-v0.1.md · Schema: @docs/schema.md
- Quyết định kỹ thuật: docs/adr/ · Nhật ký: docs/devlog.md
```

### 10.2 `.claude/skills/release-check/SKILL.md`

```markdown
---
name: release-check
description: Kiểm tra checklist trước khi tag một release của PhoAI. Dùng khi tôi nói "chuẩn bị release", "tag v0.x" hoặc gọi /release-check.
---

# Release check

1. Đọc version trong pyproject.toml và tag gần nhất (`git describe --tags --abbrev=0`).
2. Kiểm tra từng mục, báo ✅ / ❌ kèm lý do:
   - version đã tăng so với tag gần nhất
   - CHANGELOG.md có mục cho version mới
   - prompts/CHANGELOG.md cập nhật nếu prompts/ thay đổi kể từ tag trước
   - evals/reports/ có báo cáo cho version mới, có bảng so với bản trước
   - .env.example chứa mọi biến môi trường được dùng trong src/
   - `uv run pytest -m "not slow"` qua
   - không có file trong data/raw/, runs/, .env được git theo dõi
3. KHÔNG tự tạo tag hay push. Chỉ in danh sách việc còn thiếu.
```

### 10.3 `.github/pull_request_template.md`

```markdown
## Làm gì
<!-- 1–3 dòng. Liên kết issue: Fixes #... -->

## Kiểm tra
- [ ] Đã đọc toàn bộ diff
- [ ] Test qua (`pytest -m "not slow"`)
- [ ] Nếu đổi prompt/model: đã chạy eval, kết quả trong evals/reports/
- [ ] Không có secret / dữ liệu thô trong diff
- [ ] Tôi giải thích được mọi dòng thay đổi

## Claude hỗ trợ phần nào
<!-- ví dụ: viết test mẫu, review; phần lõi tự viết -->
```

### 10.4 `CHANGELOG.md`

```markdown
# Changelog

## [0.2.0] — 2026-12-04
### Added
- Eval harness: precision/recall theo dimension, độ ổn định 3 lần chạy
- Cache kết quả theo hash(ảnh + prompt_version + model_id)
### Changed
- Prompt v2 → v3: ... (xem prompts/CHANGELOG.md)
### Fixed
- Retry khi JSON lỗi (#7)

## [0.1.0] — 2026-11-22
### Added
- critique.py chạy trên 5 ảnh, output JSON hợp lệ 100%
```

### 10.5 `docs/devlog.md`

```markdown
## Tuần 3 (15–21/11)
- Xong: schema + pydantic, prompt v1→v2, critique.py chạy 5 ảnh (PHO-03)
- Vướng: model hay trả evidence chung chung ("toàn ảnh") → issue #9
- Quyết định: giữ JSON mode thay vì function calling (ADR 0002)
- Bước đầu tiên tuần sau: tag v0.1.0, hẹn 1 người xem CN 22/11
- Claude: thêm luật "test không gọi API thật" vào CLAUDE.md
```

---

## 11. Nhịp quản lý

**Mỗi block (Pomodoro)**
- Đầu block: mở issue → tạo/chuyển sang nhánh → phiên Claude mới (`/clear`).
- Cuối block: commit → push → kéo thẻ Kanban → ghi bước đầu tiên lần sau.

**Mỗi Chủ nhật (việc nhẹ 17:00)**
- Viết đoạn tuần trong `docs/devlog.md`, cập nhật "Trạng thái hiện tại" trong CLAUDE.md.

**Mỗi tối thứ 7 (tổng kết 19:00) — 10 phút cho dự án**
- Rà Milestone: đóng issue xong, issue trễ thì dời (có lý do) hoặc cắt.
- Xem chi phí API trong tuần.
- Rà CLAUDE.md và auto memory (`/memory`): thêm luật mới, xoá ghi chú cũ.
- Đọc lại mục 6 (giới hạn phạm vi) của sổ tay này.

**Mỗi release**
- Chạy `/release-check`, làm theo checklist mục 5.2, cập nhật file Thành tựu.

---

### Tài liệu tham khảo
- Claude Code — Memory (CLAUDE.md, auto memory): https://code.claude.com/docs/en/memory
- Claude Code — Skills: https://code.claude.com/docs/en/skills
- Conventional Commits: https://www.conventionalcommits.org
- Semantic Versioning: https://semver.org
- Keep a Changelog: https://keepachangelog.com

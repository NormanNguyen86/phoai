# test-photos.en.md — PhoAI test photo set

- Written: 2026-11-16 (labels assigned from EXIF and measurements on the images; the primary labels were confirmed by the author on the same day)
- Photo author: Ngoc Manh, shot on a Canon EOS RP with an RF24-105mm F4-7.1 IS STM; full usage rights
- Location: `data/test-photos.md` (text). The photos are in `data/raw/`, outside git.
- Revised: 2026-11-19. Added section 9 (expected output per dimension, aligned to the `prompts/critique_v1.md` prompt) and edited the `02a` ISO row in section 6. Sections 2–5 are unchanged. Section 9 was derived from sections 5–6 and is **not yet confirmed by the author**.
- No model output was seen when these labels were written, or when section 9 was written.
- Sections 1–8 only describe the photo set. Section 9 is tied to one prompt version (`prompts/critique_v1.md`, identified as `critique_v1` in run output); if the prompt's rules change, section 9 must be re-checked. How the set is used and judged may change later.

## 1. Scope and reproducibility

- The photos belong to the author and live outside the repo, so anyone cloning the repo cannot re-run this exact set. To verify you have the same photos, compare the sha256 values in section 3.
- `data/raw/` holds 9 files. 5 are test inputs (see the "Role" column in section 3); the other 4 are same-scene references. `example_01b` was originally a test photo and has been moved to the references so the set has exactly 5 test photos, as the DoD requires. 01b was chosen because its label rests on an eyeballed estimate [EYE], which is weaker than the measured labels. Its label is still in section 6.
- Evidence tags: **[EXIF]** read from metadata, **[MEASURED]** computed by code on the correctly rotated image (full 1620×1080 px), **[EYE]** estimated by eye on a 10% grid (error about ±0.02 of the frame).
- Label convention: a **primary label** is a clear, measurable or author-confirmed finding. Subjective or unclear judgements were dropped. **Other measured observations** (section 6) are only there to see whether a model notices them unprompted; they are not counted as expected defects.
- Defect labels (sections 2 and 6) are not the prompt's output. The prompt reports five dimensions (`subject_story`, `composition`, `light_exposure`, `color_tone`, `technical`) with a label for each. Section 9 maps the defect labels to that output; use section 9, not section 6, when scoring a model run.

## 2. Test set (5 photos)

| Photo ID | Short description | Why chosen | Expected issue (primary label) | Written |
|---|---|---|---|---|
| `example_01c` | Station corridor, person walking far away near the vanishing point | Lighting group: good composition, subject not separated from the background | Subject poorly separated from background: 1.8 stops darker than its surroundings | 2026-11-16 |
| `example_02a` | Central clock tower, white sky | Exposure group: settings error, with a fixed version (`02b`) | Severe highlight clipping (40.6% of pixels ≥ 250, sky 100%), clock-face detail lost. The ISO label needs the shooting settings, see section 6 | 2026-11-16 |
| `example_03` | Under a bridge, car in the bright opening behind | Subject-position group: good frame-within-frame, subject placed poorly | Car sits against the right pillar of the opening (0.04 of frame). Exposure error: 41.4% of pixels ≤ 10, not intentional | 2026-11-16 |
| `example_04` | Staircase between two walls, person walking down | Lighting group: good composition and leading lines, subject underlit | Subject sunk in shade and underexposed: 1.9 stops darker than surroundings. Right wall: 64% of pixels ≤ 10 | 2026-11-16 |
| `example_05b` | Street corner, woman walking to the right | Look-room group | Look room ahead 0.16 of frame (photo `05a`: 0.58) | 2026-11-16 |

## 3. Files in `data/raw/`

All are JPEG, RGB, no ICC profile, stored at 1620×1080 px. Photos with Orientation = 8 display at 1080×1620 (portrait) once rotated. File sizes range from 222 KB to 449 KB, about 2.8 MB in total.

| File | Role | Date, time shot [EXIF] | KB | Orient. | Shutter, aperture, ISO, focal length [EXIF] | EV100 from settings | sha256 (first 12 chars) |
|---|---|---|---|---|---|---|---|
| Example_01_a.JPG | reference (no subject) | 2026-10-30 16:02:06 | 222 | 8 | 1/250, f/5.6, ISO 1250, 40mm | 9.29 | 18dfc099a558 |
| Example_01_b.JPG | reference (subject-position counterpart) | 2026-10-30 16:02:13 | 223 | 8 | 1/250, f/5.6, ISO 1250, 40mm | 9.29 | 15a447582487 |
| Example_01_c.JPG | **test** | 2026-10-30 16:02:14 | 224 | 8 | 1/250, f/5.6, ISO 1250, 40mm | 9.29 | 434a401a20be |
| Example_02_a.JPG | **test** | 2026-10-30 15:42:47 | 358 | 8 | 1/250, f/8, ISO 1000, 70mm | 10.64 | fda937e2facd |
| Example_02_b.JPG | reference (fixed version of 02a) | 2026-10-30 15:43:30 | 449 | 8 | 1/250, f/8, ISO 125, 70mm | 13.64 | 1204780924c6 |
| Example_03.JPG | **test** | 2026-11-06 07:10:50 | 250 | 1 | 1/200, f/7.1, ISO 400, 60mm | 11.30 | 4d9aaa6015c9 |
| Example_04.JPG | **test** | 2026-11-11 17:49:49 | 319 | 8 | 1/250, f/7.1, ISO 1000, 105mm | 10.30 | b5d76377eaba |
| Example_05_a.JPG | reference (counterpart of 05b) | 2026-11-11 17:45:22 | 427 | 8 | 1/250, f/9, ISO 160, 105mm | 13.63 | 0bd90f714a69 |
| Example_05_b.JPG | **test** | 2026-11-11 17:45:35 | 420 | 8 | 1/250, f/9, ISO 160, 105mm | 13.63 | 4ba0a181a6c2 |

EV100 = log2(f²/t) − log2(ISO/100), i.e. normalised to ISO 100. For a sunny scene, `02b` and `05` give EV100 ≈ 13.6. `02a` is 3 stops lower: with the same 1/250 and f/8 the light reaching the sensor is identical, and ISO 1000 only amplifies the signal, so the image is 3 stops brighter than `02b`.

## 4. Comparison groups

Pairs and triples both count, as long as the scene is the same. **The a/b pairs are comparison sets with a known answer.** In each group one main variable changes and the others stay fixed.

| Group | Photos | What changes | What stays fixed (evidence) | Can compare |
|---|---|---|---|---|
| G01 | `01a`, `01b`, `01c` | Subject: none / touching wall / far away in the dark | Same settings. Mean luma 61.1–63.4, R/B of the white tiles 2.28–2.34. At most 8 seconds apart | Subject position and separation. Exposure and colour are nearly constant, so they act as the control |
| G02 | `02a` → `02b` | ISO 1000 → 125 (3 stops) | Same 1/250, f/8, 70mm, same framing (tower offset ≤ 0.03). 43 seconds apart | Exposure. `02b` is the corrected version |
| G05 | `05a`, `05b` | Subject: man walking left / woman walking right | Identical settings. Median L* 56.1 and 55.8. 13 seconds apart | Look room, subject position |
| (single) | `03`, `04` | none | none | No same-scene counterpart. Only indirect comparison through measurements (both high-contrast scenes with heavy shadows) |

## 5. Measurements

Conventions: images rotated per EXIF, 8-bit sRGB. Luma uses Rec.709 weights on gamma-encoded values. L* is CIELAB with D65. "Stop" is log2 of the linear luminance ratio. Subjects are measured inside an eyeballed bounding box and compared with the ring around it (box expanded by 50%).

### 5.1 Brightness and tone

| Photo | Mean luma | Median L* | p99 luma | % pixels ≥ 250 | % pixels ≤ 10 | Notes |
|---|---|---|---|---|---|---|
| 01_a | 63.4 | 26.5 | 106 | 0.01 | 2.4 | White tile luma 79 |
| 01_b | 61.1 | 26.1 | 106 | 0.01 | 3.1 | White tile luma 75 |
| 01_c | 62.0 | 26.3 | 106 | 0.01 | 2.9 | White tile luma 77 |
| 02_a | 223.9 | 93.7 | 255 | **40.59** | 0.0 | Sky 100% ≥ 250. Tower 42.2% ≥ 250. Clock face: luma 5th–95th percentile 140–255, std 37.5 |
| 02_b | 140.3 | 61.0 | 226 | 0.02 | 0.3 | Clock face: luma 5th–95th percentile 56–225, std 51.6. 5.0% of pixels have at least one channel ≥ 250 (red channel on the sandstone) |
| 03 | 23.9 | 3.9 | 162 | 0.02 | **41.4** | 21.0% ≤ 5. The bright opening is 5.0 stops above the dark pillar |
| 04 | 47.1 | 9.5 | 246 | 0.65 | **28.9** | Right wall: median luma 8, 64% ≤ 10. Sunlit left wall: 87. Sky/glass at top: 184. Sky is 6.3 stops above the right wall; sunlit wall is 4.5 stops above it |
| 05_a | 106.6 | 56.1 | 197 | 0.01 | 8.8 | |
| 05_b | 107.5 | 55.8 | 200 | 0.03 | 5.6 | |

### 5.2 Colour

| Photo | Measurement | Notes |
|---|---|---|
| 01_a / 01_b / 01_c | White tiles (ROI on the column): R/B = 2.28 / 2.34 / 2.31. Lab (a*, b*) = (5.7, 22.9) / (5.5, 22.5) / (5.7, 22.8). Whole-frame mean b* about 19.5 | White objects are strongly yellow-orange. Same in all three. The author does not treat this as a defect |
| 02_a | Mean b* 8.1 | White sky, so sky colour cannot be measured |
| 02_b | Mean b* 1.6. Mean sky RGB (147, 175, 228) | Close to neutral, blue sky |
| 03 | Mean b* 3.0 | |
| 04 | Mean (a*, b*) = (0.1, −0.1) | Neutral |
| 05_a / 05_b | Mean b* 13.3 in both | Warm, but there is no neutral object in the frame to use as a reference, so no colour cast is claimed. Shot at 17:45 |

### 5.3 Subject and composition

d(1/3) is the distance (in normalised frame units) from the subject centre to the nearest rule-of-thirds intersection.

| Photo | Centre (x, y) | Margins L / R / T / B | Bbox area | d(1/3) | Other measurements |
|---|---|---|---|---|---|
| 01_b | (0.78, 0.60) | 0.71 / 0.14 / 0.48 / 0.27 | 3.8% | 0.13 | Left edge of the box is about 0.01–0.03 from the wall corner [EYE]. Subject is 0.7 stop darker than its ring. Offset from the vanishing-point axis (x ≈ 0.50): 0.28 |
| 01_c | (0.55, 0.61) | 0.50 / 0.40 / 0.50 / 0.28 | 2.2% | 0.13 | Offset from the vanishing-point axis: 0.05. Subject is **1.8 stops** darker than its ring (median luma 26 vs 54) |
| 03 | (0.65, 0.62) | 0.59 / 0.30 / 0.57 / 0.32 | 1.2% | 0.05 | Inside the bright opening (x from 0.31 to 0.74): car at 0.79 of the opening width, 0.04 of the frame from the right pillar. Car brightness (mean luma 51) is close to its surroundings (58), −0.5 stop |
| 04 | (0.51, 0.60) | 0.43 / 0.42 / 0.48 / 0.28 | 3.6% | 0.17 | On the centre axis. Leading lines (stairs, handrails) converge near (0.5, 0.33) [EYE]. Subject is **1.9 stops** darker than its ring (median luma 9 vs 26) |
| 05_a | (0.69, 0.77) | 0.58 / 0.20 / 0.62 / 0.09 | 6.3% | 0.10 | Walking left: space ahead 0.58, behind 0.20 |
| 05_b | (0.74, 0.77) | 0.64 / 0.16 / 0.65 / 0.12 | 4.6% | 0.12 | Walking right: space ahead **0.16**, behind 0.64 |

## 6. Labels per photo

Thresholds used to assign labels. **The thresholds were set after looking at the measurements of this very set**, so the labels are partly circular (thresholds chosen from the data, then the data labelled by the thresholds). Keep this in mind when using them as answers in v0.2, and do not treat a model matching these labels as independent evidence of accuracy. The thresholds can be changed:

| Criterion | Threshold |
|---|---|
| Highlight clipping | % pixels ≥ 250: ≥ 2% is present, ≥ 25% is severe |
| Lost shadow detail | % pixels ≤ 10: ≥ 10% is present, ≥ 30% is severe |
| Dark overall | Median L* < 35 |
| High-contrast scene | Difference between brightest and darkest areas ≥ 4.5 stops |
| Subject poorly separated or sunk in shade | Darker than its ring by ≥ 1.5 stops |
| Limited look room | Space ahead < 0.25 of frame width |
| Subject at an edge or line | Distance to frame edge or line ≤ 0.05 |

| Photo | Primary label (expected) | Basis | Other measured observations (not counted as expected defects) |
|---|---|---|---|
| `01c` | `subject_low_separation` | −1.8 stop [MEASURED]; confirmed by author | Whole scene is dark (median L* 26, white tiles ≈ 77/255). Yellow-orange, R/B 2.31. Subject centre is 0.05 from the vanishing-point axis (a strength) |
| `02a` | `highlight_clipped_severe`; `subject_detail_loss` | 40.6% ≥ 250 and sky 100% [MEASURED]; clock-face minimum luma 140 vs 56 in `02b` [MEASURED] | |
| `03` | `shadow_crush_severe` (exposure error; the author confirmed it was not intentional); `subject_at_inner_frame_edge` | 41.4% ≤ 10 [MEASURED]; 0.04 from the right pillar [EYE] | High-contrast scene: the opening is 5.0 stops above the dark pillar. The car covers only 1.2% of the frame. Against the whole frame the car is only 0.05 from a thirds intersection, so a full-frame thirds check passes while its relationship to the inner frame does not |
| `04` | `subject_in_shade_underexposed`; `shadow_crush` | −1.9 stop [MEASURED], confirmed by author; 28.9% ≤ 10 and right wall 64% [MEASURED] | High-contrast scene: sky is 6.3 stops above the right wall. Strengths: no significant clipping (0.65% ≥ 250); subject on the centre axis, matching the leading-line convergence point |
| `05b` | `limited_look_room` | Space ahead 0.16 [EYE], vs 0.58 in `05a` | Exposure is fine (median L* 55.8; 0.03% ≥ 250). The traffic light was placed deliberately (confirmed by author) |

Note: labels in the same row that share a root cause are one problem in the prompt's output (`02a`: `highlight_clipped_severe` and `subject_detail_loss`; `04`: `subject_in_shade_underexposed` and `shadow_crush`; both fall under Light & Exposure). The two labels of `03` have different causes and are two problems. See section 9.

Reference photos:

| Photo | Label | Basis |
|---|---|---|
| `01a` | `subject_missing` | Same scene and settings as `01b`, `01c` |
| `01b` | `subject_tangent_to_wall_line` | 0.01–0.03 from the wall corner [EYE]; stated by author. Whole scene dark and yellow-orange as in `01c`; separation −0.7 stop, below the threshold |
| `02b` | `exposure_ok` | Median L* 61; p99 226; 0.02% ≥ 250 |
| `05a` | `look_room_ok` | Space ahead 0.58; same settings and exposure as `05b` |

Labels that need the shooting settings (EXIF) and cannot be inferred from the pixels of a single photo:

| Photo | Label | Basis | Condition for scoring |
|---|---|---|---|
| `02a` | `iso_too_high_for_light` | ISO 1000 (EV100 10.64) vs ISO 125 in `02b` (EV100 13.64), same 1/250, f/8: the image is 3 stops brighter because of the higher ISO [EXIF] | **Out of scope for v0.1, not scored.** The `critique_v1` prompt tells the model not to assume camera settings or EXIF, and v0.1 sends only the image, so this label cannot be checked from the output. Revisit only if a later version passes the shooting settings to the model; passing settings is not implemented yet (Backlog) |

## 7. Preprocessing required before use

1. **Apply the EXIF Orientation.** 8 of 9 photos have Orientation = 8 (only `Example_03` is 1). Without rotation the image appears turned 90°, and every composition judgement (thirds, facing direction, look room) is made on the wrong orientation. Use `ImageOps.exif_transpose`. All coordinates and measurements in this file were taken on rotated images. Rotate in memory, on decoded pixels; do not save back to JPEG (see items 4 and 8). The API documentation also warns that the model may make mistakes on rotated images.
2. **Extract the shooting settings before stripping EXIF.** Pull ExposureTime, FNumber, ISO and FocalLength (and DateTimeOriginal if needed) into text or `annotations.csv`. A model should not have to guess settings from pixels.
3. **Strip private metadata before sending images outside or publishing them.** All 9 photos carry the camera body serial, the lens serial and an embedded thumbnail. A GPS block is present in EXIF but contains only GPSVersionID, with no coordinates (checked). Order: rotate → extract settings → strip EXIF.
4. **Do not adjust tone, re-compress as JPEG, or resize before measuring.** Auto-contrast, gamma and a second JPEG compression change the measurements (clipping, lost shadow detail, colour). Measure directly on the rotated pixels. When sending to an API, encode the rotated pixels as **PNG** (lossless on the decoded pixels); do not save back to JPEG. The sha256 values in section 3 apply only to the original JPEG files, because a PNG has a different hash.
5. **Do not convert the colour space.** The photos have no ICC profile; treat them as sRGB and leave them as they are.
6. **Verify integrity with sha256 (section 3).** Re-exporting or re-saving a JPEG changes the hash. If a photo is replaced, update the table and the date.
7. **Photos contain strangers** (`01b`, `01c`, `03`, `04`, `05a`, `05b`). No one has been asked for permission, so the set is not published.
8. **API image limits** (checked against the Claude API documentation on 2026-11-16):
   - Up to 10 MB per image (base64) on the Claude API, 5 MB on Amazon Bedrock. Up to 8000×8000 px. Formats: JPEG, PNG, GIF, WebP. Up to 128 MB per request on the Claude API.
   - The 9 photos as PNG after rotation are 1.05–2.21 MB (Pillow 12.3.0, default compression). Base64 adds about 33%, at most about 2.95 MB, still under Bedrock's 5 MB limit.
   - Long edge 1620 px: models on the standard tier downscale to at most 1568 px (about 3% smaller). The high-resolution tier (for example Sonnet 5, Opus 4.7/4.8, Fable 5, Mythos 5) allows up to 2576 px and does not downscale. The measurements use normalised 0–1 coordinates, so they do not change with the downscale.
   - Fallback: JPEG at quality 95, 4:4:4 (about 0.33–0.66 MB), but that is a second compression; use it only if the size limit is exceeded.
   - Lossless JPEG rotation (jpegtran) was not tried. The photos are 4:2:2 and 1620 is not a multiple of 16, so edges may be trimmed or the transform refused.

## 8. Source of the measurements

The measurements in section 5 were computed on 2026-11-16 with Python (Pillow 12.3.0, NumPy 2.5.3), run by Claude (an AI assistant) in a working session at the author's request. The script is not saved in the repo, so reproducing the numbers means re-implementing them from the conventions at the top of section 5. Subject bounding boxes are eyeballed estimates, not the result of automatic detection. If a photo is replaced, re-measure.

Section 9 was written on 2026-11-19 by Claude at the author's request. It adds no new measurements: it re-expresses sections 5 and 6 in the prompt's output terms. Every entry that is not copied from those sections is a mapping decision and is marked as unconfirmed.

## 9. Expected output per dimension (for `prompts/critique_v1.md`)

Status: **proposed, not confirmed by the author.** No model output was seen. The thresholds behind the defect labels were chosen after looking at this set (section 6), so matching this table is not independent evidence of accuracy.

### 9.1 Conventions

- Dimension codes: `subject_story`, `composition`, `light_exposure`, `color_tone`, `technical`.
- Expected label for each dimension:

| Value | Meaning in this file |
|---|---|
| `needs_work` | The dimension has a primary label in section 6. The prompt's v0.1 output does not separate "present" from "severe", so both give `needs_work` |
| `fine` | A weakness is documented in this file, but it is below the threshold or the author does not treat it as a defect |
| `good` | A reference label says "ok", or this file records a strength and no weakness |
| `unscored` | No ground truth (not measured, not labelled). Whatever the model says for this dimension is neither right nor wrong |

- "`X` or `Y`" means either label is accepted.
- **Root problem.** The prompt assigns each problem to one dimension: anything about brightness or lost tonal detail (clipped highlights, crushed shadows, too dark, too bright) is always `light_exposure`, whichever setting would fix it; otherwise the dimension whose fix solves it. Labels from section 6 that share a root cause are one problem.
- **Evidence zones.** The prompt reports 3×3 grid zones on the upright image. Columns split at x = 1/3 and 2/3, rows at y = 1/3 and 2/3. The expected zone comes from the subject centre in section 5.3. If the point lies within 0.05 of a grid line, the adjacent zone is also accepted. `global` means the whole image. "Not mapped" means this file has no coordinates for it, so the evidence of that problem is not scored.
- **Priority.** Where a photo has two expected problems, the author has not set an order; either order is accepted.

### 9.2 Expected label per dimension

| Photo | Role | `subject_story` | `composition` | `light_exposure` | `color_tone` | `technical` |
|---|---|---|---|---|---|---|
| `01c` | test | `needs_work` or `fine` | `good` | `needs_work` | `good` or `fine` | `unscored` |
| `02a` | test | `unscored` | `unscored` | `needs_work` | `unscored` | `unscored` |
| `03` | test | `unscored` | `needs_work` | `needs_work` | `unscored` | `unscored` |
| `04` | test | `needs_work` or `fine` | `good` | `needs_work` | `unscored` | `unscored` |
| `05b` | test | `unscored` | `needs_work` | `good` or `fine` | `unscored` | `unscored` |
| `01a` | reference | `needs_work` | `unscored` | `unscored` | `unscored` | `unscored` |
| `01b` | reference | `fine` | `needs_work` | `unscored` | `unscored` | `unscored` |
| `02b` | reference | `unscored` | `unscored` | `good` | `unscored` | `unscored` |
| `05a` | reference | `unscored` | `good` | `good` or `fine` | `unscored` | `unscored` |

Reasons for the entries that are not a direct copy of a section 6 label:
- `01c` and `04`, `subject_story`: the subject is 1.8 / 1.9 stops darker than its surroundings, so a model may also flag subject readability. That is accepted but not required, because the root problem is brightness (`light_exposure`).
- `01c`, `color_tone`: white objects are strongly yellow-orange (R/B 2.31), but the author does not treat it as a defect. `needs_work` here counts as a false positive.
- `01b`, `subject_story`: the subject is 0.7 stop darker than its ring, below the 1.5-stop threshold (section 6), so `fine`.
- `05b` and `05a`, `light_exposure`: section 6 says exposure is fine (median L* 55.8 / 56.1, ≤ 0.03% pixels ≥ 250). Light quality (direction, hardness) was not assessed, so `good` or `fine`.
- `02b`, `light_exposure`: `exposure_ok` (median L* 61; 0.02% ≥ 250).

### 9.3 Expected problems, evidence, strengths and author intent

| Photo | Expected root problem(s) | Section 6 labels merged | Expected evidence zone | Expected strengths (dimension: what) | Author intent on record |
|---|---|---|---|---|---|
| `01c` | `light_exposure`: subject 1.8 stops darker than its surroundings. Related: `subject_story` | `subject_low_separation` | `center` (subject centre (0.55, 0.61)) | `composition`: subject 0.05 from the vanishing-point axis | None for the shot. The author does not treat the yellow-orange cast as a defect |
| `02a` | `light_exposure`: severe highlight clipping, clock-face detail lost | `highlight_clipped_severe`, `subject_detail_loss` | `global` (clipping covers 40.6% of pixels, sky 100%; per-zone location not mapped) | None recorded | None recorded |
| `03` | Two problems: (a) `light_exposure`: crushed shadows, 41.4% of pixels ≤ 10; (b) `composition`: car 0.04 of the frame from the right pillar of the opening | (a) `shadow_crush_severe`; (b) `subject_at_inner_frame_edge` | (a) `global` (not mapped); (b) `center` (car centre (0.65, 0.62) is 0.017 from the x = 2/3 line and 0.047 from the y = 2/3 line, so by the 9.1 rule `middle-right`, `bottom-center` and `bottom-right` are also accepted) | `composition`: frame-within-frame (section 2) | The exposure error was **not intentional** (author-confirmed). The prompt treats lost tonal detail as a flaw even when the mood looks deliberate, so a "dark, moody, intentional" reading is a wrong answer |
| `04` | `light_exposure`: subject 1.9 stops darker than its surroundings, right wall crushed (64% ≤ 10) | `subject_in_shade_underexposed`, `shadow_crush` | Subject: `center` (centre (0.51, 0.60)). Right wall: not mapped | `composition`: subject on the centre axis, leading lines converge near (0.5, 0.33) [EYE]. `light_exposure`: no significant clipping (0.65% ≥ 250) | None recorded |
| `05b` | `composition`: space ahead of the subject 0.16 of the frame (0.58 in `05a`) | `limited_look_room` | `bottom-right` (subject centre (0.74, 0.77), walking right) | `light_exposure`: exposure fine (median L* 55.8; 0.03% ≥ 250) | The traffic light was placed deliberately (author-confirmed). Flagging it as a defect is a false positive |
| `01a` | `subject_story`: no subject | `subject_missing` | `global` | None | None recorded |
| `01b` | `composition`: subject 0.01–0.03 from the wall corner [EYE] | `subject_tangent_to_wall_line` | `middle-right` (subject centre (0.78, 0.60)) | None | None recorded |
| `02b` | None expected | `exposure_ok` | None | `light_exposure`: no clipping (0.02% ≥ 250), p99 luma 226 | None recorded |
| `05a` | None expected | `look_room_ok` | None | `composition`: space ahead 0.58 | None recorded |

Strengths are scored for recall only: the model may list other true strengths, but it is not wrong if it misses one of these. "None recorded" means the author has not stated an intent for the shot; the author should fill these in before v0.2.

### 9.4 Coverage limits

- **`technical` and `color_tone` have no ground truth.** No photo carries a labelled Technical or Color defect, and sharpness, noise and focus were never measured. Under v0.1 these two dimensions can only be checked for obvious false positives; the model's labels there are `unscored`. To score them, measure (for example sharpness) or add photos with a known defect.
- **The expected root problems are unbalanced.** Of the 6 expected root problems in the test photos, 4 are `light_exposure` and 2 are `composition` (`03b`, `05b`); `subject_story` appears only in the reference `01a`. Per-dimension precision and recall will rest on very few cases.
- **`iso_too_high_for_light` is out of scope** (section 6): the prompt does not assume settings.
- **Photos with one expected problem do not test ranking.** Only `03` has two expected problems, and its order is not set, so the prompt's priority ordering is not tested.
- **Circularity** (section 6) still applies, and this mapping has not been confirmed by the author. Confirm 9.2 and 9.3 before using them to score a run.
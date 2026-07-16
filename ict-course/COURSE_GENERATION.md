# ICT Video Course — Windows Generation Guide (Edge TTS + FFmpeg)

This folder contains a pipeline that:
1) Extracts the **voice-over text** from `ict-course/scripts/lesson-XX-*.md`
2) Generates **male TTS audio** using **Microsoft Edge/Bing TTS** (voice: `en-US-GuyNeural`)
3) Creates **placeholder “width” slide images** (until PDF image extraction is added)
4) Renders an **MP4** using **FFmpeg**

## Prerequisites (install once)

### 1) Python
- Python 3.10+ recommended

### 2) FFmpeg
- Ensure `ffmpeg` is available in PATH

Test:
```bat
ffmpeg -version
```

### 3) Python dependencies
Run from repo root (same folder that contains `ict-course/`):
```bat
pip install -r ict-course/requirements.txt
```

> If `ict-course/requirements.txt` does not exist yet, create it (or tell me and I’ll add it).

## Voice (Edge/Bing TTS)
- Default voice comes from `ict-course/voice_settings.md`
- Voice used by generator: `en-US-GuyNeural`

## Output layout
- Output root: `ict-course/course/`
- Per lesson:
  - `ict-course/course/lesson-01/voice/`
  - `ict-course/course/lesson-01/images/`
  - `ict-course/course/lesson-01/video/lesson-01.mp4`

## Run

### Build all lessons
```bat
python ict-course/generate_course.py --all
```

### Build a single lesson
```bat
python ict-course/generate_course.py --lesson 01
```

## Notes about “PDF images”
This scaffold currently generates **placeholder slide images** derived from the narration.
Once you confirm a PDF-to-image method, we’ll replace placeholders with extracted images/figures from:
- `ICTPDF_Practical_ICT_Strategies_by_Ayub_Rana_5th+Edition_@ict_goat.pdf`

Suggested future extraction options:
- Poppler (`pdftoppm` / `pdfimages`)
- Python (`pymupdf` / `fitz`)
- CLI + scripting around FFmpeg

## What this produces
For each lesson:
- `voice/voice_script.txt` (extracted narration text)
- `voice/audio.mp3` (Edge/Bing TTS output)
- `images/slide-XX.png` (placeholder slides)
- `video/lesson-XX.mp4` (final MP4)

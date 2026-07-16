import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

try:
    import edge_tts  # type: ignore
except Exception:
    edge_tts = None


REPO_ROOT = Path(__file__).resolve().parent
COURSE_ROOT = REPO_ROOT / "course"


@dataclass
class Canvas:
    width: int
    height: int
    fps: int


def load_config() -> dict:
    cfg_path = REPO_ROOT / "course_config.json"
    if not cfg_path.exists():
        raise FileNotFoundError(f"Missing config: {cfg_path}")
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def parse_voice_settings() -> str:
    voice_file = REPO_ROOT / "voice_settings.md"
    txt = voice_file.read_text(encoding="utf-8")
    # expects: Voice: `en-US-GuyNeural`
    m = re.search(r"Voice:\s*`([^`]+)`", txt)
    if not m:
        # fallback
        return "en-US-GuyNeural"
    return m.group(1).strip()


def read_lesson_script(lesson_id: str) -> str:
    src = REPO_ROOT / "scripts" / f"lesson-{lesson_id}-"
    # find matching files
    candidates = sorted((REPO_ROOT / "scripts").glob(f"lesson-{lesson_id}-*.md"))
    if not candidates:
        raise FileNotFoundError(f"No lesson script found for lesson-{lesson_id}-*.md")
    # If multiple, pick the first (usually one)
    content = candidates[0].read_text(encoding="utf-8")
    return content


def extract_narration_text(md: str) -> str:
    """
    Extract only narration body text.
    Heuristic:
      - remove the 'Narration (...)' header block and metadata lines
      - stop at 'Practice / Assignment' and 'Recap'
      - keep lines after 'Lesson Script' header until next section header.
    """
    # Normalize newlines
    text = md.replace("\r\n", "\n")

    # Find "## Lesson Script"
    m = re.search(r"^##\s*Lesson Script\s*$", text, flags=re.MULTILINE)
    if not m:
        # fallback: use full doc
        body = text
    else:
        body = text[m.end():]

    # Cut off at Practice / Assignment or Recap
    cut = re.search(r"^##\s*Practice\s*/\s*Assignment\s*$|^##\s*Recap\s*$|^##\s*Recap\s*$|^##\s*Recap\s*\(", body, flags=re.MULTILINE)
    if cut:
        body = body[: cut.start()]

    # Remove section headings like "### 1) Hook..." but keep content following them.
    # We'll just strip lines that start with ### or ####
    cleaned_lines = []
    for line in body.splitlines():
        if re.match(r"^###\s+", line.strip()):
            continue
        if re.match(r"^####\s+", line.strip()):
            continue
        # remove "On screen:" label lines but keep the spoken text that follows
        # If a line starts with "On screen:" ignore it.
        if line.strip().startswith("On screen:"):
            continue
        cleaned_lines.append(line)

    # Remove extra whitespace
    cleaned = "\n".join(cleaned_lines).strip()
    # Collapse multiple blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


PDF_PAGES_DIR = REPO_ROOT / "pdf_pages"

LESSON_NAMES = {
    "01": "Introduction",
    "02": "ICT PD-Array",
    "03": "Order Blocks",
    "04": "Breaker Blocks",
    "05": "Fair Value Gap",
    "06": "Inverse FVG",
    "07": "Implied FVG & BPR",
    "08": "Rejection Block",
    "09": "Vacuum Block",
    "10": "Mitigation Block",
    "11": "Buy & Sell Side Liquidity",
    "12": "High/Low Resistance & Internal/External Range",
    "13": "Liquidity Pool, Void, Sweep & Run",
    "14": "Weekly Profiles",
    "15": "Daily Bias",
    "16": "Intraday Profiles",
    "17": "Advanced Market Structure",
    "18": "Market Maker Models & Judas Swing",
    "19": "IRL to ERL & HRLR to LRLR",
    "20": "AMD, MSS, CISD & Turtle Soup",
    "21": "Asian Range & ICT Macros",
    "22": "Silver Bullet & Kill Zones",
    "23": "Bonus Lecture: 2024 Model",
    "24": "Risk Management",
}


def make_pdf_slides(lesson_id: str, lesson_dir: Path) -> list[Path]:
    images_dir = lesson_dir / "images"
    ensure_dir(images_dir)

    cfg = load_config()
    lesson_pages = cfg.get("lesson_pages", {})
    page_nums = lesson_pages.get(lesson_id, [])
    if not page_nums:
        return []

    from PIL import Image, ImageDraw, ImageFont

    try:
        font_title = ImageFont.truetype("arial.ttf", 48)
        font_subtitle = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = font_title

    slide_files = []
    for idx, pnum in enumerate(page_nums, start=1):
        src = PDF_PAGES_DIR / f"page-{pnum:03d}.png"
        if not src.exists():
            continue

        page_img = Image.open(src).convert("RGB")
        pw, ph = page_img.size
        target_w, target_h = 1920, 1080
        scale = min(target_w / pw, target_h / ph)
        new_w = int(pw * scale)
        new_h = int(ph * scale)
        page_img = page_img.resize((new_w, new_h), Image.LANCZOS)

        canvas = Image.new("RGB", (target_w, target_h), (11, 15, 26))
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2
        canvas.paste(page_img, (x_offset, y_offset))

        draw = ImageDraw.Draw(canvas)
        lesson_label = lesson_id
        lesson_name = LESSON_NAMES.get(lesson_id, "")
        draw.text((40, 20), f"Lesson {lesson_label}", font=font_title, fill=(255, 255, 255))
        draw.text((40, 72), lesson_name, font=font_subtitle, fill=(0, 212, 255))

        png_path = images_dir / f"slide-{idx:02d}.png"
        canvas.save(png_path)
        slide_files.append(png_path)

    return slide_files


def make_placeholder_slides(lesson_dir: Path, narration_text: str) -> list[Path]:
    images_dir = lesson_dir / "images"
    ensure_dir(images_dir)

    from PIL import Image, ImageDraw, ImageFont

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", narration_text) if p.strip()]
    if not paragraphs:
        paragraphs = [narration_text.strip()]

    max_slides = 18
    stride = max(1, len(paragraphs) // max_slides)
    chunks = paragraphs[::stride][:max_slides]

    width = 1920
    height = 1080
    bg_color = (11, 15, 26)
    title_color = (255, 255, 255)
    accent_color = (0, 212, 255)
    body_color = (208, 215, 226)

    try:
        font_large = ImageFont.truetype("arial.ttf", 54)
        font_medium = ImageFont.truetype("arial.ttf", 36)
        font_body = ImageFont.truetype("arial.ttf", 30)
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_body = font_large

    slide_files = []
    for i, chunk in enumerate(chunks, start=1):
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        lesson_label = lesson_dir.name.upper().replace("LESSON-", "")
        draw.text((90, 40), "Lesson", font=font_large, fill=title_color)
        draw.text((420, 40), lesson_label, font=font_large, fill=accent_color)

        lines = []
        chunk_clean = re.sub(r"[ \t]+", " ", chunk)
        words = chunk_clean.split(" ")
        line: list[str] = []
        for w in words:
            if sum(len(x) for x in line) + len(w) > 90:
                lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)
        if line:
            lines.append(" ".join(line))
        lines = lines[:28]

        y = 130
        for line_text in lines:
            draw.text((90, y), line_text, font=font_body, fill=body_color)
            y += 34

        png_path = images_dir / f"slide-{i:02d}.png"
        img.save(png_path)
        slide_files.append(png_path)

    return slide_files


def build_scene_plan(lesson_dir: Path, slide_files: list[Path], fallback_per_slide: int) -> dict:
    # Create plan with constant duration per slide. Exact timestamps are handled by ffmpeg concat.
    scenes = []
    t = 0.0
    for idx, img in enumerate(slide_files, start=1):
        dur = float(fallback_per_slide)
        scenes.append(
            {
                "index": idx,
                "start": t,
                "duration": dur,
                "image": img.name,
            }
        )
        t += dur

    plan = {"scenes": scenes}
    (lesson_dir / "scenes").mkdir(parents=True, exist_ok=True)
    (lesson_dir / "scenes" / "scene_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return plan


async def tts_edge_to_mp3(text: str, out_mp3: Path, voice: str) -> None:
    if edge_tts is None:
        raise RuntimeError(
            "edge_tts python package not installed. Install with: pip install edge-tts"
        )
    ensure_dir(out_mp3.parent)
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%", pitch="+0Hz", volume="+0%")
    out_tmp = out_mp3.with_suffix(".tmp.mp3")
    if out_tmp.exists():
        out_tmp.unlink()

    with out_tmp.open("wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

    out_tmp.replace(out_mp3)


def render_mp4(lesson_dir: Path, slide_pngs: list[Path], audio_path: Path, out_mp4: Path, canvas: Canvas) -> None:
    images_dir = lesson_dir / "images"
    ensure_dir(out_mp4.parent)

    # Create slideshow video from image sequence (constant framerate)
    # We'll assume placeholder constant duration determined by slide count:
    # total video length must match audio length; for simplicity, we loop/truncate by -shortest.
    # Set per-frame duration: use 1 fps * duration? We’ll use -framerate equal to 1/slide_duration seconds.
    # With fixed fallback, approximate:
    # Determine duration from audio
    audio_dur = get_audio_duration_seconds(audio_path)

    slide_count = len(slide_pngs)
    per_slide = max(1.0, audio_dur / slide_count) if slide_count else audio_dur

    # -framerate for images to display: frames per second = 1 / per_slide
    fps = 1.0 / per_slide
    # But ffmpeg expects rational; pass as float
    tmp_video = out_mp4.with_suffix(".tmp.mp4")

    # Use concat demuxer list for exact ordering with -loop? easiest with image2 pattern:
    # slide-01.png ... slide-NN.png
    # Ensure filenames are sequential
    pattern = str((images_dir / "slide-%02d.png").resolve())

    cmd_vid = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-framerate",
        str(fps),
        "-i",
        pattern,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        str(tmp_video),
    ]
    subprocess.run(cmd_vid, check=True)

    # Mux audio
    cmd_mux = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(tmp_video),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        str(out_mp4),
    ]
    subprocess.run(cmd_mux, check=True)
    if tmp_video.exists():
        tmp_video.unlink()


def get_audio_duration_seconds(audio_path: Path) -> float:
    # ffprobe
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ]
    out = subprocess.check_output(cmd).decode("utf-8").strip()
    return float(out)


def build_lesson(lesson_id: str, canvas: Canvas, voice: str, placeholder_slide_duration: int) -> None:
    lesson_dir = COURSE_ROOT / f"lesson-{lesson_id}"
    ensure_dir(lesson_dir)

    src_md = REPO_ROOT / "scripts" / f"lesson-{lesson_id}-*.md"
    # Read content for extraction
    lesson_md = read_lesson_script(lesson_id)
    narration = extract_narration_text(lesson_md)

    voice_dir = lesson_dir / "voice"
    images_dir = lesson_dir / "images"
    video_dir = lesson_dir / "video"
    scenes_dir = lesson_dir / "scenes"
    ensure_dir(voice_dir)
    ensure_dir(images_dir)
    ensure_dir(video_dir)
    ensure_dir(scenes_dir)

    voice_script = voice_dir / "voice_script.txt"
    voice_script.write_text(narration, encoding="utf-8")

    audio_path = voice_dir / "audio.mp3"
    if not audio_path.exists():
        import asyncio

        if edge_tts is None:
            raise RuntimeError(
                "edge_tts is not installed. Install it: pip install edge-tts"
            )
        asyncio.run(tts_edge_to_mp3(narration, audio_path, voice=voice))
    else:
        print(f"[skip] audio exists: {audio_path}")

    # Use PDF page images as slides when available, fallback to placeholder text slides
    pdf_slides = make_pdf_slides(lesson_id, lesson_dir)
    if pdf_slides:
        slide_pngs = pdf_slides
        print(f"[slides] {len(slide_pngs)} PDF page slides for lesson {lesson_id}")
    else:
        slide_pngs = make_placeholder_slides(lesson_dir, narration)
        print(f"[slides] {len(slide_pngs)} placeholder slides for lesson {lesson_id}")
    build_scene_plan(lesson_dir, slide_pngs, fallback_per_slide=placeholder_slide_duration)

    out_mp4 = video_dir / f"lesson-{lesson_id}.mp4"
    if not out_mp4.exists():
        render_mp4(lesson_dir, [Path(p) for p in slide_pngs], audio_path, out_mp4, canvas)
    else:
        print(f"[skip] video exists: {out_mp4}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Build lessons 01-10")
    parser.add_argument("--lesson", type=str, default=None, help="Lesson number (e.g., 1 or 01)")
    args = parser.parse_args()

    cfg = load_config()
    canvas = Canvas(
        width=int(cfg["canvas"]["width"]),
        height=int(cfg["canvas"]["height"]),
        fps=int(cfg["canvas"]["fps"]),
    )
    placeholder_dur = int(cfg.get("generation", {}).get("slideDurationSecondsFallback", 6))

    voice = parse_voice_settings()

    ensure_dir(COURSE_ROOT)

    if args.all:
        ids = [f"{i:02d}" for i in range(1, 25)]
    elif args.lesson and args.lesson.lower() == "phase2":
        ids = [f"{i:02d}" for i in range(11, 25)]
    elif args.lesson is not None:
        n = int(args.lesson)
        ids = [f"{n:02d}"]
    else:
        raise SystemExit("Provide --all or --lesson <n>")

    for lid in ids:
        print(f"=== Building lesson {lid} ===")
        build_lesson(lid, canvas=canvas, voice=voice, placeholder_slide_duration=placeholder_dur)

    print("Done.")


if __name__ == "__main__":
    main()

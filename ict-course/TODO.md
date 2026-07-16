# ICT Course — Video Course Generation TODO

- [x] Create output scaffold folder structure: `ict-course/course/` with `lesson-01` … `lesson-24` subfolders
- [x] Add course configuration: `ict-course/course_config.json` (resolution/fps/ffmpeg settings)
- [x] Add generation docs: `ict-course/COURSE_GENERATION.md` (Windows commands)
- [x] Implement generator pipeline: `ict-course/generate_course.py`
- [x] For each lesson (01–24):
  - [x] Extract narration voice script from `ict-course/scripts/lesson-XX-*.md` into `course/lesson-XX/voice/voice_script.txt`
  - [x] Generate TTS audio using Edge voice `en-US-GuyNeural` into `course/lesson-XX/voice/audio.mp3`
  - [x] Create `scene_plan.json` (timed slide list)
  - [x] Create slide images from PDF page renders (real charts/graphics from the book)
  - [x] Render MP4 using FFmpeg into `course/lesson-XX/video/lesson-XX.mp4`

## Future improvements
- [ ] Add intro/outro bumper slides
- [ ] Generate chapter markers for YouTube
- [ ] Add subtitle tracks from narration text

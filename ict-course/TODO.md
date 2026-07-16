# ICT Course — Video Course Generation TODO

- [ ] Create output scaffold folder structure: `ict-course/course/` with `lesson-01` … `lesson-10` subfolders
- [ ] Add course configuration: `ict-course/course_config.json` (resolution/fps/ffmpeg settings)
- [ ] Add generation docs: `ict-course/COURSE_GENERATION.md` (Windows commands)
- [ ] Implement generator pipeline: `ict-course/generate_course.py`
- [ ] For each lesson (01–10):
  - [ ] Extract narration voice script from `ict-course/scripts/lesson-XX-*.md` into `course/lesson-XX/voice/voice_script.txt`
  - [ ] Generate TTS audio using Edge voice `en-US-GuyNeural` into `course/lesson-XX/voice/audio.mp3` (or `.wav`)
  - [ ] Create `scene_plan.json` (timed slide list)
  - [ ] Create placeholder “width” slide images (until PDF image extraction is enabled)
  - [ ] Render MP4 using FFmpeg into `course/lesson-XX/video/lesson-XX.mp4`

# Narration / TTS Voice Settings (Edge/Bing — Male)

These settings are intended to be used by any workflow that supports **Microsoft Edge / Bing TTS** voice selection.

## Default voice (male)
- **Voice:** `en-US-DavidNeural`
- **Language:** en-US
- **Style:** Neutral / Standard
- **Suggested speaking rate:** 1.0x
- **Suggested pitch:** 0 (neutral)
- **Suggested volume:** 1.0 (neutral)

## How to use
Copy the header block from the top of each lesson file:
- `ict-course/scripts/lesson-01-introduction.md`
- ...
- `ict-course/scripts/lesson-10-mitigation-block.md`

Then pass it into your TTS pipeline (or manually set the voice to `en-US-GuyNeural` if your tool only accepts voice name).

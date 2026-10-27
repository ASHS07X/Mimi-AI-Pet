# Mimi-AI Pet

An animated ChatGPT pet build for Mimi, with a plush-style character, expressive motion states, directional poses, and sprite-sheet assets.

## Project contents

- `outputs/Pets/Mimi/mimi-spritesheet.png` — final transparent v2 atlas, 1536 x 2288 pixels.
- `outputs/Pets/Mimi/` — nine state GIFs, all-states GIF and MP4, look-direction GIF, contact sheets, and QA summary.
- `work/mimi-pet-run/` — prompts, source references, generated rows and frames, revisions, assembly scripts, and QA records.
- `work/mimi-pet-run/scripts/render_final_previews.py` — rebuilds the previews from the final atlas.

## Render the previews

Python with Pillow and FFmpeg are required. From the project root, run:

```powershell
python work/mimi-pet-run/scripts/render_final_previews.py
```

The final sprite sheet is ready to upload to ChatGPT Pets. This repository contains the pet artwork and project files, not ChatGPT's proprietary pet-rendering runtime. The generated artwork can be reused as-is; regenerating it from prompts requires an image-generation service.

## GitHub

Repository: https://github.com/ASHS07X/Mimi-AI-Pet
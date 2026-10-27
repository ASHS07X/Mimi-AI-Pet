from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
ATLAS = ROOT / "work" / "mimi-pet-run" / "final" / "spritesheet-mimi-final.png"
QA = ROOT / "work" / "mimi-pet-run" / "qa"
OUT = ROOT / "outputs" / "Pets" / "Mimi"
FRAMES = QA / "frames-final"
MP4_FRAMES = QA / "mp4-frames"

STATES = [
    ("idle", 6, [280, 110, 110, 140, 140, 320]),
    ("running-right", 8, [120] * 7 + [220]),
    ("running-left", 8, [120] * 7 + [220]),
    ("waving", 4, [140, 140, 140, 280]),
    ("jumping", 5, [140, 140, 140, 140, 280]),
    ("failed", 8, [140] * 7 + [240]),
    ("waiting", 6, [150] * 5 + [260]),
    ("running", 6, [120] * 5 + [220]),
    ("review", 6, [150] * 5 + [280]),
]


def load_cell(atlas: Image.Image, row: int, col: int) -> Image.Image:
    x, y = col * 192, row * 208
    return atlas.crop((x, y, x + 192, y + 208)).convert("RGBA")


def write_gif(frames: list[Image.Image], durations: list[int], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    MP4_FRAMES.mkdir(parents=True, exist_ok=True)
    with Image.open(ATLAS) as opened:
        atlas = opened.convert("RGBA")

    all_frames: list[Image.Image] = []
    all_durations: list[int] = []
    rows: dict[str, list[Image.Image]] = {}
    for row, (state, count, durations) in enumerate(STATES):
        row_dir = FRAMES / state
        row_dir.mkdir(parents=True, exist_ok=True)
        rows[state] = []
        for col in range(count):
            frame = load_cell(atlas, row, col)
            frame.save(row_dir / f"{col:02d}.png")
            rows[state].append(frame)
        write_gif(rows[state], durations, OUT / f"mimi-{state}.gif")
        all_frames.extend(rows[state])
        all_durations.extend(durations)

    write_gif(all_frames, all_durations, OUT / "mimi-all-states.gif")
    idle = rows["idle"]
    jump = rows["jumping"]
    transition = idle + jump + idle[-2:0:-1]
    transition_durations = [280, 110, 110, 140, 140, 320] + [140, 140, 140, 140, 280] + [140, 110, 110, 280]
    write_gif(transition, transition_durations, OUT / "mimi-idle-jump-idle.gif")

    directions = [load_cell(atlas, 9 + (i // 8), i % 8) for i in range(16)]
    write_gif(directions, [170] * len(directions), OUT / "mimi-look-loop.gif")

    # Four labeled, native-size stills from the final atlas.
    selected = [("Idle", idle[0]), ("Greeting", rows["waving"][0]), ("Working", rows["running"][2]), ("Waiting", rows["waiting"][2])]
    tile_w, tile_h = 288, 288
    montage = Image.new("RGB", (tile_w * 2, tile_h * 2), "#f3f1ef")
    draw = ImageDraw.Draw(montage)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for idx, (label, frame) in enumerate(selected):
        x, y = (idx % 2) * tile_w, (idx // 2) * tile_h
        scaled = frame.resize((216, 234), Image.Resampling.LANCZOS)
        matte = Image.new("RGBA", scaled.size, "#f3f1ef")
        matte.alpha_composite(scaled)
        montage.paste(matte.convert("RGB"), (x + 36, y + 16))
        draw.text((x + 14, y + 8), label, fill="#3a2a25", font=font)
    montage.save(OUT / "mimi-motion-stills.png")

    # Create an MP4 copy of the all-state loop on a white matte.
    for path in MP4_FRAMES.glob("*.png"):
        path.unlink()
    frame_index = 0
    white = Image.new("RGBA", (192, 208), "white")
    for frame, duration in zip(all_frames, all_durations):
        matte = Image.alpha_composite(white, frame).convert("RGB")
        copies = max(1, round(duration / 125))
        for _ in range(copies):
            matte.save(MP4_FRAMES / f"{frame_index:05d}.png")
            frame_index += 1
    ffmpeg = subprocess.run(["where.exe", "ffmpeg"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-framerate", "8", "-i", str(MP4_FRAMES / "%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT / "mimi-all-states.mp4")],
        check=True,
    )

    # Save the final encoded atlas and labeled QA sheets beside the previews.
    import shutil
    shutil.copy2(ATLAS, OUT / "mimi-spritesheet.png")
    shutil.copy2(QA / "contact-sheet-final.png", OUT / "mimi-contact-sheet.png")
    shutil.copy2(QA / "direction-qa-final.png", OUT / "mimi-directions.png")
    shutil.copy2(QA / "pet-quality-final.json", OUT / "mimi-quality-report.json")
    print(f"Rendered {len(all_frames)} standard frames; wrote previews and final assets to {OUT}")


if __name__ == "__main__":
    main()

# Waiting row QA

- Result: PASS; six frames extracted and the bundled inspector reports `ok: true` with no errors or warnings.
- Visual review: Mimi remains recognizable across all frames (white plush, brown ears, pink bow, glossy eyes, pink cheeks and mouth, brown bowtie). The raised paw by the cheek and gentle head tilts read as attentive and curious, with patient, subtle motion. No text, hearts, props, shadow, or floating effects are present.
- Registration: all six frames share a 192x208 canvas and a common bottom baseline (bbox bottom y=203); scale and placement remain stable through the tilt.

- Strip: `decoded/waiting.png`
- Extracted frames: `qa/rows/waiting/frames/waiting/00.png` through `05.png`
- Inspection report: `qa/rows/waiting/review.json`
- Extraction manifest: `qa/rows/waiting/frames/frames-manifest.json`

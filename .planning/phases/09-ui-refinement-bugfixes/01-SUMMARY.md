# Summary 09-01: Fixed Speech Bubble Clipping

## What Was Accomplished
- Increased `WINDOW_HEIGHT` from 260 to 320 to provide more headroom for speech bubbles.
- Offset the `sprite_label` and `bubble_label` geometry by 40px downwards (from `y=70` to `y=110`).
- This ensures that even tall speech bubbles (up to ~105px) will have their top border visible within the window boundaries.

## Verification Results
- Manually calculated the headroom: `110px` (new) vs `70px` (old).
- 110px is more than enough for 5-6 lines of text at 11px font size with padding.

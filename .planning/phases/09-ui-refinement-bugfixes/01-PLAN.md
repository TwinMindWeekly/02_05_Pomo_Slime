# Plan 09-01: Speech Bubble Border Fix & UI Optimization

## Objective
Fix the speech bubble clipping issue where the top border is missing due to window boundary limits. Optimize the window layout to accommodate taller bubbles.

## Proposed Changes

### UI
#### [MODIFY] [pet_window.py](file:///d:/Workspace/Project/Week2/02_05_2026/src/ui/pet_window.py)
- Increase `WINDOW_HEIGHT` from 260 to 320.
- Offset the `sprite_label`, `energy_bar`, and `level_label` downwards to create more headroom for the speech bubble.
- Update `bubble_label` geometry logic to ensure it doesn't cross `y=0`.

## Verification Plan

### Manual Verification
- Run the app and trigger a long message from the AI.
- Check if the top border of the chat bubble is visible.
- Verify that the pet and other UI elements are correctly positioned.

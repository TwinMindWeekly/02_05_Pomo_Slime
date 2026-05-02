# Plan 10-01: Custom Title Bar & Frameless Settings Window

## Objective
Transform the Settings Window into a modern, frameless window with a custom title bar that matches the PomoSlime aesthetic.

## Proposed Changes

### UI Components
#### [NEW] [modern_title_bar.py](file:///d:/Workspace/Project/Week2/02_05_2026/src/ui/components/modern_title_bar.py)
- A reusable component for custom title bars.
- Includes window title, icon, and custom Close button.
- Handles window dragging logic.

#### [MODIFY] [settings_window.py](file:///d:/Workspace/Project/Week2/02_05_2026/src/ui/settings_window.py)
- Set window to `FramelessWindowHint`.
- Add `ModernTitleBar` at the top of the main layout.
- Adjust layout margins and padding for a cleaner look.
- Implement rounded corners for the entire window using stylesheets and `WA_TranslucentBackground`.

## Verification Plan

### Manual Verification
- Open Settings window.
- Verify it is frameless and has rounded corners.
- Drag the window using the custom title bar.
- Close the window using the custom close button.

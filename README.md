PygameLikeGlslScreen - resizeable screen using moderngl
==================================================

## Description:
A Python library that combines Pygame's API with moderngl shaders with automatic screen resizing and standardized mouse coordinates accrose diffrent screen sizes.

## Requirements:
- Python 3.7+
- pygame-ce
- moderngl
- pyautogui

## Installation:
1. Download and unzip the project files
2. Install Python and pip if not already installed
3. Open Command Prompt and run:
   ```pip install pygame-ce moderngl pyautogui```
   or use build.bat (!! build.bat will uninstall pyagme and install pyagme-ce !!)

## Running the Demo:
1. Navigate to project folder in Command Prompt:
   cd YOUR_PROJECT_FOLDER_PATH
2. Run the demo:
   python demo.py

## API Features:
- moderngl-accelerated rendering with custom shader support
- Automatic screen resizing and fullscreen toggle
- Standardized mouse coordinates across resolutions
- Pygame-compatible drawing methods (fill, blit)
- Custom vertex and fragment shader loading
- Texture management with RGBA support
- Useg of 
```
(0, 0) is the TOP-LEFT corner of the screen/window
X-axis increases to the RIGHT
Y-axis increases DOWNWARD
```

## Mouse Handling System:

   ### Access the mouse object through:
   screen.mouse_handler.mouse
   
   ### Available mouse properties:
   - mouse.pos - (x, y) position tuple
   - mouse.x - X coordinate
   - mouse.y - Y coordinate
   - mouse.state.left - Left button pressed state
   - mouse.state.middle - Middle button pressed state
   - mouse.state.right - Right button pressed state
   - mouse.clicked.down.left - Left button pressed this frame
   - mouse.clicked.down.middle - Middle button pressed this frame
   - mouse.clicked.down.right - Right button pressed this frame
   - mouse.clicked.up.left - Left button released this frame
   - mouse.clicked.up.middle - Middle button released this frame
   - mouse.clicked.up.right - Right button released this frame

## Key Methods:
- PygameLikeGlslScreen(size, title) - Initialize screen
- fill(color) - Fill background color
- blit(image, position) - Draw images
- display_flip() - Render frame with shaders (automatically updates mouse)
- change_fullscreen_state() - Toggle fullscreen
- change_frag_shader(path) - Load custom fragment shader
- change_vert_shader(path) - Load custom vertex shader

## Important Notes:
- Mouse coordinates are automatically scaled to original screen size
- Call screen.mouse_handler.change_stored_current_screen_size() on VIDEORESIZE events
- display_flip() automatically calls mouse_handler.tick() to update mouse state
- Mouse click detection works on frame-by-frame basis

## Shader Support:
- Load custom GLSL shaders from files
- Built-in basic vertex/fragment shaders provided
- Supports OpenGL 3.3 core profile

## Controls:
- Press any key to toggle fullscreen
- Close window to exit program
- Window can be resized manually

# The library maintains Pygame coordinate system compatibility while providing modelgl acceleration and consistent input handling across different screen sizes with proper scaling.

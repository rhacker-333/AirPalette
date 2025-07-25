
# AirPalette

  A Python virtual painting tool that lets you draw, select colors/tools, and erase using only **hand gestures** and your **webcam** — no keyboard or mouse required! Built with OpenCV and custom hand-tracking logic.

  ## Features

  - **Draw, erase, and select tools** using intuitive hand gestures.
  - **Customizable color toolbar** with overlay images.
  - **Works on any screen size** — UI auto-scales.
  - **Visual feedback** for active tool, FPS, and detected mode (PAINT/SELECT).
  - **Fully touchless** — just wave your hand and paint!


  <img width="1273" height="717" alt="image" src="https://github.com/user-attachments/assets/3fa46370-12aa-4f5a-96d8-2fbc5526e0f1" />
  
  <img width="1277" height="711" alt="image" src="https://github.com/user-attachments/assets/e82b790c-c821-4508-ab16-e2b47395c91b" />

  <img width="1273" height="713" alt="image" src="https://github.com/user-attachments/assets/543bc677-1f31-40ce-ace8-885220521d32" />

  <img width="1274" height="721" alt="image" src="https://github.com/user-attachments/assets/83c3f9a2-5381-40f7-b5e4-59b9a2a5ebd7" />

  <img width="1271" height="715" alt="image" src="https://github.com/user-attachments/assets/47ff2633-5bad-434c-b634-0d295ba6bed0" />

  <img width="1262" height="713" alt="image" src="https://github.com/user-attachments/assets/bd9bf9bb-03a6-49f1-ba5f-fdaa6cc0bdae" />



  ## Installation & Setup

  ### 1. Clone the repository

### 2. Set up your Python environment (recommended)


### 3. Install dependencies


Main dependencies:
- opencv-python
- numpy
- pyautogui
- (optionally: mediapipe, if used in helpers/track_hands.py)

### 4. Prepare the header images

- Place at least **5 images** (e.g., 1.png, 2.png, …, 5.png) inside the `header_images/` directory.
- These are used for your color/tool/eraser toolbar.

### 5. Ensure hand-tracking helper exists

- Confirm the presence of `helpers/track_hands.py` for hand and finger landmark detection.

### 6. Run the app


## Usage

- **Select a tool/color:** Hold up both index and middle fingers. Move your hand to the color/tool region at the top. The app will switch tools when your fingers "touch" those regions.
- **Draw:** Only index finger up. Draw by waving your hand.
- **Erase:** Select the eraser tool then draw as usual.
- **Exit:** Press `Esc`, `q`, or close the app window.


## Troubleshooting

- **Webcam not detected?**  
  Check your webcam is connected and not used by other software.
- **No hand detection?**  
  Ensure mediapipe (if required) is installed; check for good lighting.
- **No overlay/toolbar images?**  
  Fill the `header_images/` directory with valid PNG/JPG files.

## Customization

- Change brush/eraser sizes or default colors in `main.py`.
- Update toolbar icons by replacing images in `header_images/`.
- Tweak hand gesture logic in `helpers/track_hands.py`.

## License

MIT License *(replace or adapt as needed).*

## Acknowledgments

- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [pyautogui](https://pyautogui.readthedocs.io/)
- [MediaPipe](https://google.github.io/mediapipe/) (if used)
- The open source community!

**Happy painting!** ✋🎨  
Just wave your hand and start creating!




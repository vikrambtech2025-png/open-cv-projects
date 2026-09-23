# OpenCV Projects

A collection of standalone computer-vision experiments built with **OpenCV** and **NumPy** — real-time face detection, authorized-face matching, and hand-gesture segmentation from a webcam feed.

## Projects

| Script | What it does |
|---|---|
| `face recognition.py` | Real-time face detection using Haar cascades — draws bounding boxes and labels on the live webcam feed (press `q` to quit). |
| `gender dtector.py` | Authorized-face check — matches a live face against stored student reference images (`students/<email>.jpg`) using pixel-difference similarity. |
| `hand gesture recognition .py` | Hand-gesture detection by skin-color segmentation (HSV) inside a region of interest, overlaid on the live feed. |

## Getting started

```bash
pip install opencv-python numpy
```

Run any script standalone, for example:

```bash
python "face recognition.py"
```

## Notes

- A webcam is required; press `q` in the preview window to stop the feed.
- Haar cascade files ship with OpenCV (`cv2.data.haarcascades`).
- The authorized-face script reads reference images from a `students/` folder (one `*.jpg` per email) and can be wired into a CGI form handler.

## License

No license specified — for learning/reference use.
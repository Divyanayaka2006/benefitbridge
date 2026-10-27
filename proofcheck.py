# proofcheck.py - is an uploaded proof file readable?
# This does NOT check whether a document is genuine. It only looks at the
# picture itself: can it be opened, is it big enough, bright enough and sharp.
import io

import numpy as np
from PIL import Image, ImageOps

MIN_LONG_SIDE = 800    # pixels; smaller photos are too small to read
MIN_BRIGHTNESS = 60    # average grey level 0-255; lower is too dark
BLUR_LIMIT = 30.0     # edge-sharpness score; lower is blurry (tune on real photos)


def sharpness(gray):
    """Variance of the Laplacian: high for sharp pictures, low for blurry ones."""
    a = gray.astype("float32")
    lap = (-4 * a[1:-1, 1:-1] + a[:-2, 1:-1] + a[2:, 1:-1]
           + a[1:-1, :-2] + a[1:-1, 2:])
    return float(lap.var())


def check_proof(data, filename):
    """Return one of: "ok", "pdf", "small", "dark", "blur", "bad"."""
    if filename.lower().endswith(".pdf"):
        return "pdf" if data[:4] == b"%PDF" else "bad"
    try:
        img = Image.open(io.BytesIO(data))
        img = ImageOps.exif_transpose(img).convert("L")
    except Exception:
        return "bad"
    if max(img.size) < MIN_LONG_SIDE:
        return "small"
    img.thumbnail((1000, 1000))          # same scale for every photo
    gray = np.asarray(img)
    if gray.mean() < MIN_BRIGHTNESS:
        return "dark"
    if sharpness(gray) < BLUR_LIMIT:
        return "blur"
    return "ok"

# checkphoto.py - see the numbers behind the readability check for one photo.
# Usage:  python checkphoto.py "C:\path\to\photo.jpg"
import sys

import numpy as np
from PIL import Image, ImageOps

from proofcheck import BLUR_LIMIT, MIN_BRIGHTNESS, MIN_LONG_SIDE, check_proof, sharpness

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    # No path typed: open a window where you can pick the photo
    from tkinter import Tk, filedialog
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Choose a photo", filetypes=[("Images", "*.jpg *.jpeg *.png")])
    if not path:
        sys.exit("No photo chosen.")
with open(path, "rb") as f:
    data = f.read()

img = ImageOps.exif_transpose(Image.open(path)).convert("L")
print(f"Size: {img.size[0]} x {img.size[1]} pixels (needs the long side >= {MIN_LONG_SIDE})")
img.thumbnail((1000, 1000))
gray = np.asarray(img)
print(f"Brightness: {gray.mean():.0f} (needs >= {MIN_BRIGHTNESS})")
print(f"Sharpness: {sharpness(gray):.0f} (needs >= {BLUR_LIMIT:.0f})")
print("Verdict:", check_proof(data, path))
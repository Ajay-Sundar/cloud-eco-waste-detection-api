from PIL import Image
from pathlib import Path

src = Path("test_images/sample4.jpg")
dst = Path("test_images/benchmark_sample.jpg")

img = Image.open(src).convert("RGB")
img.thumbnail((800, 800))
img.save(dst, "JPEG", quality=80, optimize=True)

print("Saved:", dst)
print("Size MB:", dst.stat().st_size / 1024 / 1024)
print("Resolution:", Image.open(dst).size)
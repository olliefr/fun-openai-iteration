import base64
import os
import sys
from pathlib import Path
from openai import OpenAI

if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} n input_file\nWhere n>=1 is number of steps to make,\ninput_file is the input image file name.")
    sys.exit(1)

n = int(sys.argv[1])
assert n >= 1

p = Path(sys.argv[2])
assert p.is_file()
assert p.suffix in [".jpg", ".png"]
assert len(p.stem) >= 3 # "i-0"
assert "-" in p.stem

parts = p.stem.split("-")
fname = parts[0]
k = int(parts[1]) # starting number
w = len(parts[1]) # field width (1, 01, 001)

# sys.exit(0)

assert "OPENAI_API_KEY" in os.environ

client = OpenAI()

prompt = """
Create an exact replica of the reference image, don't change a thing.
"""

while n > 0:
    result = client.images.edit(
        model="gpt-image-1",
        image=[
            p.with_stem(f"{fname}-{k:0{w}}").open("rb")
        ],
        prompt=prompt,
        quality='high',
        size='1024x1024',
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with p.with_stem(f"{fname}-{k+1:0{w}}").open("wb") as f:
        f.write(image_bytes)
    
    k += 1
    n -= 1

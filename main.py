import base64
import sys
from openai import OpenAI

if len(sys.argv) not in [2, 3]:
    print(f"usage: {sys.argv[0]} k [n]\nWhere k>=0 is the step to start from, n (optional) number of steps to make.")
    sys.exit(1)
k = int(sys.argv[1])
n = 1
if len(sys.argv) == 3:
    n = int(sys.argv[2])
assert k >= 0
assert n >= 1

client = OpenAI()

prompt = """
Create an exact replica of the reference image, don't change a thing.
"""

while n > 0:
    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open(f"oliver/oliver-{k}.jpg", "rb"),
        ],
        prompt=prompt,
        quality='high',
        size='1024x1024',
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(f"oliver/oliver-{k+1}.jpg", "wb") as f:
        f.write(image_bytes)
    
    k += 1
    n -= 1

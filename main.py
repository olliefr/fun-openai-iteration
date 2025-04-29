import base64
import sys
from openai import OpenAI

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} k; where k>=0 is the step to start from")
    sys.exit(1)
k = int(sys.argv[1])

rpm = 5

client = OpenAI()

prompt = """
Create an exact replica of the reference image, don't change a thing.
"""

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

# Save the image to a file
with open(f"oliver/oliver-{k+1}.jpg", "wb") as f:
    f.write(image_bytes)

import os
import uuid

# Use safe writable directory for Render / Docker / VPS
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")

# Ensure directory exists safely
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(content: bytes):
    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(content)

    return path
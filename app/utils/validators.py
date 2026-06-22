import imghdr


def is_image(file_bytes: bytes) -> bool:
    return imghdr.what(None, h=file_bytes) is not None


def validate_size(file_bytes: bytes, max_mb: int = 10):
    return len(file_bytes) <= max_mb * 1024 * 1024
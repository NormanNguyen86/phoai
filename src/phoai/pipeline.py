import argparse
import sys
from pathlib import Path


def verify_image_path(img_path):
    # Check if the image path is exist and is a valid image file
    if not img_path.exists():
        raise ValueError(f"Image path '{img_path}' does not exist")
    if not img_path.is_file():
        raise ValueError(f"Image path '{img_path}' is not a file")

    valid_extensions = [".jpg", ".jpeg", ".png"]
    if not any(img_path.suffix.lower() == ext for ext in valid_extensions):
        raise ValueError(
            "Invalid image file extension. Supported extensions are: "
            + ", ".join(valid_extensions)
        )


def read_image(img_path):
    # Just try to read by Path.stat().st_size
    size = img_path.stat().st_size
    if size == 0:
        raise ValueError("Image file is empty")
    return size


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=Path, help="Path to the input image")
    arg = parser.parse_args()
    try:
        verify_image_path(arg.img_path)
        image_size = read_image(arg.img_path)
        print(f"Image path '{arg.img_path}' is valid and size: {image_size} bytes")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

from pathlib import Path

import pytest

from phoai.pipeline import read_image, verify_image_path


# Test case 1: Test that verify_image_path raises ValueError for a non-existent path
def test_missing_path_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        verify_image_path(tmp_path / "nope.jpg")


# Test case 2: Test that verify_image_path raises ValueError for a directory path
def test_directory_path_raises(tmp_path: Path) -> None:
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    with pytest.raises(ValueError, match="is not a file"):
        verify_image_path(dir_path)


# Test case 3: Test that verify_image_path raises ValueError for an invalid file extension
def test_invalid_extension_raises(tmp_path: Path) -> None:
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("This is a test file.")
    with pytest.raises(ValueError, match="Invalid image file extension"):
        verify_image_path(invalid_file)


# Test case 4: Test that verify_image_path does not raise an error for a valid image file (.JPG, .JPEG, .PNG)
def test_valid_extensions(tmp_path: Path) -> None:
    valid_extensions = [".JPG", ".JPEG", ".PNG", ".jpg", ".jpeg", ".png"]
    for ext in valid_extensions:
        valid_file = tmp_path / f"test{ext}"
        valid_file.write_bytes(b"\x89PNG\r\n\x1a\n")  # Write a minimal PNG header
        verify_image_path(valid_file)


# Test case 5: Test that read_image raises ValueError for an empty image file
def test_empty_image_file_raises(tmp_path: Path) -> None:
    empty_file = tmp_path / "empty.jpg"
    empty_file.touch()  # Create an empty file
    with pytest.raises(ValueError, match="Image file is empty"):
        read_image(empty_file)


# Test case 6: Correctly handle a valid image file with a supported extension and non-zero size
def test_valid_image_file(tmp_path: Path) -> None:
    valid_file = tmp_path / "valid_image.jpg"
    valid_file.write_bytes(b"\x89PNG\r\n\x1a\n")
    verify_image_path(valid_file)
    size = read_image(valid_file)
    assert size > 0, "Image file size should be greater than zero"

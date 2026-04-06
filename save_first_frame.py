#!/usr/bin/env python3
"""Save the first frame of a video as an image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def save_with_opencv(video_path: Path, output_path: Path) -> bool:
    try:
        import cv2  # type: ignore
    except ImportError:
        return False

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    ok, frame = capture.read()
    capture.release()

    if not ok or frame is None:
        raise RuntimeError(f"Could not read the first frame from: {video_path}")

    if not cv2.imwrite(str(output_path), frame):
        raise RuntimeError(f"Could not write image: {output_path}")

    return True


def save_with_imageio(video_path: Path, output_path: Path) -> bool:
    try:
        import imageio.v3 as iio  # type: ignore
    except ImportError:
        return False

    frame = iio.imread(video_path, index=0)
    iio.imwrite(output_path, frame)
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save the first frame of a video as a PNG image."
    )
    parser.add_argument(
        "video",
        nargs="?",
        default="BBQ-ICRA.mp4",
        help="Path to the source video. Default: BBQ-ICRA.mp4",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="BBQ-ICRA-first-frame.png",
        help="Path to the output image. Default: BBQ-ICRA-first-frame.png",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    video_path = Path(args.video)
    output_path = Path(args.output)

    if not video_path.exists():
        print(f"Video not found: {video_path}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    for saver in (save_with_opencv, save_with_imageio):
        if saver(video_path, output_path):
            print(f"Saved first frame to {output_path}")
            return 0

    print(
        "Missing dependency. Install either 'opencv-python' or 'imageio[ffmpeg]' and try again.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

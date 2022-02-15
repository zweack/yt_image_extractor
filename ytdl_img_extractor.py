"""Downloads YouTube video and extracts video frames as a collection of image files."""
import argparse
import sys
import uuid
from pathlib import Path

import cv2
from yt_dlp import YoutubeDL, utils

# Base directory path
parent = Path(__file__).resolve().parent


class VideoProcessor:
    """Main processor."""

    def __init__(self):
        """Setup video and image directories."""
        self.video = parent.joinpath(str(uuid.uuid1()))
        self.images = self.video.joinpath("Images")

    def download_video(self, url: str, small=None, fps=None):
        """Youtube video downloader."""
        if small:
            ydl_opts = {"format": "worst", "outtmpl": f"{self.video}/%(title)s.%(ext)s"}
        else:
            ydl_opts = {"format": "best", "outtmpl": f"{self.video}/%(title)s.%(ext)s"}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except utils.DownloadError:
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()
        else:
            self.video.mkdir(parents=True, exist_ok=True)
            self.images.mkdir(parents=True, exist_ok=True)
            self.extract_images(fps)

    def extract_images(self, fps: int):
        """Extract video frames from file."""
        video_file = "".join([str(vidobj) for vidobj in self.video.iterdir() if vidobj.is_file()])
        video_capture = cv2.VideoCapture(video_file)
        length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        success, image = video_capture.read()
        count = 0
        while success:
            success, image = video_capture.read()
            if not success:
                break
            try:
                if count % fps == 0:
                    filename = self.images.joinpath(f"frame_{str(count)}.jpg")
                    cv2.imwrite(str(filename), image)
                    print(f"[processing frame] {count}/{length}", end="\r")
                count += 1
            except KeyboardInterrupt:
                sys.exit()
        print("\n[completed]")


def check_value(arg):
    """Ensure the FPS is a positive int value."""
    num = int(arg)
    if num <= 0:
        raise argparse.ArgumentTypeError("argument must be a positive integer value")
    return num


def main():
    """Argument parser/main function."""
    fps_rate = 30
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="youtube url")
    parser.add_argument(
        "-s",
        "--small",
        action="store_true",
        help="download lowest quality video (smaller size video)",
    )
    parser.add_argument(
        "-f",
        dest="fps",
        metavar="N",
        nargs="?",
        type=check_value,
        default=fps_rate,
        help="images to capture per frame (default is 30 = 1 image per 30 frames)",
    )
    args = parser.parse_args()

    vidp = VideoProcessor()
    vidp.download_video(args.url, args.small, args.fps)


if __name__ == "__main__":
    BANNER = """
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    """
    print(BANNER)

    main()

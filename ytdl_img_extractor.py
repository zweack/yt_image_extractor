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
        """
        Downloads a video from a given url and saves it in a folder called "video" in the current
        directory.

        :param url: The URL of the video you want to download
        :type url: str
        :param small: If True, the video will be downloaded in the worst quality
        :param fps: Frames per second
        """
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
        """
        Extract video frames from file.

        :param fps: frames per second
        :type fps: int
        """
        vidfile = "".join([str(vidobj) for vidobj in self.video.iterdir() if vidobj.is_file()])
        vidcap = cv2.VideoCapture(vidfile)
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        count = 0
        while True:
            ret, frame = vidcap.read()
            if not ret:
                break
            try:
                if count % fps == 0:
                    filename = self.images.joinpath(f"frame_{str(count)}.jpg")
                    cv2.imwrite(str(filename), frame)
                    print(f"[processing frame] {count}/{length}", end="\r")
                count += 1
            except KeyboardInterrupt:
                vidcap.release()
                sys.exit()
        print("\n[completed]")
        vidcap.release()


def check_value(arg):
    """
    Takes a string argument, converts it to an integer, and then checks to see if it's a positive
    integer. If it is, it returns the integer. If it's not, it raises an error. This ensures the
    FPS is a positive int value.

    :param arg: The argument to be checked
    :return: the value of the argument.
    """
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

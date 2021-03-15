import argparse
import sys
import uuid
from pathlib import Path

import cv2
import youtube_dl

# Base directory path
parent = Path(__file__).resolve().parent


class Video_Processor:
    def __init__(self):
        self.video = parent.joinpath(str(uuid.uuid1()))
        self.images = self.video.joinpath("Images")

        self.video.mkdir(parents=True, exist_ok=True)
        self.images.mkdir(parents=True, exist_ok=True)

    def download_video(self, url, small=None, fps=None):
        try:
            if small:
                opts = {
                    "format": "worst",
                    "outtmpl": f"{self.video}/%(title)s.%(ext)s",
                }
            else:
                opts = {
                    "outtmpl": f"{self.video}/%(title)s.%(ext)s",
                }

            with youtube_dl.YoutubeDL(opts) as ydl:
                ydl.download([url])

            self.extract_images(fps)
        except Exception as exc:
            print(f"[download error] {exc}")

    def extract_images(self, fps):
        vidfile = "".join([str(x) for x in self.video.iterdir() if x.is_file()])
        vidcap = cv2.VideoCapture(vidfile)
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        success, image = vidcap.read()
        count = 0

        while success:
            success, image = vidcap.read()
            if not success:
                break
            try:
                if count % fps == 0:
                    fname = self.images.joinpath(f"frame_{str(count)}.jpg")
                    cv2.imwrite(str(fname), image)
                    print(f"[processing frame] {count}/{length}", end="\r")
                count += 1
            except KeyboardInterrupt:
                sys.exit()
        print("\n[completed]")


def main(url, small, fps):
    vp = Video_Processor()
    vp.download_video(url, small, fps)


if __name__ == "__main__":
    banner = r"""
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    """
    print(banner)

    def check_value(arg):
        num = int(arg)
        if num <= 0:
            raise argparse.ArgumentTypeError("argument must be a positive interger value")
        return num

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="youtube url")
    parser.add_argument(
        "-s", "--small", action="store_true", help="download lowest quality video (smaller size video)"
    )
    parser.add_argument(
        "-f",
        dest="fps",
        metavar="N",
        nargs="?",
        type=check_value,
        default=30,
        help="images to capture per frame (default is 30 = 1 image per 30 frames)",
    )
    args = parser.parse_args()

    main(args.url, args.small, args.fps)

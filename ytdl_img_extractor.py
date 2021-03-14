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

    def download_video(self, url):
        try:
            ydl_opts = {"outtmpl": f"{self.video}/%(title)s.%(ext)s"}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.extract_images()
        except Exception as exc:
            print(f"[download error] {exc}")

    def extract_images(self):
        vidfile = "".join([str(x) for x in self.video.iterdir() if x.is_file()])
        vidcap = cv2.VideoCapture(vidfile)
        fps = round(int(vidcap.get(cv2.CAP_PROP_FPS)))
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


def main(url):
    vp = Video_Processor()
    vp.download_video(url)


if __name__ == "__main__":
    banner = r"""
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    """
    print(banner)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="youtube url")
    args = parser.parse_args()

    main(args.url)

# YouTube Frame/Image Extractor

![Generic badge](https://img.shields.io/badge/python-3.7-blue.svg) [![Twitter](https://img.shields.io/badge/Twitter-@pulsecode-blue.svg)](https://twitter.com/pulsecode)

Downloads YouTube video and extracts video frames as a collection of image files

## Installation

```text
git clone https://github.com/dfirsec/ytdl_img_extractor.git
cd ytdl_img_extractor
pip install -r requirements.txt
```

## Usage

```console
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+

usage: ytdl_img_extractor.py [-h] [-s] [-f [N]] url

positional arguments:
  url          youtube url

optional arguments:
  -h, --help   show this help message and exit
  -s, --small  download lowest quality video (smaller size video)
  -f [N]       images to capture per frame (default is 30 = 1 image per 30 frames)
```

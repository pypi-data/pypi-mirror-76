# Photo ID Magick

Python library to automatically align and crop your photos to the correct biometric passport photo size.

This library is based on the libraries [face_detection](https://github.com/ageitgey/face_recognition) and [Pillow](https://python-pillow.org/).

## Installation

```bash
$ pip install photoidmagick
```

## Usage

|                         |                         |                         |                         |
| ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| ![](doc/sample_003.jpg) | ![](doc/sample_005.jpg) | ![](doc/sample_009.jpg) | ![](doc/sample_011.jpg) |

|                                |                                |                                |                                |
| ------------------------------ | ------------------------------ | ------------------------------ | ------------------------------ |
| ![](doc/sample_003.square.jpg) | ![](doc/sample_005.square.jpg) | ![](doc/sample_009.square.jpg) | ![](doc/sample_011.square.jpg) |

```bash
$ photoidmagick -f sample_039.jpg -s 1750x2250
Traceback (most recent call last):
__main__.ObliqueFacePoseException: the midsagittal facial line doesn't intersect the midhorizontal iris line in the middle


$ photoidmagick -f sample_039.jpg -s 350x450 --allow-oblique-face
```

| Original                | Passport Photo Format            | Square Photo Format            |
| ----------------------- | -------------------------------- | ------------------------------ |
| ![](doc/sample_039.jpg) | ![](doc/sample_039.passport.jpg) | ![](doc/sample_039.square.jpg) |

```bash
$ photoidmagick -f sample_054.jpg -s 400x400 --allow-oblique-face
Traceback (most recent call last):
__main__.UnevenlyOpenEyelidException: the right eye is more opened than the left eye

$ photoidmagick -f sample_054.jpg -s 1000x1000 --allow-oblique-face --allow-unevenly-open-eye
```

| Original                | Passport Photo Format            | Square Photo Format            |
| ----------------------- | -------------------------------- | ------------------------------ |
| ![](doc/sample_054.jpg) | ![](doc/sample_054.passport.jpg) | ![](doc/sample_054.square.jpg) |  |

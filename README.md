# Image Collector
This program downloads images from Google Image Search.

## Environment
I tested this program on Ubuntu 20.04, but it should work on other OS's as well.

## Pre-requisite
```
pip install -r requirements.txt
```

## How to run
Move to this directory and run
```
python main.py -q [search query] -b [browser name] -n [number of images to download]
```
`-b` and `-n` can be omitted. If `-b` is ommited, it does not use a browser and use HTTP requests. The image quality is better if a browser is used. If `-n` is omitted, it downloads the maximum number it can, 20 for non-browser, 50 for Chrome and 100 for FireFox.

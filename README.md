# openprocessing

Simple tools to download single-file trending p5.js sketches from
[OpenProcessing](https://openprocessing.org).

## Install

```sh
pip install -r requirements.txt
```

## Usage

Grab the first page of trending sketches (90 IDs by default):

```sh
python scraper.py
```

To walk through every page of results use `--all`:

```sh
python scraper.py --all
```

Sketches and their metadata are stored under `./data/YYYY-MM-DD-run/` by
default. Use `-o` to choose a different output directory.

### Resuming

If the scraper stops unexpectedly, rerun it with the same `--progress`
file to skip sketches that were already processed:

```sh
python scraper.py --progress progress.txt
```

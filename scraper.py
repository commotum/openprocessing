#!/usr/bin/env python3
"""
Fetch today's 'Trending' sketches that are one‑file‑only
and store them under ./data/YYYY‑MM‑DD‑run/.
"""

import argparse
import sys
import pathlib
import logging
from tqdm import tqdm
from api import trending_ids, trending_ids_iter, sketch_code, sketch_assets
from utils import out_folder, save_sketch
from settings import DEFAULT_OUTDIR

logger = logging.getLogger(__name__)


def load_progress(path):
    p = pathlib.Path(path)
    if not p.exists():
        return set()
    return {line.strip() for line in p.read_text().splitlines()}


def record_progress(path, sketch_id):
    with open(path, "a") as fh:
        fh.write(f"{sketch_id}\n")

def is_single_file(sketch_id):
    code_arr  = sketch_code(sketch_id)
    if len(code_arr) != 1 or not code_arr[0]["filename"].endswith(".js"):
        return None
    if sketch_assets(sketch_id):          # non‑empty → has assets
        return None
    return code_arr[0]                    # qualifying code object

def main(limit, out, grab_all=False, progress="progress.txt"):
    outdir = out_folder(out)
    processed = load_progress(progress)
    kept = 0
    ids = trending_ids_iter(step=limit) if grab_all else trending_ids(limit)
    for sid in tqdm(ids):
        if str(sid) in processed:
            continue
        try:
            code_obj = is_single_file(sid)
        except Exception as exc:
            logger.error("%s: %s", sid, exc)
            continue
        if not code_obj:
            record_progress(progress, sid)
            processed.add(str(sid))
            continue
        save_sketch(sid, code_obj["filename"], code_obj, outdir)
        record_progress(progress, sid)
        processed.add(str(sid))
        kept += 1
    logger.info("\u2713 Saved %d single-file sketches to %s", kept, outdir)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Grab single‑file trending p5.js sketches")
    p.add_argument("--limit", type=int, default=90,
                   help="how many trending IDs to request per page")
    p.add_argument("--all", action="store_true",
                   help="iterate through all pages of trending IDs")
    p.add_argument("-o", "--out", default=DEFAULT_OUTDIR,
                   help="base output directory (default: ./data)")
    p.add_argument("--progress", default="progress.txt",
                   help="path to progress file for resuming runs")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        main(args.limit, args.out, grab_all=args.all, progress=args.progress)
    except KeyboardInterrupt:
        sys.exit("\nAborted.")

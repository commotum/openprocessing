#!/usr/bin/env python3
"""
Fetch today's 'Trending' sketches that are one‑file‑only
and store them under ./data/YYYY‑MM‑DD‑run/.
"""

import argparse, sys
from tqdm import tqdm
from api import trending_ids, sketch_code, sketch_assets
from utils import out_folder, save_sketch
from settings import DEFAULT_OUTDIR

def is_single_file(sketch_id):
    code_arr  = sketch_code(sketch_id)
    if len(code_arr) != 1 or not code_arr[0]["filename"].endswith(".js"):
        return None
    if sketch_assets(sketch_id):          # non‑empty → has assets
        return None
    return code_arr[0]                    # qualifying code object

def main(limit, out):
    outdir = out_folder(out)
    kept = 0
    for sid in tqdm(trending_ids(limit)):
        code_obj = is_single_file(sid)
        if not code_obj:
            continue
        save_sketch(sid, code_obj["filename"], code_obj, outdir)
        kept += 1
    print(f"\n✓ Saved {kept} single‑file sketches to {outdir}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Grab single‑file trending p5.js sketches")
    p.add_argument("--limit", type=int, default=90,
                   help="how many trending IDs to test (multiple of 30 recommended)")
    p.add_argument("-o", "--out", default=DEFAULT_OUTDIR,
                   help="base output directory (default: ./data)")
    args = p.parse_args()
    try:
        main(args.limit, args.out)
    except KeyboardInterrupt:
        sys.exit("\nAborted.")

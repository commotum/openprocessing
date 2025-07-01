import json, os, pathlib, re, datetime as dt
from slugify import slugify

def out_folder(base):
    t = dt.datetime.now().strftime("%Y‑%m‑%d‑run")
    path = pathlib.Path(base) / t
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_sketch(sketch_id, title, code_obj, outdir):
    slug = slugify(title)[:40] or "sketch"
    stem = f"{sketch_id}_{slug}"
    js_path   = outdir / f"{stem}.js"
    meta_path = outdir / f"{stem}_meta.json"

    js_path.write_text(code_obj["content"], encoding="utf‑8")

    meta = {k: code_obj.get(k) for k in ("filename","orderID")}
    meta.update({"sketch_id": sketch_id, "title": title})
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    return js_path

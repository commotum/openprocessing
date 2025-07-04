import time
from ratelimit import limits, sleep_and_retry
import requests
from requests.exceptions import JSONDecodeError, RequestException
from settings import BASE_URL, USER_AGENT, MAX_CALLS_PER_MINUTE

HEADERS = {"User-Agent": USER_AGENT}

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=60)
def _get(path, *, params=None, timeout=15, retries=3, backoff=5):
    """Polite GET wrapper that respects the 40‑req/min rule.

    Retries a few times on network errors to make the scraper more
    fault tolerant.
    """
    url = f"{BASE_URL}{path}"

    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
<<<<<<< ours
            try:
                return r.json()
            except JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from {url}") from e
        except (RequestException, ValueError):
=======
            return r.json()
        except (RequestException, JSONDecodeError) as exc:
>>>>>>> theirs
            if attempt == retries - 1:
                raise ValueError(f"Failed to retrieve JSON from {url}") from exc
            time.sleep(backoff * (attempt + 1))

# ---------- high‑level helpers ---------- #

def trending_ids(limit=90, offset=0):
    """
    Return a list of sketch IDs that the front‑end labels 'Trending'.

    Internally the site calls:
        /api/sketches?sort=trending&limit=…&offset=…
    (confirmed via DevTools, July 2025).
    """
    payload = dict(sort="trending", limit=limit, offset=offset)
    try:
        data = _get("/api/sketches", params=payload)  # → { records:[{id: …}, …] }
    except ValueError as exc:
        print(f"[error] failed to fetch trending IDs: {exc}")
        return []
    return [rec["id"] for rec in data["records"]]

def trending_ids_iter(step=90, start=0):
    """Yield trending sketch IDs across all pages until exhausted."""
    offset = start
    while True:
        ids = trending_ids(limit=step, offset=offset)
        if not ids:
            break
        for sid in ids:
            yield sid
        offset += step

def sketch_code(sketch_id):
    """Return the *array* of code files (one element per tab)."""
    return _get(f"/api/sketch/{sketch_id}/code")        # :contentReference[oaicite:0]{index=0}

def sketch_assets(sketch_id):
    """Return any uploaded binary files (images, fonts, etc.)."""
    return _get(f"/api/sketch/{sketch_id}/files")       # :contentReference[oaicite:1]{index=1}

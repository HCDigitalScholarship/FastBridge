"""Cache-busting helper for static assets.

Appends ?v=<file-mtime> to a static URL so browsers refetch a file only when it
actually changes. No git dependency (works inside the built container image),
and one os.stat per include — negligible cost.

Registered as a Jinja global named ``static_v`` on the templates instances that
render pages with frequently-changing app JS (select/userspace/stats/oracle).
"""
from pathlib import Path

# Mirrors main.py: StaticFiles is mounted at /assets from static/assets
_STATIC_ROOT = Path.cwd() / "static" / "assets"


def static_v(path: str) -> str:
    """Return ``path`` with a cache-busting ?v=<mtime> suffix.

    Falls back to the unmodified path if the file can't be found, so a bad
    path never breaks rendering.
    """
    rel = path.lstrip("/")
    if rel.startswith("assets/"):
        rel = rel[len("assets/"):]
    try:
        version = int((_STATIC_ROOT / rel).stat().st_mtime)
    except OSError:
        return path
    sep = "&" if "?" in path else "?"
    return f"{path}{sep}v={version}"

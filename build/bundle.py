#!/usr/bin/env python3
"""Produce a self-contained single-file build of the campaign page.

Images are downscaled and inlined as data: URIs, the GSAP scripts are inlined,
and the document wrapper is stripped so the result can be published as an
Artifact (whose CSP blocks every external host except Google Fonts).
"""
import base64
import mimetypes
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"
OPTIMIZED = BUILD / "opt"
OPTIMIZED.mkdir(parents=True, exist_ok=True)

# Target width per asset role. Renderings carry the page, so they get the most
# pixels; the headline pills render at ~90px wide and need almost none.
WIDTHS = {
    "portrait-": 420,
    "r-": 1400,
    "wordmark-": 1200,
    "monogram-": 320,
}
DEFAULT_WIDTH = 1100


def target_width(name: str) -> int:
    for prefix, width in WIDTHS.items():
        if name.startswith(prefix):
            return width
    return DEFAULT_WIDTH


def optimize(src: Path) -> Path:
    """Downscale and re-encode.

    PNGs with transparency (the marks) stay PNG. Everything else lands as JPEG,
    including WebP sources: sips can read WebP but cannot write it, so the
    resample has to target the .jpg path directly rather than round-tripping.
    """
    keep_png = src.suffix.lower() == ".png"
    out = (OPTIMIZED / src.name).with_suffix(".png" if keep_png else ".jpg")

    cmd = ["sips", "--resampleWidth", str(target_width(src.name))]
    if not keep_png:
        cmd += ["-s", "format", "jpeg", "-s", "formatOptions", "68"]
    cmd += [str(src), "--out", str(out)]

    subprocess.run(cmd, check=True, capture_output=True)
    return out


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    # Inline every asset reference, whether it came from src="" or url('').
    cache: dict[str, str] = {}
    for ref in sorted(set(re.findall(r"assets/([\w.\-]+)", html))):
        src = ASSETS / ref
        if not src.exists():
            raise SystemExit(f"missing asset: {src}")
        cache[ref] = data_uri(optimize(src))
        print(f"  inlined {ref:28} {len(cache[ref]) // 1024:>5} KB")

    for ref, uri in cache.items():
        html = html.replace(f"assets/{ref}", uri)

    # Inline GSAP; the Artifact CSP blocks cdnjs.
    for tag, lib in (
        ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>', "gsap.min.js"),
        ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>', "ScrollTrigger.min.js"),
    ):
        if tag not in html:
            raise SystemExit(f"could not find script tag for {lib}")
        html = html.replace(tag, "<script>" + (BUILD / lib).read_text(encoding="utf-8") + "</script>")

    # Strip the document wrapper: Artifacts supply doctype/head/body themselves.
    # The document keeps a full SEO title; the Artifact gallery wants the
    # campaign name alone, with the explainer moved to the publish description.
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).split("|")[0].strip()
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)

    keep = "".join(
        m.group(0) for m in re.finditer(r"<style>.*?</style>", head, re.S)
    )
    fonts = "".join(
        m.group(0) for m in re.finditer(r'<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>', head)
    )

    out = f"<title>{title}</title>\n{fonts}\n{keep}\n{body}"
    dest = BUILD / "artifact.html"
    dest.write_text(out, encoding="utf-8")
    print(f"\nwrote {dest}  ({dest.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()

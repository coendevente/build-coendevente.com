"""Create compact delivery images while retaining original assets for downloads."""
import hashlib
import io
import os
import re
from pathlib import Path

from PIL import Image, ImageOps
import resvg_py


URL = re.compile(r'''url\(\s*(['"]?)([^)'"\s]+)\1\s*\)''')
SRC = re.compile(r'''(\bsrc\s*=\s*['"])([^'"]+)(['"])''')


def optimize_site_images(site=Path('site')):
    site = Path(site).resolve()
    output = site / 'images' / 'optimized'
    output.mkdir(parents=True, exist_ok=True)
    replacements = {}

    def asset(url, document):
        if url.startswith(('http:', 'https:', '//', 'data:', '#')) or '?' in url or '#' in url:
            return url
        source = (document.parent / url).resolve()
        if not source.is_relative_to(site) or not source.is_file():
            return url
        if source.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.svg'):
            return url
        if source not in replacements:
            raw = source.read_bytes()
            # Keep small vector icons as vectors.
            if source.suffix.lower() == '.svg' and len(raw) < 100_000:
                return url
            digest = hashlib.sha256(raw + b'webp-v1-1920-q84').hexdigest()[:20]
            target = output / (digest + '.webp')
            if not target.exists():
                if source.suffix.lower() == '.svg':
                    raw = resvg_py.svg_to_bytes(svg_path=str(source), width=1600)
                with Image.open(io.BytesIO(raw)) as original:
                    if getattr(original, 'is_animated', False):
                        return url
                    image = ImageOps.exif_transpose(original)
                    image.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                    image.convert('RGBA' if 'A' in image.getbands() else 'RGB').save(target, 'WEBP', quality=84, method=6)
            replacements[source] = target if target.stat().st_size < source.stat().st_size else source
        target = replacements[source]
        return Path(os.path.relpath(target, document.parent)).as_posix()

    for document in [*site.glob('*.html'), *site.glob('css/*.css')]:
        text = document.read_text()
        def replace_url(match):
            replacement = asset(match[2], document)
            return match[0] if replacement == match[2] else "url('" + replacement + "')"

        text = URL.sub(replace_url, text)
        if document.suffix == '.html':
            text = SRC.sub(lambda m: m[1] + asset(m[2], document) + m[3], text)
        document.write_text(text)
    return replacements


def create_cover_panels(settings, site=Path('site')):
    source = site / settings['source']
    raw = resvg_py.svg_to_bytes(svg_path=str(source), width=2400)
    image = Image.open(io.BytesIO(raw)).convert('RGB')
    paths = []
    for crop in settings['crops']:
        box = tuple(round(value * (image.width if i % 2 == 0 else image.height))
                    for i, value in enumerate(crop))
        panel = image.crop(box)
        digest = hashlib.sha256(source.read_bytes() + str(crop).encode()).hexdigest()[:20]
        relative = Path('images/optimized') / (digest + '.webp')
        (site / relative).parent.mkdir(parents=True, exist_ok=True)
        panel.save(site / relative, 'WEBP', quality=88, method=6)
        paths.append(relative.as_posix())
    return paths

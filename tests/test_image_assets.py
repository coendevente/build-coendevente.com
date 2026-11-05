import tempfile
import unittest
from pathlib import Path
from PIL import Image
from image_assets import optimize_site_images


class ImageAssetsTests(unittest.TestCase):
    def test_delivery_images_preserve_links_transparency_and_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / 'images').mkdir()
            (site / 'css').mkdir()
            Image.new('RGBA', (2400, 1200), (200, 50, 20, 100)).save(site / 'images/photo.png')
            html = '''<a href="images/photo.png"><img src="images/photo.png"></a>
<div style="background-image: url('images/photo.png')"></div>
<script>$(".card").hover(function() {});</script>'''
            (site / 'index.html').write_text(html)
            (site / 'css/style.css').write_text('div { background: url(../images/photo.png); }')
            mapping = optimize_site_images(site)
            target = mapping[(site / 'images/photo.png').resolve()]
            with Image.open(target) as image:
                self.assertEqual(image.size, (1920, 960))
                self.assertIn('A', image.getbands())
            output = (site / 'index.html').read_text()
            self.assertIn('href="images/photo.png"', output)
            self.assertIn('$(".card").hover(function() {});', output)
            self.assertIn('src="images/optimized/', output)
            self.assertIn('../images/optimized/', (site / 'css/style.css').read_text())
            optimize_site_images(site)
            self.assertEqual(output, (site / 'index.html').read_text())

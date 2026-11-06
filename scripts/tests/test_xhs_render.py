"""Tests for xhs_render.py: deliberately broken pages must be caught, clean pages must not be accused, and long strips must be cut into the right number of images.

Run: python3 -m unittest scripts/tests/test_xhs_render.py -v
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / 'xhs_render.py'
FX = HERE / 'fixtures'

try:
    import playwright  # noqa: F401
    HAVE = True
except ImportError:
    HAVE = False


def run(name, out):
    p = subprocess.run([sys.executable, str(SCRIPT), str(FX / name), '--out', out], capture_output=True, text=True, timeout=180)
    return p.returncode, p.stdout + p.stderr


@unittest.skipUnless(HAVE, 'playwright not installed')
class XhsRender(unittest.TestCase):
    def test_bad_page_is_caught(self):
        with tempfile.TemporaryDirectory() as d:
            code, out = run('xhs_bad.html', d)
            self.assertEqual(code, 1, out)
            self.assertIn('label floor', out)            # a 24px label
            self.assertIn('body floor', out)              # a 34px multi-line paragraph
            self.assertIn('text outside the page', out)
            self.assertIn('text across seam 1', out)
            self.assertIn('text overlapping text', out)
            self.assertIn('text covered by another element', out)
            self.assertIn('✗ page 01  text overlapping text', out)
            pngs = sorted(Path(d).glob('*.png'))
            self.assertIn('text crowded against a graphic', out)    # a grid collapsed into one column and crowded the text
            self.assertEqual(len(pngs), 4)            # 2 pages + the long strip cut into 2
            self.assertTrue((Path(d) / 'sheet.jpg').exists())

    def test_clean_page_passes(self):
        with tempfile.TemporaryDirectory() as d:
            code, out = run('xhs_ok.html', d)
            self.assertEqual(code, 0, out)
            self.assertNotIn('text overlapping text', out)
            self.assertNotIn('covered', out)
            self.assertEqual(sorted(p.name for p in Path(d).iterdir()), ['01.png', 'sheet.jpg'])   # no intermediate images left behind


if __name__ == '__main__':
    unittest.main()

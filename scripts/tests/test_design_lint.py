"""Tests for design_lint.py and learn.py: the checks must catch deliberately broken inputs, and must not accuse clean ones.

Run: python3 -m unittest scripts/tests/test_design_lint.py -v
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import design_lint as dl  # noqa: E402
import learn  # noqa: E402
import ref_board  # noqa: E402

FX = HERE / 'fixtures'


class LintFacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        names = ['lint_slop.html', 'lint_reskin.html', 'lint_clean.html', 'lint_broken.html']
        cls.f = dict(zip(names, dl.collect([str(FX / n) for n in names])))

    def test_slop_hits_the_2026_clusters(self):
        red, yellow = dl.judge(self.f['lint_slop.html'])
        text = '\n'.join(yellow)
        fams = '\n'.join(dl.families(self.f['lint_slop.html']))
        self.assertIn('warm-paper serif', fams)       # warm cream + terracotta + serif: description only
        self.assertIn('card kit', fams)               # cards with the same radius and same shadow: description only
        self.assertNotIn('warm-paper serif', text)    # families no longer raise a yellow light
        self.assertIn('Template chrome', text)        # all-caps eyebrow labels, middots, arrows
        self.assertIn('one recolored/italicized word', text)
        self.assertIn('01/02/03', text)

    def test_clean_page_is_not_accused(self):
        red, yellow = dl.judge(self.f['lint_clean.html'])
        self.assertEqual(red, [])
        self.assertEqual(yellow, [])

    def test_broken_page_goes_red(self):
        red, _ = dl.judge(self.f['lint_broken.html'])
        text = '\n'.join(red)
        self.assertIn('broken images', text)
        self.assertIn('body font size below the floor', text)
        self.assertIn('insufficient contrast', text)

    def test_reskin_is_caught_by_layout_not_colour(self):
        a = dl.fingerprint(self.f['lint_slop.html'])
        b = dl.fingerprint(self.f['lint_reskin.html'])
        c = dl.fingerprint(self.f['lint_clean.html'])
        hits, pd, lc = dl.similar(a, b)
        self.assertGreater(pd, 0.06)          # the colors really did change
        self.assertTrue(any('layout skeletons highly similar' in h for h in hits), hits)   # but the skeleton didn't
        self.assertFalse(dl.similar(a, c)[0])  # two genuinely different versions are not flagged

    def test_warm_cream_is_classified_warm(self):
        self.assertEqual(dl.bg_class((0xF4, 0xF1, 0xEA)), 'light·warm paper')
        self.assertEqual(dl.bg_class((0xFA, 0xF8, 0xF4)), 'light·warm paper')
        self.assertEqual(dl.bg_class((0xFA, 0xFA, 0xFA)), 'light·neutral white')
        self.assertNotEqual(dl.bg_class((0xDF, 0xEB, 0xE5)), 'light·warm paper')   # a cool celadon grey is not warm cream


class LintEdgeCases(unittest.TestCase):
    """False positives and false negatives reported by an independent review, pinned down one by one as regression tests."""

    def test_no_false_red_on_svg_sibling_plate_and_caption(self):
        f = dl.collect([str(FX / 'lint_tricky_ok.html')])[0]
        red, _ = dl.judge(f)
        self.assertEqual(red, [])   # scaled-up SVG text, white text on a sibling dark layer, and a 13px caption must not go red

    def test_deck_div_body_and_ghost_text_go_red(self):
        f = dl.collect([str(FX / 'lint_tricky_bad.html')], viewport=(1920, 1080), min_body=24, min_label=16)[0]
        red, yellow = dl.judge(f)
        text = '\n'.join(red)
        self.assertIn('body font size below the floor', text)   # 16px body written as a div
        self.assertIn('insufficient contrast', text)             # white text at 8% opacity
        self.assertTrue(any('relative-path images' in y for y in yellow))

    def test_unreachable_stylesheet_does_not_kill_the_batch(self):
        res = dl.collect([str(FX / 'lint_offline.html'), str(FX / 'lint_clean.html')])
        self.assertEqual(len(res), 2)
        self.assertNotIn('fatal', res[1])
        self.assertEqual(dl.judge(res[1])[0], [])

    def test_glob_is_expanded_by_the_script(self):
        self.assertIn(str(FX / 'lint_clean.html'), dl.expand([str(FX / 'lint_c*.html')]))

    def test_brand_mode_only_compares_skeleton(self):
        f = dl.collect([str(FX / 'lint_slop.html')])[0]
        a = dl.fingerprint(f)
        self.assertTrue(dl.similar(a, a)[0])
        b = dict(a, layout=[-x for x in a['layout']])   # same colors and fonts, completely different skeleton
        self.assertFalse(dl.similar(a, b, brand=True)[0])


class Ledger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['HUASHU_DESIGN_HOME'] = self.tmp.name

    def tearDown(self):
        os.environ.pop('HUASHU_DESIGN_HOME', None)
        self.tmp.cleanup()

    def test_add_then_check_flags_the_same_look(self):
        self.assertEqual(dl.main(['ledger', 'add', str(FX / 'lint_slop.html'), '--project', '测试项目']), 0)
        rows = dl.ledger_read()
        self.assertEqual(len(rows), 1)
        self.assertIn('light·warm paper', rows[0]['desc'])
        # the same look again: must be flagged as a collision
        self.assertEqual(dl.main(['ledger', 'check', str(FX / 'lint_slop.html')]), 1)
        # a genuinely different look: not flagged
        self.assertEqual(dl.main(['ledger', 'check', str(FX / 'lint_clean.html')]), 0)


class Learn(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['HUASHU_DESIGN_HOME'] = self.tmp.name

    def tearDown(self):
        os.environ.pop('HUASHU_DESIGN_HOME', None)
        self.tmp.cleanup()

    def test_refuses_entries_nobody_can_check(self):
        with self.assertRaises(learn.LearnError):
            learn.add_entry('guess', 'deck', '随便', '证据')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('observed', '', '没有主题', '证据')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('observed', 'deck', '没有证据', '')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('preference', 'color', '他喜欢暖色', '对话')  # a preference must quote the user verbatim

    def test_roundtrip(self):
        learn.add_entry('preference', 'color,cover', '「封面用暖纸底」——只用于他自己的封面', '2026-10-17 对话')
        learn.add_entry('observed', 'deck', '三版都用了同一个骨架被他一眼看出', 'B2 基准')
        out = learn.recall(['deck'])
        self.assertIn('封面用暖纸底', out)      # preferences always come along
        self.assertIn('同一个骨架', out)
        self.assertIn('L2', learn.local_file().read_text(encoding='utf-8'))
        self.assertNotIn('同一个骨架', learn.recall(['motion']).split('## Experience from past projects')[1])

    def test_hand_edited_heading_without_trailing_dot_keeps_its_kind(self):
        learn.local_file().parent.mkdir(parents=True, exist_ok=True)
        learn.local_file().write_text('# x\n\n## 手记 · preference\n\n- 原话：「要大胆」\n', encoding='utf-8')
        self.assertEqual(learn.entries(learn.local_file(), 'local')[0]['kind'], 'preference')

    def test_topic_named_like_a_subcommand_can_be_recalled(self):
        self.assertIn('Experience from past projects', learn.recall(['status']))
        self.assertEqual(learn.main(['--', 'status']), 0)


class RefBoard(unittest.TestCase):
    def test_blank_screenshot_counts_as_not_seen(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            blank, real = Path(d) / 'blank.jpg', Path(d) / 'real.jpg'
            Image.new('RGB', (1440, 900), (32, 26, 28)).save(blank)   # what a WebGL site looks like in a headless browser
            im = Image.new('RGB', (1440, 900), 'white')
            ImageDraw.Draw(im).rectangle([100, 100, 900, 600], fill=(20, 60, 200))
            im.save(real)
            self.assertTrue(ref_board.mostly_blank(blank))
            self.assertFalse(ref_board.mostly_blank(real))
            # a minimalist design must not be mistaken for never having loaded
            sparse = HERE.parent.parent / 'assets' / 'style-specimens' / 'info' / '17-ma-emptiness.jpg'
            self.assertFalse(ref_board.mostly_blank(sparse))

    def test_local_image_goes_on_the_board(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / 'src.png'
            im = Image.new('RGB', (800, 500), (240, 236, 228))
            ImageDraw.Draw(im).rectangle([60, 60, 420, 440], fill=(200, 40, 40))
            im.save(src)
            out = Path(d) / 'refs' / 'board.jpg'
            self.assertEqual(ref_board.main([str(src), '--out', str(out)]), 0)
            self.assertTrue(out.exists() and (out.parent / 'board-1.jpg').exists())


if __name__ == '__main__':
    unittest.main()

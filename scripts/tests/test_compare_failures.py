"""Compare must not approve directions that could not all be inspected.

Stdlib-only: python3 -m unittest discover -s scripts/tests -p test_compare_failures.py -v
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import design_lint as dl  # noqa: E402


class CompareFailures(unittest.TestCase):
    def run_compare(self, facts, hits=()):
        output = io.StringIO()
        fingerprint = {'desc': 'synthetic direction', 'bg_class': 'test'}
        with patch.object(dl, 'collect', return_value=facts), \
             patch.object(dl, 'fingerprint', return_value=fingerprint) as fp, \
             patch.object(dl, 'families', return_value=[]), \
             patch.object(dl, 'similar', return_value=(list(hits), 0.2, 0.1)), \
             contextlib.redirect_stdout(output):
            code = dl.main(['compare'] + [f['path'] for f in facts])
        return code, output.getvalue(), fp.call_count

    def test_all_unreadable_directions_are_not_a_success(self):
        code, output, count = self.run_compare([
            {'path': '/fixtures/missing.html', 'fatal': 'file not found'},
            {'path': '/fixtures/invalid.html', 'fatal': 'navigation failed'},
        ])
        self.assertEqual(code, 2)
        self.assertIn('missing.html', output)
        self.assertIn('invalid.html', output)
        self.assertNotIn('✓', output)
        self.assertEqual(count, 0)

    def test_one_readable_direction_cannot_mask_a_failure(self):
        code, output, count = self.run_compare([
            {'path': '/fixtures/readable.html'},
            {'path': '/fixtures/missing.html', 'fatal': 'file not found'},
        ])
        self.assertEqual(code, 2)
        self.assertIn('file not found', output)
        self.assertNotIn('✓', output)
        self.assertEqual(count, 0)

    def test_two_distinct_directions_cannot_mask_a_failed_third(self):
        code, output, count = self.run_compare([
            {'path': '/fixtures/first.html'},
            {'path': '/fixtures/second.html'},
            {'path': '/fixtures/missing.html', 'fatal': 'file not found'},
        ])
        self.assertEqual(code, 2)
        self.assertNotIn('✓', output)
        self.assertEqual(count, 0)

    def test_complete_distinct_comparison_still_passes(self):
        code, output, count = self.run_compare([
            {'path': '/fixtures/first.html'}, {'path': '/fixtures/second.html'},
        ])
        self.assertEqual(code, 0)
        self.assertIn('✓', output)
        self.assertEqual(count, 2)

    def test_complete_colliding_comparison_still_fails(self):
        code, output, count = self.run_compare([
            {'path': '/fixtures/first.html'}, {'path': '/fixtures/second.html'},
        ], hits=['same layout'])
        self.assertEqual(code, 1)
        self.assertIn('same layout', output)
        self.assertNotIn('✓', output)
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()

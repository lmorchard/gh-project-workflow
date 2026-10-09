import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scenario_index as index


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evals/scenarios').mkdir(parents=True)
        (self.root / 'evals/results').mkdir()
        for name in ('sample', 'unrun'):
            (self.root / f'evals/scenarios/{name}.md').write_text('scenario')

    def row(self, **changes):
        row = dict(scenario='sample', date='2026-10-08', skill_commit=None,
                   runner=None, model=None, grade='Pass (2/2)', phase='sample', note=None, order=None)
        return row | changes

    def report(self, name, rows):
        (self.root / f'evals/results/{name}.md').write_text(
            'Historical prose\n\n```scenario-results\n' + json.dumps(rows) + '\n```\n')

    def test_unknown_metadata_is_a_recorded_run_and_batch_grade_survives(self):
        self.report('result', [self.row()])
        result = index.render(self.root)
        runs, missing = result.split('## No recorded run')
        self.assertIn('| unknown | unknown | unknown | Pass (2/2) |', runs)
        self.assertNotIn('[sample]', missing)
        self.assertIn('[unrun]', missing)

    def test_unknown_scenario_is_an_error(self):
        self.report('result', [self.row(scenario='typo')])
        with self.assertRaisesRegex(index.RecordError, 'unknown scenario'):
            index.render(self.root)

    def test_missing_and_malformed_records_fail_instead_of_false_unrun(self):
        path = self.root / 'evals/results/result.md'
        for text in ('Unstructured report', '```scenario-results\n[\n```\n',
                     '```scenario-results\n[]\n```\n', '```scenario-results\n[{}]\n```\n'):
            with self.subTest(text=text):
                path.write_text(text)
                with self.assertRaises(index.RecordError):
                    index.render(self.root)

    def test_latest_date_ties_and_undated_evidence_are_retained(self):
        self.report('old', [self.row(date='2026-10-01', grade='Fail')])
        self.report('one', [self.row(grade='Partial')])
        self.report('two', [self.row(grade='Pass')])
        self.report('undated', [self.row(date=None, grade='ungraded')])
        result = index.render(self.root)
        self.assertNotIn('[old.md]', result)
        for name in ('one', 'two', 'undated'):
            self.assertIn(f'[{name}.md]', result)

    def test_explicit_order_supersedes_baseline_only_within_same_report(self):
        self.report('experiment', [self.row(phase='baseline', grade='Fail', order=1),
                                   self.row(phase='changed skill', order=2)])
        self.report('independent', [self.row(grade='Partial', order=1)])
        result = index.render(self.root)
        self.assertNotIn('| Fail |', result)
        self.assertIn('| changed skill |', result)
        self.assertIn('| Partial |', result)

    def test_same_phase_samples_are_preserved_and_generation_is_deterministic(self):
        rows = [self.row(grade='Partial', order=2), self.row(order=2)]
        self.report('experiment', rows)
        first = index.render(self.root)
        self.report('experiment', rows[::-1])
        self.assertEqual(first, index.render(self.root))
        self.assertIn('| Partial |', first)
        self.assertIn('| Pass (2/2) |', first)

    def test_invalid_date_or_order_fails(self):
        for changes in ({'date': '2026-02-30'}, {'date': '20261008'}, {'order': True}, {'order': 0}):
            self.report('result', [self.row(**changes)])
            with self.subTest(changes=changes), self.assertRaises(index.RecordError):
                index.render(self.root)

    def test_check_detects_missing_stale_and_current_index(self):
        self.report('result', [self.row()])
        with patch.object(index, 'ROOT', self.root):
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(1, index.main(['--check']))
                self.assertIn('is stale', errors.getvalue())
            self.assertEqual(0, index.main([]))
            self.assertEqual(0, index.main(['--check']))
            self.report('result', [self.row(grade='Fail')])
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, index.main(['--check']))

if __name__ == '__main__':
    unittest.main()

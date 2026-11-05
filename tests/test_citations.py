import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
from bibliography import citations


class CitationTests(unittest.TestCase):
    def setUp(self):
        citations.author_works.cache_clear()
        self.addCleanup(citations.author_works.cache_clear)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'counts.json'
        patcher = patch.object(citations, 'CACHE_PATH', self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.work = {'id': 'https://openalex.org/W123', 'title': 'A title',
                     'publication_year': 2024, 'cited_by_count': 23,
                     'authorships': [{'author': {'display_name': 'Coen de Vente'}}]}

    @patch.object(citations, 'request_work')
    def test_counts_including_zero_and_cache(self, get):
        for count in [23, 0]:
            self.work['cited_by_count'] = count
            get.return_value = self.work
            result = citations.get_citation(str(count), 'A title', 2024, '10.1234/test')
            self.assertEqual(result['count'], count)
            self.assertEqual(result['source'], 'OpenAlex')
        get.reset_mock()
        citations.get_citation('0', 'A title', 2024, '10.1234/test')
        get.assert_not_called()

    @patch.object(citations, 'request_work')
    def test_failure_preserves_previous_count(self, get):
        get.return_value = {'results': [self.work], 'meta': {'count': 1}}
        citations.get_citation('pub', 'A title', 2024)
        cache = json.loads(self.path.read_text())
        cache['pub']['updated_at'] = '2025-01-01T00:00:00+00:00'
        self.path.write_text(json.dumps(cache))
        before = self.path.read_text()
        for failure in [requests.Timeout(), ValueError('bad response')]:
            get.side_effect = failure
            self.assertEqual(citations.get_citation('pub', 'A title', 2024)['count'], 23)
            self.assertEqual(self.path.read_text(), before)
            self.assertIsNone(citations.get_citation('new', 'Unknown', 2024))

    @patch.object(citations, 'request_work')
    def test_conservative_title_matching(self, get):
        get.return_value = {'results': [self.work], 'meta': {'count': 1}}
        self.assertEqual(citations.resolve_work('A TITLE!', 2024, None), self.work)
        self.assertIsNone(citations.resolve_work('Different title', 2024, None))
        self.assertIsNone(citations.resolve_work('A title', 2020, None))
        self.assertIsNone(citations.resolve_work('A title', 2023, None, '@conference'))
        citations.author_works.cache_clear()
        get.return_value = {'results': [self.work, dict(self.work, id='https://openalex.org/W456')], 'meta': {'count': 2}}
        self.assertIsNone(citations.resolve_work('A title', 2024, None))
        citations.author_works.cache_clear()
        get.return_value = {'results': [dict(self.work, authorships=[])], 'meta': {'count': 1}}
        self.assertIsNone(citations.resolve_work('A title', 2024, None))

    @patch.object(citations, 'request_work')
    def test_missing_count_is_not_zero(self, get):
        get.return_value = dict(self.work, cited_by_count=None)
        self.assertIsNone(citations.get_citation('pub', 'A title', 2024, '10.1234/test'))
        self.assertFalse(self.path.exists())

    def test_doi_and_sorting(self):
        self.assertEqual(citations.normalize_doi('https://doi.org/https://doi.org/10.1234/ABC'), '10.1234/abc')
        pubs = {'unknown': {'citation_count': None, 'year': 2026},
                'zero': {'citation_count': 0, 'year': 2024},
                'old': {'citation_count': 12, 'year': 2020},
                'new': {'citation_count': 12, 'year': 2025},
                'top': {'citation_count': 100, 'year': 2018}}
        self.assertEqual([k for k,v in sorted(pubs.items(), key=citations.publication_sort_key)],
                         ['top', 'new', 'old', 'zero', 'unknown'])

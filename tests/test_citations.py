import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

import requests
from bibliography import citations


class CitationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'counts.json'
        self.path.write_text(json.dumps({'123': {'count': 42}}))
        self.patch = patch.object(citations, 'CACHE_PATH', self.path)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    @patch.dict('os.environ', {'SERPAPI': 'test-key'})
    @patch.object(citations.requests, 'get')
    def test_api_count_and_zero_are_persisted(self, get):
        for count in [1234, 0]:
            get.return_value = Mock(ok=True)
            get.return_value.json.return_value = {'search_information': {'total_results': count}}
            self.assertEqual(citations.get_count('123'), count)
            self.assertEqual(json.loads(self.path.read_text())['123']['count'], count)

    @patch.dict('os.environ', {'SERPAPI': 'test-key'})
    @patch.object(citations.requests, 'get')
    def test_failure_preserves_cache(self, get):
        before = self.path.read_text()
        get.side_effect = requests.Timeout()
        self.assertEqual(citations.get_count('123'), 42)
        self.assertIsNone(citations.get_count('unknown'))
        self.assertEqual(self.path.read_text(), before)

    @patch.dict('os.environ', {'SERPAPI': 'test-key'})
    @patch.object(citations.requests, 'get')
    def test_error_or_missing_total_is_not_zero(self, get):
        for data in [{'error': 'Blocked'}, {}, {'search_information': {'total_results': 'bad'}}]:
            get.return_value = Mock(ok=True)
            get.return_value.json.return_value = data
            self.assertEqual(citations.get_count('123'), 42)

    @patch.dict('os.environ', {}, clear=True)
    @patch.object(citations.requests, 'get')
    def test_html_summary_and_block_page(self, get):
        get.return_value = Mock(ok=True, text='<div id="gs_ab_md">About 1,234 results (0.1 sec)</div>')
        self.assertEqual(citations.get_count('123'), 1234)
        get.return_value.text = '<html>Sorry, 999 results unavailable</html>'
        self.assertEqual(citations.get_count('123'), 1234)

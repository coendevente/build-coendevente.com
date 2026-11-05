"""Refresh Google Scholar counts without discarding the last successful values."""
import json
import os
import re
import warnings
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests

CACHE_PATH = Path(__file__).parent / 'content' / 'citation_counts.json'


def get_count(scholar_id):
    cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    count = None
    key = os.environ.get('SERPAPI')
    try:
        if key:
            response = requests.get('https://serpapi.com/search.json', params={
                'engine': 'google_scholar', 'cites': scholar_id,
                'hl': 'en', 'api_key': key,
            }, timeout=30)
            if response.ok:
                data = response.json()
                if not data.get('error'):
                    count = data.get('search_information', {}).get('total_results')
        else:
            response = requests.get('https://scholar.google.com/scholar',
                                    params={'cites': scholar_id, 'hl': 'en'}, timeout=15)
            if response.ok:
                # Restrict parsing to the results summary, never arbitrary page numbers.
                summary = re.search(r'id=[\"\']gs_ab_md[\"\'][^>]*>(.*?)</div>',
                                    response.text, re.S)
                if summary:
                    text = unescape(re.sub('<[^>]+>', ' ', summary.group(1)))
                    match = re.search(r'\b([\d,]+)\s+results?\b', text)
                    if match:
                        count = int(match.group(1).replace(',', ''))
    except (requests.RequestException, ValueError):
        # Do not log exceptions containing the API URL/key.
        pass
    if type(count) is int and count >= 0:
        cache[scholar_id] = {'count': count, 'updated_at': datetime.now(timezone.utc).isoformat()}
        CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True) + '\n')
        return count
    previous = cache.get(scholar_id)
    warnings.warn(f'Could not refresh Scholar ID {scholar_id}; using cached count if available')
    return previous['count'] if previous else None

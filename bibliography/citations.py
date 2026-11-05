"""OpenAlex citation counts, with conservative matching and a persistent cache."""
import hashlib
import json
import os
import re
import warnings
from datetime import datetime, timezone, timedelta
from pathlib import Path
from functools import lru_cache

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from unidecode import unidecode

CACHE_PATH = Path(__file__).parent / 'content' / 'openalex_counts.json'
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'coendevente.com-publications/1.0 (https://coendevente.com)'
SESSION.mount('https://', HTTPAdapter(max_retries=Retry(
    total=2, backoff_factor=1, respect_retry_after_header=False, status_forcelist=[500, 502, 503, 504])))


def normalize(text):
    return re.sub(r'[^a-z0-9]', '', unidecode(text).lower())


def normalize_doi(value):
    match = re.search(r'10\.\d{4,9}/[^\s{}]+', value, re.I)
    return match.group(0).lower() if match else None


def request_work(path, **params):
    if os.environ.get('OPENALEX_API_KEY'):
        params['api_key'] = os.environ['OPENALEX_API_KEY']
    response = SESSION.get('https://api.openalex.org/' + path, params=params, timeout=30)
    # Keep API credentials out of error messages.
    if not response.ok:
        raise ValueError(f'OpenAlex HTTP {response.status_code}')
    return response.json()


@lru_cache(maxsize=1)
def author_works():
    # Verified OpenAlex author: Coen de Vente, ORCID 0000-0001-5908-8367.
    works = []
    page = 1
    while True:
        data = request_work('works', filter='author.id:A5028752528', per_page=200, page=page)
        works.extend(data['results'])
        if len(works) >= data['meta']['count']:
            return works
        if not data['results']:
            raise ValueError('Incomplete author response')
        page += 1


def resolve_work(title, year, doi, entry_type=""):
    if doi:
        return request_work('works/https://doi.org/' + doi)
    matches = []
    for work in author_works():
        authors = [normalize(a.get('author', {}).get('display_name', ''))
                   for a in work.get('authorships', [])]
        if (normalize(work.get('title') or '') == normalize(title)
                and abs((work.get('publication_year') or 0) - year) <= (0 if entry_type.lower() == '@conference' else 1)
                and any('coen' in a and 'devente' in a for a in authors)):
            matches.append(work)
    exact_year = [w for w in matches if w['publication_year'] == year]
    matches = exact_year or matches
    # Ambiguous titles need an explicit DOI; never guess the top search result.
    return matches[0] if len(matches) == 1 else None


def get_citation(key, title, year, doi='', entry_type=''):
    cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    doi = normalize_doi(doi)
    signature = hashlib.sha256(f'{normalize(title)}|{year}|{doi}|{entry_type}'.encode()).hexdigest()
    previous = cache.get(key)
    if previous and previous.get('signature') != signature:
        previous = None
    now = datetime.now(timezone.utc)
    if previous and os.environ.get('REFRESH_CITATIONS') != 'true' and now - datetime.fromisoformat(previous['updated_at']) < timedelta(days=1):
        return previous
    try:
        work = (request_work('works/' + previous['work_id'].rsplit('/', 1)[-1])
                if previous else resolve_work(title, int(year), doi, entry_type))
        if work and type(work.get('cited_by_count')) is int and work['cited_by_count'] >= 0:
            work_id = work.get('id', '')
            if not re.fullmatch(r'https://openalex.org/W\d+', work_id):
                raise ValueError('Invalid OpenAlex work ID')
            record = {'count': work['cited_by_count'], 'work_id': work_id,
                      'title': work['title'], 'source': 'OpenAlex',
                      'updated_at': now.isoformat(), 'signature': signature}
            cache[key] = record
            CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True) + '\n')
            print(f'OpenAlex {key}: {record["count"]} citations ({work_id})')
            return record
        reason = 'no unambiguous match or citation count'
    except (requests.RequestException, ValueError, KeyError, TypeError):
        reason = 'API request failed'
    warnings.warn(f'OpenAlex {key}: {reason}; retaining cached count if available')
    return previous


def publication_sort_key(item):
    """Known counts descending; unknown last; newest year breaks ties."""
    count = item[1].get('citation_count')
    return (-(count if type(count) is int else -1), -item[1]['year'], item[0])

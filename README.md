# Repo to build coendevente.com

## Installation
`pip3 install -r requirements.txt`

## Building
`python3 generate.py`

## Content
Projects are in `projects`, with the content of files as `.md` files and `.json` for the settings.
Publications are in `publications/content/publications.bib`.

## Automated publication and citations

The Actions build uses Python 3.11 (compatible with the pinned Pillow release).
`SERPAPI` is the existing SerpApi API-key secret used for Google Scholar citation
refreshes. If refreshes fail, `bibliography/content/citation_counts.json` retains
the last successful count and its timestamp; a failed request never becomes zero.
The initial fallback values were recovered from the published site on April 10,
2025, with their source commit recorded in the cache. Counts can therefore lag
Google Scholar during outages. Local builds without the secret try Scholar directly.

`SITE_DEPLOY_KEY` is a write-enabled deploy key scoped to
`coendevente/coendevente.github.io`. The workflow commits and pushes the generated
`site` to its `master` branch, then records the submodule and citation cache here.
Run the workflow manually to refresh counts without editing content.

Run citation regression tests with `python -m unittest discover -s tests`.

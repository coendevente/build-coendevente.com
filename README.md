# Repo to build coendevente.com

## Installation
`pip3 install -r requirements.txt`

## Building
`python3 generate.py`

## Content
Projects are in `projects`, with the content of files as `.md` files and `.json` for the settings.
Publications are in `publications/content/publications.bib`.

## Automated publication and citations

Actions builds with Python 3.11 and refreshes citation counts from OpenAlex every
Monday at 06:23 UTC, on pushes, or via workflow_dispatch. No API key is required
for this small workload; the optional OPENALEX_API_KEY secret supports a higher
quota. Counts are OpenAlex counts, not Google Scholar counts.

One filtered author-catalog request resolves titles without relying on the
rate-limited full-text search endpoint. Publications resolve by DOI, or by an
exact normalized title, matching author
(Coen de Vente), and publication year within one year (exact year for conference abstracts). Ambiguous results are
omitted until a DOI is supplied. Resolved OpenAlex work IDs, counts, and timestamps
are saved in bibliography/content/openalex_counts.json. Successful responses are
cached for one day; failures retain the previous OpenAlex count. Missing counts
are never treated as zero. Each group sorts by count descending, then year
descending, with unavailable counts last.

SITE_DEPLOY_KEY is a write-enabled deploy key scoped to
coendevente/coendevente.github.io. Actions publishes the generated site to master,
then records the submodule, publication data, and citation cache here.

Run regression tests with `python -m unittest discover -s tests`.

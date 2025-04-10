import re
from scholarly import scholarly

def slugify(text, max_length=8):
    """
    Create a simplified slug from the given text:
      - Remove any non-alphanumeric characters.
      - Lowercase the text.
      - Limit the output to max_length characters.
    """
    slug = re.sub(r'\W+', '', text).lower()
    return slug[:max_length] if len(slug) > max_length else slug

def get_pub_type(bib):
    """
    Basic decision for publication type based on available keys.
    """
    if 'journal' in bib:
        return '@article'
    elif 'booktitle' in bib:
        return '@conference'
    else:
        return '@misc'

def generate_publication_dict(author_name, max_nr=3):
    """
    Searches for an author using scholarly, fills in publication details,
    and returns a dictionary where each key is a short publication ID and
    the value is a dictionary containing formatted fields.
    """
    pub_dict = {}
    
    # Search and fetch the author profile
    author_search = scholarly.search_author(author_name)
    try:
        author = next(author_search)
    except StopIteration:
        print("Author not found!")
        return pub_dict

    author = scholarly.fill(author)
    
    for pub in author.get('publications', []):
        filled_pub = scholarly.fill(pub)
        bib = filled_pub.get('bib', {})

        title    = bib.get('title', 'No title')
        authors  = bib.get('author', 'No author')
        year     = bib.get('pub_year', 'Unknown')
        
        # Use journal or booktitle if available
        venue = bib.get('journal') or bib.get('booktitle') or 'Unknown venue'
        
        # Create a publication key using a slug from the title
        pub_id = slugify(title)
        
        # Create HTML content (customize as needed)
        html = (
            f"<p><span class='highlight-me'>{authors}</span>, {title}, "
            f"in: <i>{venue}</i>, {year}.</p>"
            f"<div class='publication-button-group'>"
            f"<a class='knop footerknop movewithmouse w-button publication-button'>Cite</a> "
            f"<a target='_blank' class='knop footerknop movewithmouse w-button publication-button' "
            f"href='http://placeholder.url'>URL</a>"
            f"</div>\n"
        )
        
        # Create a plain-text version (you might remove extra punctuation as needed)
        only_text = f"{authors}, {title}, in: <i>{venue}</i>, {year}."
        
        # Determine publication type (this is a simple rule)
        pub_type = get_pub_type(bib)
        
        # Combine venue and year for publication details
        pub_details = f"in: <i>{venue}</i>, {year}"
        
        # Create a very basic BibTeX entry (adjust or use a dedicated package for more detail)
        bibtex = (
            f"{pub_id},\n"
            f"  author = {{{authors}}},\n"
            f"  title = {{{title}}},\n"
            f"  year = {{{year}}},\n"
            f"  venue = {{{venue}}}\n"
        )
        
        # Convert year to int if possible
        try:
            year_val = int(year)
        except (ValueError, TypeError):
            year_val = year  # leave it as is if not a proper integer
        
        # Build the dictionary entry
        pub_dict[pub_id] = {
            'html': html,
            'only_text': only_text,
            'year': year_val,
            'pub_type': pub_type,
            'pub_details': pub_details,
            'bibtex': bibtex
        }
        
        print(pub_dict[pub_id])
        
        if len(pub_dict) >= max_nr:
            break
    return pub_dict

if __name__ == "__main__":
    # Replace with the desired author name or unique identifier.
    author_name = "C. de Vente"
    
    publications = generate_publication_dict(author_name)
    
    # For demonstration, print out the dictionary.
    for pub_id, details in publications.items():
        print(f"Publication ID: {pub_id}")
        for key, value in details.items():
            print(f"  {key}: {value}\n")
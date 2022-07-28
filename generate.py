from pydoc import getpager
from urllib.request import urlopen
from black import main
from markdown import markdownFromFile
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
import json
from pathlib import Path
from bibliography import bibparser, bibwriter
import os
import io
import requests
from PIL import Image
import tempfile
import hashlib


template_env = Environment(loader=FileSystemLoader(searchpath='./'))

def get_header(title="Personal website"):
    return template_env.get_template('header.html').render(title=title)

def get_footer(include_contact=True):
    return template_env.get_template('footer.html').render(include_contact=include_contact)

def get_publications():
    with open('bibliography/content/dict_pubs.json') as f:
        all_publications = json.load(f)

    for k, v in all_publications.items():
        all_publications[k]['html'] = v['html'].replace("C. de Vente", "<span class='highlight-me'>C. de Vente</span>")
    
    return all_publications


def download_file(url):
    buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        downloaded = 0
        filesize = int(r.headers['content-length'])
        for chunk in r.iter_content(chunk_size=1024):
            downloaded += len(chunk)
            buffer.write(chunk)
            # print(downloaded/filesize)
        buffer.seek(0)
        i = Image.open(io.BytesIO(buffer.read()))
    buffer.close()

    return i



def copy_to_local(config, k, new_shortest_axis_size=None):
    v = config[k]
    if "url(" in v and ")" in v:
        url = v.split("url(")[1].split(")")[0].replace("'", "")
        if url.startswith("http"):
            im = download_file(url)
            fname = hashlib.md5(url.encode()).hexdigest()
            url_out = Path("images") / (fname + ".jpg")
        else:
            im = Image.open(Path("site/") / url)
            url_out = os.path.splitext(url)[0] + "_thumb.jpg"
        
        if new_shortest_axis_size is None:
            im_out = im
        else:
            if im.size[0] < im.size[1]:
                w = new_shortest_axis_size
                h = int(round(w / im.size[0] * im.size[1]))
            else:
                h = new_shortest_axis_size
                w = int(round(h / im.size[1] * im.size[0]))

            im_out = im.resize((w, h))

        im_out = im_out.convert('RGB')

        im_out.save(Path("site/") / url_out)

        config[k] = v.split("url(")[0] + "url('" + str(url_out) + "')" + ")".join(v.split("url(")[1].split(")")[1:])
        print(config[k])


def update_imgs_in_config(config):
    for k, v in config.items():
        if k == "thumbnail":
            copy_to_local(config, k, 512)
        elif k == "main_image":
            copy_to_local(config, k)
    

def projects():
    all_publications = get_publications()

    projects_filter_func = lambda p: (p.startswith("projects/") and p.endswith(".md"))
    all_projects = template_env.list_templates(filter_func=projects_filter_func)

    project_dict = {}

    for project_filename in all_projects:   
        project_name = Path(project_filename).stem

        project_filename_json = project_filename.replace(".md", ".json")
        with open(project_filename_json) as json_file:
            config = json.load(json_file)
        
        update_imgs_in_config(config)
        
        out_filename = f'project-{project_name}.html'
        project_dict[out_filename] = (project_filename, config)
    
    for out_filename, (project_filename, config) in project_dict.items():
        with open(project_filename) as markdown_file:
            project_text = markdown(markdown_file.read())

        if 'bib' not in config:
            bib = False
        else:
            bib = {k: all_publications[k] for k in config['bib']}

        header = get_header(config['title'])
        footer = get_footer()
        
        project_keys = [k for k in list(project_dict.keys()) if k != out_filename][:3]
        project_dict_other = {k: project_dict[k] for k in project_keys}
        projects_thumbs = template_env.get_template('project_thumbs.html').render(projects=project_dict_other, w_col_n=4, make_lists=False)
        text = header + template_env.get_template('project.html').render(
            title=config['title'],
            main_image=config['main_image'],
            main_image_position=config['main_image_position'],
            publication_date=config['publication_date'],
            bib=bib,
            project_text=project_text,
            projects=projects_thumbs
        ) + footer

        with open(os.path.join('site', out_filename), 'w') as output_file:
            output_file.write(text)


    header = get_header("Projects")
    footer = get_footer()

    projects_thumbs = template_env.get_template('project_thumbs.html').render(projects=project_dict, w_col_n=3, make_lists=True)
    projects_text = header + template_env.get_template('projects.html').render(projects=projects_thumbs) + footer
    with open('site/projects.html', 'w') as output_file:
        output_file.write(projects_text)
    
    return project_dict

def get_index_body():
    project_dict = projects()
    project_names_featured = list(project_dict.keys())[:3]
    project_dict_featured = {k: project_dict[k] for k in project_names_featured}

    projects_text = template_env.get_template('project_thumbs.html').render(projects=project_dict_featured, w_col_n=4, make_lists=False)

    return template_env.get_template('index_body.html').render(projects=projects_text)

def homepage():
    header = get_header("Home")
    index_body = get_index_body()
    footer = get_footer()

    text = header + index_body + footer
    
    with open('site/index.html', 'w') as output_file:
        output_file.write(text)


def about():
    header = get_header("About")
    body = template_env.get_template('about.html').render()
    footer = get_footer()

    text = header + body + footer
    
    with open('site/about.html', 'w') as output_file:
        output_file.write(text)


def contact():
    header = get_header("Contact")
    body = template_env.get_template('contact.html').render()
    footer = get_footer(include_contact=False)

    text = header + body + footer
    
    with open('site/contact.html', 'w') as output_file:
        output_file.write(text)


def cv():
    header = get_header("Curriculum vitae")
    body = template_env.get_template('cv.html').render()
    footer = get_footer(include_contact=True)

    text = header + body + footer
    
    with open('site/cv.html', 'w') as output_file:
        output_file.write(text)


def publications():
    header = get_header("Publications")
    all_publications = get_publications()

    keys = all_publications.keys()
    types = set([all_publications[k]['pub_type'].lower() for k in keys])
    all_publications_grouped = {}
    for type in types:
        pub_this_type = {k: v for k, v in all_publications.items() if v['pub_type'].lower() == type.lower()}
        all_years = [pub_this_type[k]['year'] for k in pub_this_type.keys()]
        years = reversed(sorted(list(set(all_years))))
        pub_this_type_sorted = {}
        for year in years:
            for k, v in pub_this_type.items():
                if v['year'] == year:
                    pub_this_type_sorted[k] = v
        all_publications_grouped[type] = pub_this_type_sorted
    
    order_types = ['@article', '@preprint', '@conference', '@inproceedings']
    order_types += list(types - set(order_types))

    def replace_pub_type_name(type):
        dct = {
            '@article': "International journal articles",
            '@conference': "Abstracts",
            '@inproceedings': "Papers in conference proceedings",
            '@phdthesis': "PhD thesis",
            '@mastersthesis': "Master thesis",
            '@patent': "Patents",
            '@book': "Books",
            '@preprint': "Preprints",
        }

        if type not in dct:
            print(type)
            return type.replace('@', '').capitalize() + 's'
        
        return dct[type]

    all_publications_grouped = {
        replace_pub_type_name(k): all_publications_grouped[k] 
        for k in order_types
    }

    body = template_env.get_template('publications.html').render(bib=all_publications_grouped)
    footer = get_footer(include_contact=True)

    text = header + body + footer
    
    with open('site/publications.html', 'w') as output_file:
        output_file.write(text)


def prepare_bib():
    bib_files_root = Path("bibliography/content/")

    with open(bib_files_root / "diag.bib") as f:
        diag_bib = f.read()

    with open(bib_files_root / "coen.bib") as f:
        coen_bib = f.read()

    publications_bib = diag_bib + '\n' + coen_bib

    with open(bib_files_root / "publications.bib", 'w') as f:
        f.write(publications_bib)

    bibparser.main()
    bibwriter.main()


def main():
    prepare_bib()
    homepage()
    about()
    contact()
    publications()
    cv()

if __name__ == "__main__":
    all_publications = get_publications()

    main()

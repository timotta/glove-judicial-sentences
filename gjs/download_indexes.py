from requests import get
from lxml.cssselect import CSSSelector
from lxml import html
from slugify import slugify
import base64
import os

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)

def has_next(file_name):
    with open(file_name, "r") as file:
        doc = html.fromstring("".join(file.readlines()))
    for el in doc.cssselect(".pagination-list .disabled a"):
        if el.text_content().strip() == 'Próximo':
            return False
    return True

def check_file(file_name):
    try:
        with open(file_name, "r") as file:
            doc = html.fromstring("".join(file.readlines()))
        return len(doc.cssselect(".SearchResults-documents")) > 0
    except:
        return False

def generate_output_file_name(url, base_output_path):
    path = "/".join(url.split("/")[3:])
    slug = slugify(path)
    base = base64.urlsafe_b64encode(bytes(slug, "utf-8")).decode("utf-8")
    folder = base.replace("=", "")[-2:].lower()
    return os.path.join(base_output_path, folder, slug)

def prepare_output_folder(output_file):
    folder = os.path.dirname(output_file)
    if not os.path.exists(folder):
        os.makedirs(os.path.dirname(output_file))

def download_if_necessary(input_url, output_file, retry=0, sleep=5):
    if retry >= 3:
        print(f"Could not correctly download {output_file}")
        return
    if not os.path.exists(output_file) or not check_file(output_file):
        print(f"Downloading to {output_file}, retry={retry}")
        prepare_output_folder(output_file)
        download(input_url, output_file)
        if not check_file(output_file):
            download_if_necessary(input_url, output_file, retry+1)
    else:
        print(f"File {output_file} already exists")

def download_all_from_base_url(base_url, base_output):
    for i in range(1000):
        page = i+1
        input_url = "%s&p=%d" % (base_url, page)
        output_file = generate_output_file_name(input_url, base_output)
        download_if_necessary(input_url, output_file)
        if not check_file(output_file):
            print(f"Stopping pages from {base_url}")
            return
        if not has_next(output_file):
            print(f"Finished all pages from {base_url}")
            return

def download_all(output):
    TOPICS = [
        "T10000007", #TRF
        "T10000009", #TRT
        "T10000010", #TJ
        "T10000004", #TST
        "T10000002", #STJ
        "T10000001", #STF
        "T10000319", #CNJ
    ]

    BASE_URL = "https://www.jusbrasil.com.br/jurisprudencia/busca?"
    BASE_URL += "q=%%22Senten%%C3%%A7a+Judicial%%22+seguro&idtopico=%s&o=data"

    for topic in TOPICS:
        base_url = BASE_URL % topic
        download_all_from_base_url(base_url, output)

download_all("/home/tiago.motta/Documents/jusbrasil")
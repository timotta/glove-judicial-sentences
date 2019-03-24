from lxml.cssselect import CSSSelector
from lxml import html
from slugify import slugify
import base64
import os
import index
import utils

def has_next(file_name):
    with open(file_name, "r") as file:
        doc = html.fromstring("".join(file.readlines()))
    for el in doc.cssselect(".pagination-list .disabled a"):
        if el.text_content().strip() == 'Próximo':
            return False
    return True

def download_all_from_base_url(base_url, base_output):
    for i in range(1000):
        page = i+1
        input_url = "%s&p=%d" % (base_url, page)
        output_file = utils.generate_output_file_name(input_url, base_output)
        utils.download_if_necessary(input_url, output_file, index.check_file)
        if not index.check_file(output_file):
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

if __name__ == "__main__":
    download_all("data/indexes")
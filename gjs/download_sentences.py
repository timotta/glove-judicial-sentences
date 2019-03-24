import os
from lxml.cssselect import CSSSelector
from lxml import html
import utils
import index
from multiprocessing import Pool
import functools
from random import shuffle

def list_indexes_files(base_folder):
    result = []
    for root, _, files in os.walk(base_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            result.append(file_path)
    return result

def fix_sentence_link(url):
    return "https:" + url.split("?")[0].split("#")[0]

def get_sentence_links(index_file_path):
    with open(index_file_path, "r") as file:
        doc = html.fromstring("".join(file.readlines()))
    result = []
    for el in doc.cssselect(".BaseSnippetWrapper-title-anchor"):
        url = fix_sentence_link(el.get("href"))
        result.append(url)
    return result

def check_file(file_name):
    try:
        with open(file_name, "r") as file:
            doc = html.fromstring("".join(file.readlines()))
        return len(doc.cssselect(".document-title")) > 0
    except:
        return False

def download_all_from_index(index_file, base_output):
    print(f"Downloading sentences from index {index_file}")
    if index.check_file(index_file):
        for input_url in get_sentence_links(index_file):
            output_file = utils.generate_output_file_name(input_url, base_output)
            utils.download_if_necessary(input_url, output_file, check_file)
            if not check_file(output_file):
                print(f"Download failed for {input_url}")
                return

def download_all(indexes_base_folder, output_path, processes=6):
    pool = Pool(processes)
    indexes = list_indexes_files(indexes_base_folder)
    shuffle(indexes)

    chunks_indexes = utils.chunks(indexes, processes)

    download = functools.partial(download_all_from_index, base_output=output_path)

    for chunk in chunks_indexes:
        pool.map(download, chunk)

if __name__ == "__main__":
    download_all(
        "data/indexes",
        "data/sentences"
    )
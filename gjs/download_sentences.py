import os
from lxml.cssselect import CSSSelector
from lxml import html
import utils
import index

def list_indexes_files(base_folder):
    result = []
    for root, _, files in os.walk(base_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            result.append(file_path)
    return result

def fix_sentence_link(url):
    only_until_path = "https:" + url.split("?")[0].split("#")[0]
    if "inteiro-teor" in only_until_path:
        return "-".join(only_until_path.split("-")[:-1])
    else:
        return only_until_path + "/inteiro-teor"
    return only_until_path

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
    if index.check_file(index_file):
        for input_url in get_sentence_links(index_file):
            output_file = utils.generate_output_file_name(input_url, base_output)
            utils.download_if_necessary(input_url, output_file, check_file)
            if not check_file(output_file):
                print(f"Download failed for {input_url}")
                return

def download_all(indexes_base_folder, output_path):
    for index_file in list_indexes_files(indexes_base_folder):
        print(f"index: {index_file}")
        download_all_from_index(index_file, output_path)

download_all(
    "/home/tiago.motta/Documents/jusbrasil/indexes",
    "/home/tiago.motta/Documents/jusbrasil/sentences"
)
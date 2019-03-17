from requests import get
import os
import base64
from slugify import slugify

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)

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

def download_if_necessary(input_url, output_file, check, retry=0, sleep=5):
    if retry >= 3:
        print(f"Could not correctly download {output_file}")
        return
    if not os.path.exists(output_file) or not check(output_file):
        print(f"Downloading to {output_file}, retry={retry}")
        prepare_output_folder(output_file)
        download(input_url, output_file)
        if not check(output_file):
            download_if_necessary(input_url, output_file, check, retry+1)
    else:
        print(f"File {output_file} already exists")
from lxml.cssselect import CSSSelector
from lxml import html

def check_file(file_name):
    try:
        with open(file_name, "r") as file:
            doc = html.fromstring("".join(file.readlines()))
        return len(doc.cssselect(".SearchResults-documents")) > 0
    except:
        return False
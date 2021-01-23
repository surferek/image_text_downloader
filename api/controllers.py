import requests

from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from api.util import validate_url, remove_html_tags, download_images, download_text, check_pathname, clean_text, md5


def get_whole_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        exit(-1)
    else:
        print("Successfully requested the page")
    soup = BeautifulSoup(response.content, 'html.parser')
    text = clean_text(remove_html_tags(soup.get_text()))
    text = " ".join(list(filter(None, text)))
    return text


def get_all_images(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if validate_url(img_url):
            urls.append(img_url)

    return list(dict.fromkeys(urls))


def controller_main(url, path):
    check_pathname(path)

    text = get_whole_text(url)
    download_text(text, path)

    images = get_all_images(url)
    for image in images:
        download_images(image, path)

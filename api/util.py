import os
import re
import hashlib
import requests

from tqdm import tqdm

from urllib.parse import urlparse


def validate_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def clean_text(text):
    return text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace("&nbsp", '').split(' ')


def check_pathname(pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)


def download_images(data, pathname):
    response = requests.get(data, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, data.split("/")[-1])

    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B",
                    unit_scale=True,
                    unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))


def download_text(data, pathname):
    if isinstance(data, str):
        filepath = os.path.join(pathname, f"{pathname}.txt")

        with open(filepath, "wb+") as f:
            f.write(bytes(data, encoding='UTF-8'))

        return f"{pathname}.txt"


def md5(fname, path):
    file = fname.split("/")[-1]
    hash_md5 = hashlib.md5()
    with open(os.path.join(path, file), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

import argparse
from urllib.parse import urlparse

from api.controllers import controller_main


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This script downloads all images and text from a web page")
    parser.add_argument("url", help="The URL of the web page you want to download images")
    parser.add_argument("path",
                        help="The Directory you want to store your result")

    args = parser.parse_args()
    url = args.url
    path = args.path

    if not path:
        path = urlparse(url).netloc

    controller_main(url, path)

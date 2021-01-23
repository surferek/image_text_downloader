import os
import json
import shutil

import unittest

from api.controllers import get_all_images, get_whole_text, download_images, download_text
from api.util import md5, check_pathname


class TestService(unittest.TestCase):
    url = "http://dev.zdroweda.pl/"
    path = "dev.zdroweda.pl"

    def mock_image_names(self):
        with open("resources/expected_image_names.json") as f:
            file = json.load(f)
        return file

    def mock_text(self):
        with open("resources/expected_text.json", encoding='utf-8') as f:
            file = json.load(f)
        return file

    def mock_md_sums(self):
        with open("resources/expected_md5_of_files.json", encoding='utf-8') as f:
            file = json.load(f)
        return file

    def clean(self):
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)

    def test_images_filenames(self):
        expected = self.mock_image_names()["names"]
        actual = list()
        imgs = get_all_images(self.url)
        for img in imgs:
            actual.append(img.split("/")[-1])

        self.assertCountEqual(expected, actual)

    def test_text(self):
        expected = self.mock_text()["text"]
        actual = get_whole_text(self.url)
        self.assertEqual(expected, actual)

    def test_md_sums(self):
        expected = self.mock_md_sums()["md5"]
        actual = list()

        check_pathname(self.path)

        text = get_whole_text(self.url)
        actual.append({f"{self.path}.txt": md5(download_text(text, self.path), self.path)})

        imgs = get_all_images(self.url)
        for img in imgs:
            download_images(img, self.path)
            actual.append({img.split("/")[-1]: md5(img, self.path)})

        self.assertEqual(expected, actual)
        self.clean()


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
#
# This submodule will provide iterator classes to deal with files

import os
import sys

sys.path.append(os.path.abspath("./"))

from utils.logger import Logger
from dotenv import load_dotenv
import json

# Loading dotenv
load_dotenv()


class FileIterator:
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as file:
            self.data = json.loads(file.read())

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.data) > 0:
            dic_element = self.data.pop(0)
            return dic_element

        else:
            with open(self.file, "w") as file:
                file.write(json.dumps(self.data))
            raise StopIteration


if __name__ == "__main__":
    for i in FileIterator("./crawler/saves/author_saves.json"):
        print(i)

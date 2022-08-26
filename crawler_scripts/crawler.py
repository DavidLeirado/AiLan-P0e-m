#!/usr/bin/env python3
#
# This is the entrypoint for the crawler_scripts submodule!
#
# It will hold the main class and the execution flux to be imported by the top-level main.py

import os
import sys

sys.path.append(os.path.abspath("./"))

from crawler_scripts.scrapers import Poem, ScrapPoemsURLs, ScrapAuthors


def run_author():
    ScrapAuthors()


def run_poems():
    Poem()


def run_poem_url():
    ScrapPoemsURLs()


def run():
    run_author()
    run_poem_url()
    run_poems()


if __name__ == "__main__":
    run_poem_url()
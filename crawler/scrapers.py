#!/usr/bin/env python3
#
# This submodule will hold complementary classes in order to build the main class
# that you can find in crawler.py!
import os

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

from utils.logger import Logger


class Poem:
    """
    This class gets the poem
    """

    def __init__(self, url, session):
        self.url = url
        self.s = session

        self.page = ""
        self.__get_page()

        self.poem = ""
        self.__get_poem_from_page()

    def __get_page(self):
        """
        requests
        :return:
        """
        self.page = self.s.get(self.url)
        return

    def __get_poem_from_page(self):
        """
        Gets poem text from raw page
        :return:
        """
        bs = BeautifulSoup(self.page.text, "html.parser")
        self.poem = bs.find("div", attrs={"class": "poema"}).text.strip()
        pass

    def get_poem(self):
        """
        poem getter
        :return:
        """
        return self.poem

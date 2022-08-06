#!/usr/bin/env python3
#
# This submodule will hold complementary classes in order to build the main class
# that you can find in crawler.py!
import os

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

from utils.logger import Logger

class PoesiasPage:
    url_base = "https://www.poesi.as/"
    s = requests.Session()

    @classmethod
    def get_session(cls):
        return cls.s

    @classmethod
    def get_url_base(cls):
        return cls.url_base

class Poem(PoesiasPage):
    """
    This class gets the poem
    """

    def __init__(self, poem):
        self.url = PoesiasPage.get_url_base() + "/" + poem
        self.s = PoesiasPage.get_session()

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

# class Author:
#     """
#     This class is instantiated for each author and retrieves each poem available
#     """
#     def __init__(self):
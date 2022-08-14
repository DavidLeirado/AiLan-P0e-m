#!/usr/bin/env python3
#
# This submodule will hold complementary classes in order to build the main class
# that you can find in crawler.py!
import os
import sys

sys.path.append(os.path.abspath("./"))

from bs4 import BeautifulSoup
import requests
from utils.logger import Logger
from time import sleep
import re
from dotenv import load_dotenv

# Loading dotenv
load_dotenv()


class PoesiasPage:
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
    url_base = "https://www.poesi.as/"
    s = requests.Session()
    s.headers['User-Agent'] = agent
    # Separator for csv
    sep = os.environ.get("SCRAPER_SEPARATOR")

    @classmethod
    def get_session(cls):
        return cls.s

    @classmethod
    def get_url_base(cls):
        return cls.url_base

    @classmethod
    def update_session(cls):
        Logger.debug("Updating Session . . .")
        sleep(10)
        cls.s = requests.Session()
        cls.s.headers['User-Agent'] = cls.agent


class Poem:
    """
    This class gets the poem
    """

    def __init__(self, poem):
        self.url = PoesiasPage.get_url_base() + "/" + poem
        self.s = PoesiasPage.get_session()

        self.page = ""
        self.__get_page()

        self.poem = ""
        self.poem_name = ""
        self.__get_poem_from_page()

    def __get_page(self):
        """
        requests
        :return:
        """
        try:
            self.page = self.s.get(self.url, allow_redirects=False)
            scode = self.page.status_code
            if not scode == 200:
                Logger.warning(f"Error code from poem: {scode}")
                Logger.debug(self.page.headers)
                Logger.debug(self.page.history)
                raise Exception("Invalid status code")
        except Exception as e:
            Logger.error(e)
            PoesiasPage.update_session()
            self.__get_page()
            # sys.exit(1)
        sleep(1)

    def __get_poem_from_page(self):
        """
        Gets poem text from raw page
        :return:
        """
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")

        try:
            self.poem = bs.find("div", attrs={"class": "poema"}).text.strip()
        except AttributeError:
            try:
                self.poem = bs.find("td", attrs={"align": "left"}).text.strip()
            except Exception as e:
                Logger.error(e)

        self.poem = re.sub(r"(?:\r)?\n(?:\r)?", "<SALTO>", self.poem)
        self.poem = re.sub(r"(?:<SALTO>){2}", "<SALTO>", self.poem)
        try:
            self.poem_name = self.poem.split('<SALTO>')[0]
        except:
            self.poem_name = "UNKNOWN"
        Logger.debug(f"Poem: {self.poem_name}")

    def get_poem(self):
        """
        poem getter
        :return:
        """
        sep = PoesiasPage.sep
        poem = f"{self.poem_name}{sep}{self.poem}"
        return poem


class Author:
    """
    This class is instantiated for each author and retrieves each poem available
    """

    def __init__(self, author):
        self.url = PoesiasPage.get_url_base() + "/" + author
        self.s = PoesiasPage.get_session()

        self.page = ""
        self.__get_page()

        self.author = ""
        self.__get_author()

        self.poem = ""
        self.__get_poems()

    def __get_page(self):
        """
        requests
        :return:
        """
        try:
            self.page = self.s.get(self.url, allow_redirects=False)
            scode = self.page.status_code
            if not scode == 200:
                Logger.warning(f"Error code from author: {scode}")
                Logger.debug(self.page.headers)
                Logger.debug(self.page.history)
                raise Exception(f"Invalid status code: {scode}")
        except Exception as e:
            Logger.error(e)
            PoesiasPage.update_session()
            self.__get_page()
            # sys.exit(1)

    def __get_author(self):
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")
        try:
            self.author = bs.find("header").find("h1").text
        except AttributeError:
            self.author = bs.find("body").find("center").findChild("div").text.strip()
        Logger.debug(f"Author: {self.author}")

    def __get_poems(self):
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")

        self.poems = bs.find_all("a", attrs={"target": "_top"})
        sep = PoesiasPage.sep
        self.poems = [sep.join((self.author, Poem(i["href"]).get_poem())) for i in self.poems if i.text != ""]

    def get_author_lines(self):
        return self.poems


class ScrapPoesia:
    """
    This class is instantiated for each author and retrieves each poem available
    """

    def __init__(self):
        self.url = PoesiasPage.get_url_base()
        self.s = PoesiasPage.get_session()

        self.page = ""
        self.__get_page()

        self.authors = []
        self.__get_authors()

        self.lines = []
        for author in self.authors:
            self.__get_lines(author)

    def __get_page(self):
        """
        requests
        :return:
        """
        try:
            self.page = self.s.get(self.url, allow_redirects=False)
            scode = self.page.status_code
            if not scode == 200:
                Logger.warning(f"Error code from main page: {scode}")
                Logger.debug(self.page.headers)
                Logger.debug(self.page.history)
                raise Exception("Invalid status code")
        except Exception as e:
            Logger.error(e)
            PoesiasPage.update_session()
            self.__get_page()
            # sys.exit(1)

    def __get_authors(self):
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")
        self.authors = bs.find("select", attrs={"class": "borde1"}).find_all("option")
        self.authors = [i["value"] for i in self.authors if i["value"] != ""]

    def __get_lines(self, author):
        auth_lines = Author(author).get_author_lines()
        self.lines += auth_lines

        if len(self.lines) >= 50:
            Logger.debug("Saving poems. . .")
            self.__save_lines()

    def __save_lines(self):
        with open(os.path.abspath("./spanish_poems_dataset.csv"), "ab") as poemsFile:
            lines = "\n".join(self.lines).encode("utf-8")
            poemsFile.write(lines)

        Logger.debug(f"{len(self.lines)} poems added to DataSet")
        self.lines = []


if __name__ == "__main__":
    # with open("./spanish_poems_dataset.csv", "r", encoding="utf8") as poemFile:
    #     print(poemFile.read())
    with open("./spanish_poems_dataset.csv", "wb") as poemFile:
        headers = f"Author{PoesiasPage.sep}PoemTitle{PoesiasPage.sep}Poem\n"
        poemFile.write(headers.encode("utf-8"))
    ScrapPoesia()

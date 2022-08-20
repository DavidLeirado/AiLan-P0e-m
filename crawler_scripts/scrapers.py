#!/usr/bin/env python3
#
# This submodule will hold complementary classes in order to build the main class
# that you can find in crawler_scripts.py!
import os
import sys

sys.path.append(os.path.abspath("./"))

from bs4 import BeautifulSoup
import requests
from utils.logger import Logger
from time import sleep
import re
from dotenv import load_dotenv
from crawler_scripts.file_writer import DataSaver
from crawler_scripts.iterators import FileIterator

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

    def __init__(self):
        self.s = PoesiasPage.get_session()

        self.saver = DataSaver("./crawler_scripts/saves/spanish_poems_dataset.json")
        self.iterator = FileIterator("./crawler_scripts/saves/poems_urls_saves.json")

        self.page = ""
        self.poem = ""
        self.poem_data = {
            "auth_name": "",
            "poem_title": "",
            "poem": ""
        }
        self.data = []

        for dic_data in self.iterator:
            url = PoesiasPage.get_url_base() + "/" + dic_data["poem_url"]
            self.__get_page(url)
            self.__get_poem_from_page(dic_data["auth_name"], dic_data["poem_title"])
            sleep(1)
            
        self.saver.save(self.data)
        self.data = []

    def __get_page(self, url):
        """
        requests
        :return:
        """
        try:
            self.page = self.s.get(url, allow_redirects=False)
            scode = self.page.status_code
            if not scode == 200:
                Logger.warning(f"Error code from poem: {scode}")
                Logger.debug(self.page.headers)
                Logger.debug(self.page.history)
                raise Exception("Invalid status code")
        except Exception as e:
            Logger.error(e)
            PoesiasPage.update_session()
            self.__get_page(url)
        sleep(1)

    def __get_poem_from_page(self, auth, title):
        """
        Gets poem text from raw page
        :return:
        """
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")

        try:
            poem = bs.find("div", attrs={"class": "poema"}).text.strip()
        except AttributeError:
            try:
                poem = bs.find("td", attrs={"align": "left"}).text.strip()
            except Exception as e:
                Logger.error(e)
                pass

        try:
            poem = re.sub(r"(?:\r)?\n(?:\r)?", "<SALTO>", poem)
            poem = re.sub(r"(?:<SALTO>){2}", "<SALTO>", poem)

            self.poem_data["auth_name"] = auth
            self.poem_data["poem_title"] = title
            self.poem_data["poem"] = poem

            self.data.append(self.poem_data.copy())

            if len(self.data) > 100:
                self.saver.save(self.data)
                self.data = []
            Logger.debug(f"Poem: {title}")

        except Exception as e:
            Logger.error(e)
            pass





class ScrapPoemsURLs:
    """
    This class is instantiated for each author and retrieves each poem available
    """

    def __init__(self):
        self.s = PoesiasPage.get_session()

        self.saver = DataSaver("./crawler_scripts/saves/poems_urls_saves.json")
        self.iterator = FileIterator("./crawler_scripts/saves/author_saves.json")

        self.page = ""
        self.poem = {
            "auth_name": "",
            "poem_title": "",
            "poem_url": ""
        }
        self.data = []

        for dic_data in self.iterator:
            url = PoesiasPage.get_url_base() + "/" + dic_data["auth_url"]
            self.__get_poems_url(url)
            self.__get_poems(dic_data["auth_name"], dic_data["poem_title"])
            sleep(1)

    def __get_poems_url(self, url):
        """
        requests
        :return:
        """
        try:
            self.page = self.s.get(url, allow_redirects=False)
            scode = self.page.status_code
            if scode >= 400:
                pass
            elif not scode == 200:
                Logger.warning(f"Error code from author: {scode}")
                Logger.debug(self.page.headers)
                Logger.debug(self.page.history)
                raise Exception(f"Invalid status code: {scode}")
        except Exception as e:
            Logger.error(e)
            PoesiasPage.update_session()
            self.__get_poems_url(url)

    def __get_poems(self, auth_name, title):
        bs = BeautifulSoup(self.page.content.decode("utf-8", 'ignore'), "html.parser")

        self.poems = bs.find_all("a", attrs={"target": "_top"})
        for i in self.poems:
            if i.text != "":
                self.poem["auth_name"] = auth_name
                self.poem["poem_title"] = i.text
                self.poem["poem"] = i["href"]
                Logger.debug(f"Author: {self.poem['auth_name']} - Poem: {self.poem['poem_title']}")
                self.data.append(self.poem.copy())

            if len(self.data) > 100:
                self.saver.save(self.data)
                self.data = []

        if len(self.data) > 0:
            self.saver.save(self.data)
            self.data = []


class ScrapAuthors:
    """
    This class is instantiated for each author and retrieves each poem available
    """

    def __init__(self):
        self.url = PoesiasPage.get_url_base()
        self.s = PoesiasPage.get_session()

        self.saver = DataSaver("./crawler_scripts/saves/author_saves.json")

        self.page = ""
        self.__get_page()

        self.author = {
            "auth_name": "",
            "auth_url": ""
        }
        self.data = []
        self.__get_authors()

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
        authors = bs.find("select", attrs={"class": "borde1"}).find_all("option")

        for i in authors:
            if i["value"] != "":
                self.author["auth_name"] = i.text
                self.author["auth_url"] = i["value"]
                Logger.debug(f"Author: {self.author['auth_name']}")
                Logger.debug(f"Url for author: {self.author['auth_url']}")
                self.data.append(self.author.copy())

            if len(self.data) > 100:
                self.saver.save(self.data)
                self.data = []

        if len(self.data) > 0:
            self.saver.save(self.data)
            self.data = []


if __name__ == "__main__":
    # with open("./spanish_poems_dataset.csv", "r", encoding="utf8") as poemFile:
    #     print(poemFile.read())
    ScrapAuthors()
    ScrapPoemsURLs()

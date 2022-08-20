#!/usr/bin/env python3
#
# This submodule will provide clases to write to files

from utils.logger import Logger
import json
import os


class DataSaver:
    def __init__(self, file):
        self.file = file
        with open(self.file, "w") as f:
            f.write(json.dumps([]))

    def __read_data(self):
        if self.file != "":
            with open(self.file, "r") as f:
                data = f.read()
                if data != "":
                    data = json.loads(data)
                else:
                    data = []
            return data
        else:
            Logger.error("Impossible to read data, empty path")

    def save(self, data: list):
        """
        Method to save data to specified file
        :param data: list of dicts
        :return:
        """
        Logger.info("Saving status...")
        self.__ensure_exists_path()
        old_data = self.__read_data()
        save_data = old_data + data
        with open(self.file, "w") as f:
            f.write(json.dumps(save_data))

    def __ensure_exists_path(self):
        path = os.path.dirname(os.path.abspath(self.file))
        file_path = os.path.abspath(self.file)
        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(file_path):
            with open(file_path, "x"):
                pass

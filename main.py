from utils.logger import Logger
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()

    debug_mode = True if bool(int(os.environ.get("DEBUG", 0))) else False

    #logger = Logger(name="Main", debug=debug_mode)
    Logger.info("Application starting")
    Logger.debug("Debug mode: on!")

import logging
import os
import configparser


class Constants:
    _config = configparser.ConfigParser()
    _config.read("resources/config.ini")

    TEST_TIMEOUT = os.environ.get("TEST_TIMEOUT", int(_config["DEFAULT"]["TEST_TIMEOUT"]))
    ERROR_TIMEOUT = os.environ.get("ERROR_TIMEOUT", int(_config["DEFAULT"]["ERROR_TIMEOUT"]))
    API_ID = os.environ.get("API_ID", _config["DEFAULT"]["API_ID"])
    API_HASH = os.environ.get("API_HASH", _config["DEFAULT"]["API_HASH"])
    ACCOUNT = os.environ.get("ACCOUNT", _config["DEFAULT"]["ACCOUNT"])
    API_KEY_BOT = os.environ.get("API_KEY_BOT", _config["DEFAULT"]["API_KEY_BOT"])
    DB_URL = os.environ.get("DB_URL", _config["DEFAULT"]["DB_URL"])


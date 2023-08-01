import logging
import os
import sys
import pytest as pytest
from argparse import ArgumentParser

import yaml
from yaml import FullLoader
from start_tests import DIR, MyPlugin
from settings.converter_model import Converter


def run_tests(env: str):
    if env == 'prod':
        sys.exit(
            pytest.main(["-v",
                         "-s",
                         "--reruns", "4", "--reruns-delay", "2",
                         "--alluredir=./allureresult"],
                        plugins=[MyPlugin()]))
    elif env == 'dev':
        sys.exit(
            pytest.main(["-v",
                         "-s",
                         "--reruns", "4", "--reruns-delay", "2",
                         "--alluredir=./allureresult"],
                        plugins=[MyPlugin()]))
    else:
        raise TypeError(f"ENV '{env}' not found")


class ConfigLoader:
    __instance = None

    DEFAULT_CONFIG_PATH = 'settings/environments.yml'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ConfigLoader, cls).__new__(cls)
        return cls.__instance

    def __del__(self):
        ConfigLoader.__instance = None

    def __init__(self, environments: dict = None):
        self.environments = environments

    @staticmethod
    def _create_parser():
        parser = ArgumentParser(
            prog='gm_cms_tests',
            description='tests run settings'
        )
        parser.add_argument(
            '--env', type=str, default="dev", help='"prod" - run prod tests, "dev" - run dev tests'
        )

        return parser

    def load_yaml_config(self, path):
        path_to_file = os.path.join(path, self.DEFAULT_CONFIG_PATH)
        with open(path_to_file) as f:
            data = yaml.load(f, Loader=FullLoader)
            return data

    def set_env(self):
        parser = self._create_parser()
        args = parser.parse_known_args()[0].__dict__

        os.environ["ENV"] = args.get("env")

        return os.getenv("ENV")

    def merge_config(self):
        """
        Если переменные среды не заданы в '.env',
        то они заполняются данными из 'enviroments.yml'
        """
        env = self.set_env()
        config_yaml = self.load_yaml_config(DIR)

        self.environments = Converter(**config_yaml[env])

        if os.getenv("UI_LOGIN"):
            self.environments.browser.login = os.getenv("UI_LOGIN")

        if os.getenv("UI_PASSWORD"):
            self.environments.browser.password = os.getenv("UI_PASSWORD")

        if os.getenv("CMS_URL"):
            self.environments.cms.cms_url = os.getenv("CMS_URL")

        if os.getenv("CMS_LOGIN"):
            self.environments.cms.cms_login = os.getenv("CMS_LOGIN")

        if os.getenv("CMS_PASSWORD"):
            self.environments.cms.cms_password = os.getenv("CMS_PASSWORD")

        if self.set_env() == "dev":
            if os.getenv("DEV_CMS_SYS_LOGIN"):
                self.environments.cms.cms_sys_login = os.getenv("DEV_CMS_SYS_LOGIN")
            if os.getenv("DEV_CMS_SYS_PASSWORD"):
                self.environments.cms.cms_sys_password = os.getenv("DEV_CMS_SYS_PASSWORD")

        if self.set_env() == "prod":
            if os.getenv("PROD_CMS_SYS_LOGIN"):
                self.environments.cms.cms_sys_login = os.getenv("PROD_CMS_SYS_LOGIN")
            if os.getenv("PROD_CMS_SYS_PASSWORD"):
                self.environments.cms.cms_sys_password = os.getenv("PROD_CMS_SYS_PASSWORD")

        if os.getenv("BOT_URL"):
            self.environments.telegram.bot_url = os.getenv("BOT_URL")

        if os.getenv("TOKEN"):
            self.environments.telegram.token = os.getenv("TOKEN")

        if os.getenv("CHAT_ID"):
            self.environments.telegram.chat_id = os.getenv("CHAT_ID")

        return self.environments


config_loader = ConfigLoader()
settings = config_loader.merge_config()

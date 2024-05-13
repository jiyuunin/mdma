import logging
import os
import sys
from functools import cache, cached_property
from typing import Iterator, Union

import yaml

from mdma.errors import MdmaMissingConfigError


class ConfigValue():

    def __init__(self, config_path: str, key: str, value: dict):
        self.config_path = config_path
        self.key = key
        self.value = value

    @cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @cache
    def _key_path(self, sub_key: str) -> str:
        return sub_key if self.key is None else f'{self.key}.{sub_key}'

    def sub_value(
        self,
        key: str,
        value: Union[dict, list, str, int]
    ) -> Union[dict, list, str, int]:
        if isinstance(value, dict):
            key_path = self._key_path(key)
            return ConfigValue(self.config_path, key_path, value)
        if isinstance(value, list):
            key_path = self._key_path(key)
            return [self.sub_value(f'{key_path}.{index}', item)
                    for index, item in enumerate(value)]
        return value

    def __getattr__(self, attribute: str) -> Union[dict, list, str, int]:
        try:
            return self.sub_value(attribute, self.value[attribute])
        except KeyError:
            key_path = self._key_path(attribute)
            self.logger.exception('No key "%s" in configuration file %s.',
                                  key_path,
                                  self.config_path)
            raise MdmaMissingConfigError(key_path)

    def __iter__(self) -> Iterator[str]:
        return iter(self.value.keys())


class Config():

    @cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @cached_property
    def program_name(self) -> str:
        return 'mdma'

    @cached_property
    def program_dir(self) -> str:
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        return os.path.abspath(os.path.dirname(__file__))

    @cached_property
    def config_path(self) -> str:
        return os.path.join(self.program_dir, 'config.yml')

    @cached_property
    def config(self) -> dict:
        with open(self.config_path) as config_file:
            return yaml.safe_load(config_file)

    @cached_property
    def config_value(self) -> ConfigValue:
        return ConfigValue(self.config_path, None, self.config)

    def __getattr__(self, attribute: str) -> Union[dict, list, str, int]:
        return getattr(self.config_value, attribute)


config = Config()

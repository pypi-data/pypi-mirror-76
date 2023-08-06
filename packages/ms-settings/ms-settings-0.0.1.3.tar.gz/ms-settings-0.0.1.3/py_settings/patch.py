#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Creation: 15/06/2020  09:16
@Author: liang
@File: patch.py
"""
import os
import re
from configparser import ConfigParser
from importlib import import_module
from pathlib import Path
from typing import Dict, Any, Optional, List


def boolean(value: str):
    return value.lower() not in ['', 'f', 'n', '0', 'false']


def patch_settings(setting_module_name: str,
                   api_env_key: str = None,
                   config_file_key: str = None,
                   valid_envs: List[str] = None):
    """
    util method for init project global setting module for later usage on project global
    """
    GlobalSettingFactory(setting_module_name, api_env_key, config_file_key, valid_envs)


class GlobalSettingFactory:
    CONFIG_FILE_KEY = '_config_files_'
    ENV_VALUE_PATTERN = r'(\$\{([^:]+)?:?(.+?)?(?:<(int|bool|str|float)>)?\})'  # ${ENV_name:DEFAULT_VALUE<type>}
    NORMAL_VALUE_PATTERN = r'(.+)?(?:<(int|bool|str|float)>)'
    API_ENV_KEY = 'API_ENV'
    VALID_ENVS = ['default', 'test', 'development', 'homolog', 'staging', 'production']
    CONVERTER_MAP = {'int': int, 'str': str, 'bool': boolean, 'float': float}

    def __init__(self,
                 setting_module_name: str,
                 api_env_key: str = None,
                 config_file_key: str = None,
                 valid_envs: List[str] = None):
        try:
            self._setting_module_name = setting_module_name
            self._module = import_module(setting_module_name)
        except Exception as e:
            raise e
        else:

            if api_env_key:
                self.API_ENV_KEY = api_env_key

            if valid_envs:
                self.VALID_ENVS = valid_envs

            if config_file_key:
                self.CONFIG_FILE_KEY = config_file_key

            self._module_path = Path(self._module.__file__).parent
            self._module_options = self._extract_module_options()
            self._module_config_files = getattr(self._module, self.CONFIG_FILE_KEY, [])

            # we need to detect the environment before parse file configurations
            self.current_env = self._parser_option_value(self._module_options.get(self.API_ENV_KEY))
            self._file_options = self._extract_config_file_options()

            self._merge_files_options()

            self._patch_setting_module_option_values()

    def _extract_module_options(self) -> Dict:
        """
       Extract all configuration options from the given settings module
        """
        return {k: getattr(self._module, k) for k in dir(self._module) if k.isupper()}

    def _extract_config_file_options(self) -> Dict:
        """
        Extract all configuration options from configuration files from the given settings module
        """
        parser = ConfigParser()
        global_file_options = {}
        for filename in self._module_config_files:
            config_path = self._module_path / filename
            if not config_path.exists():
                raise Warning(f'Configuration file: {config_path} not found!')
            parser.read(config_path)
            sections = parser.sections()
            non_valid_sections = set(sections) - set(self.VALID_ENVS)
            if non_valid_sections:
                raise Warning(f'Invalid config sections: {sections} in file {config_path}')
            current_options = dict(parser.items('default')) if parser.has_section('default') else {}
            current_options.update(parser.items(self.current_env) if parser.has_section(self.current_env) else {})
            invalid_environment_variables = {
                key.upper(): value
                for key, value in current_options.items() if re.match(self.ENV_VALUE_PATTERN, value)
            }
            if invalid_environment_variables:
                raise Warning(
                    f'Environment variables {invalid_environment_variables} should be declared in python settings module!'
                )

            global_file_options.update(current_options)
        return {key.upper(): value for key, value in global_file_options.items()}

    def _merge_files_options(self):
        """
        Merge the configuration options into the module options
        """
        non_valid_options = set(self._file_options.keys()) - set(self._module_options.keys())
        if non_valid_options:
            raise Warning(
                f'Configuration fields: {non_valid_options} should be declared in {self._setting_module_name}!')
        self._module_options.update(self._file_options)

    def _parser_option_value(self, config_value: str) -> Optional[Any]:
        """
        Parse the config option's value which consider the environment variable and datatype
        """
        if not isinstance(config_value, str):
            return config_value
        match = re.match(self.ENV_VALUE_PATTERN, config_value)
        if match:
            env_name, default_value, value_type = match.groups()[1:]
            final_value = os.environ.get(env_name, default_value)
            if value_type:
                return self.CONVERTER_MAP[value_type](final_value)
            return final_value

        match = re.match(self.NORMAL_VALUE_PATTERN, config_value)
        if match:
            value, value_type = match.groups()
            if value_type:
                return self.CONVERTER_MAP.get(value_type, str)(value)

        return config_value

    def _patch_setting_module_option_values(self):
        for k, v in self._module_options.items():
            if v is not None:
                v = self._parser_option_value(v)
                self._module_options[k] = v
                setattr(self._module, k, v)

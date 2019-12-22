#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 配置管理

import configparser as config_parser
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))


def get_config(section, option, file_path='conf/apollo.ini'):
    file_path = os.path.join(BASE_DIR, file_path)
    if os.getenv(option, None):
        if os.getenv(option):
            return os.getenv(option)

    conf = config_parser.RawConfigParser()
    conf.read_file(open(file_path))
    if conf.has_section(section):
        if conf.has_option(section, option):
            conf_value = conf.get(section, option)
            return conf_value
        else:
            return None
    else:
        return None

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils.apollo_handler import apo_client, apollo_config
from utils.apollo_handler import get_apollo_conf


def ini_file_conf(file_path, section, param):
    conf_value = get_conf(param, section, file_path)

    return conf_value


def env_file_conf(conf_name, conf_type='string'):

    conf_value = os.getenv(conf_name, None)

    if conf_type == 'int' and conf_value:
        conf_value = int(conf_value)
    if conf_type == 'bool' and conf_value:
        if conf_value.upper() == 'TRUE':
            conf_value = True
        else:
            conf_value = False

    return conf_value


def apollo_envs_conf(conf_name, namespace, conf_type='string'):
    ENV_TYPE = env_file_conf("ENV_TYPE")
    APOLLO_HOST, APOLLO_PORT, APOLLO_CLUSTER, APOLLO_NAMESPACE, APOLLO_APP_ID = get_apollo_conf(ENV_TYPE)
    client = apo_client(
        APOLLO_APP_ID,
        config_server_url='http://' + APOLLO_HOST + ':' + APOLLO_PORT,
        cluster=APOLLO_CLUSTER,
        timeout=300
    )

    client.start()

    apo_value = apollo_config(client, conf_name=conf_name, default_val=None, namespace=namespace)

    if conf_type == 'int' and apo_value:
        apo_value = int(apo_value)
    if conf_type == 'bool' and apo_value:
        if apo_value.upper() == 'TRUE':
            apo_value = True
        else:
            apo_value = False

    client.stop()

    return apo_value


def get_conf(conf_name, namespace='application', conf_type='string'):

    apollo_value = apollo_envs_conf(conf_name, namespace=namespace, conf_type=conf_type)

    env_file_value = env_file_conf(conf_name, conf_type=conf_type)

    config_value = apollo_value if apollo_value else env_file_value

    return config_value

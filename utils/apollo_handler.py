#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from pyapollo import ApolloClient
from utils.get_configure import ini_file_conf

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))


def get_apollo_conf(env_type, conf_file="conf/apollo.ini"):
    apollo_conf_file = os.path.join(BASE_DIR, conf_file)
    APOLLO_HOST = ini_file_conf(apollo_conf_file, env_type, "host")
    APOLLO_PORT = int(ini_file_conf(apollo_conf_file, env_type, "port"))
    APOLLO_CLUSTER = ini_file_conf(apollo_conf_file, env_type, "cluster")
    APOLLO_NAMESPACE = ini_file_conf(apollo_conf_file, env_type, "namespace")
    APOLLO_APP_ID = ini_file_conf(apollo_conf_file, env_type, "app_id")

    return APOLLO_HOST, APOLLO_PORT, APOLLO_CLUSTER, APOLLO_NAMESPACE, APOLLO_APP_ID


def apo_client(app_id, **kwargs):
    ap_client = ApolloClient(app_id=app_id, **kwargs)
    return ap_client


def apollo_config(apollo_client, conf_name=None, default_val=None, namespace=None):
    conf_value = apollo_client.get_value(conf_name, default_val=default_val, namespace=namespace)

    return conf_value


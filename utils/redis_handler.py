# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import redis

from utils.get_configure import get_conf

_logger = logging.getLogger(__name__)


def get_redis_conf():
    namespace = "redis"
    REDIS_DB = get_conf("REDIS_DB", namespace=namespace)
    REDIS_HOST = get_conf("REDIS_HOST", namespace=namespace)
    REDIS_PORT = get_conf("REDIS_PORT", namespace=namespace, conf_type="int")
    REDIS_PASS = get_conf("REDIS_PASS", namespace=namespace)

    return REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASS


def redis_handle():
    host, port, db, password = get_redis_conf()
    r = redis.Redis(host=host, port=port, db=db, password=password)
    return r

# -*- coding: utf-8 -*-
# @Time    : 2024/06/27
# @Author  : Derek

import logging
from .base import Client
from .config import ConfigurationManager
from .constants import *
from typing import Dict, List

config_manager = ConfigurationManager()

## add default config
config_manager.configure(name="deepnlp", endpoint=KEY_ENDPOINT_BASE_URL_V2)
config_manager.configure(name=KEY_ENDPOINT_REGISTER_V2, endpoint=KEY_ENDPOINT_REGISTER_V2_URL)
config_manager.configure(name=KEY_ENDPOINT_REGISTER_V1, endpoint=KEY_ENDPOINT_REGISTER_V1_URL)
config_manager.configure(name="aiagenta2z", endpoint=KEY_ENDPOINT_BASE_URL_AIAGENTA2Z_V2)

## Default Registry Endpoint: https://www.deepnlp.org/api/ai_agent_marketplace/registry
_default_client = Client(endpoint=KEY_ENDPOINT_REGISTER_V2_URL)

DEFAULT_CONFIG_NAME = "deepnlp"

def set_endpoint(config_name="", url=""):
    """
        priority:
        P1: first set config_name,
        P2: set using the url
    """
    if config_name == "" and url == "":
        return
    if config_name != "":
        config = config_manager.get_config(config_name)
        if config is not None:
            _default_client.set_endpoint(config.endpoint)
    else:
        if url != "":
            _default_client.set_endpoint(url)

def set_endpoint_from_params(params):
    """ Check if params contains config keys
    """
    if KEY_CONFIG_NAME in params or KEY_URL in params:
        config_name = params[KEY_CONFIG_NAME] if KEY_CONFIG_NAME in params else ""
        url = params[KEY_URL] if KEY_URL in params else ""
        set_endpoint(config_name, url)
    else:
        # without setting endpoint using defaujt
        set_endpoint(DEFAULT_CONFIG_NAME, "")

def get(resource_id, **params):
    set_endpoint_from_params(params)
    return _default_client.get(resource_id)

def add(data: Dict, **params):
    return _default_client.add(data, **params)

def delete(resource_id, **params):
    set_endpoint_from_params(params)
    return _default_client.delete(resource_id)

def list(**params):
    set_endpoint_from_params(params)
    return _default_client.list(**params)

def search(**query_params):
    set_endpoint_from_params(query_params)
    print('GET Endpoint %s' % _default_client.endpoint)
    return _default_client.search(**query_params)

def search_batch(query_params_list):
    if len(query_params_list) > 0:
        set_endpoint_from_params(query_params_list[0])
    print('GET Endpoint %s' % _default_client.endpoint)        
    return _default_client.search_batch(query_params_list)

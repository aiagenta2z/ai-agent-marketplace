# -*- coding: utf-8 -*-
# @Time    : 2024/06/27
# @Author  : Derek

from .base import *

SUPPORTED_APIS = {
}

def search(q, **kwargs):
    
    api_cls = SearchFunctionAPI(None)
    res_dict = {}
    try:
        # required fields
        res_dict = api_cls.api(q, **kwargs)
    except Exception as e:
        print (e)
    return res_dict

def add(access_key, name, item_info, **kwargs):
    """
        item: dict of item information
        **kwargs: external attributes
    """
    api_cls = AddServiceAPI(None)
    res_dict = {}
    try:
        res_dict = api_cls.api(access_key, name, item_info, **kwargs)
    except Exception as e:
        print (e)
    return res_dict

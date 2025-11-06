# -*- coding: utf-8 -*-
# @Time    : 2025/03/01

import requests
import json
from bs4 import BeautifulSoup
import re
import os
import sys
import pkg_resources

import time
import datetime
import codecs

import cachetools
from cachetools import cached, TTLCache
import func_timeout
from func_timeout import func_set_timeout
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

API_NAME_SEARCH = "api_search"
API_NAME_ADD_SERVICE = "api_add_service"
API_AI_AGENT_MARKETPLACE_ENDPOINT = "http://www.deepnlp.org/api/ai_agent_marketplace/v1"
MOCK_ACCESS_KEY = "${your_access_key}"

def read_file(file_path):
    lines = []
    lines_clean = []
    try:
        with codecs.open(file_path, "r", "utf-8") as file:
            lines = file.readlines()
        for line in lines:
            line_clean = line.strip()
            line_clean = line_clean.replace("\n", "")
            lines_clean.append(line_clean)
    except Exception as e:
        print ("DEBUG: read_file failed file_path %s" % file_path)
        print (e)
    return lines_clean

class BaseAPI(object):
    """docstring for ClassName"""
    def __init__(self, configs):
        self.configs = configs
        
    def api(self, kwargs):
        """
            Args:
                kwargs: dict, 
            Return:
                res_dict: dict
        """
        # input
        # output
        res_dict={}
        return res_dict

class SearchFunctionAPI(BaseAPI):
    """
        Args:
            kwargs key value params
            
            q: str
            kwargs: dict
                limit: int, maximum 100 will be returned
                timeout: 5
        Output:
            res_dict_list: list of dict
    """
    def __init__(self, configs):
        super(SearchFunctionAPI, self).__init__(configs)
        self.name = API_NAME_SEARCH
        self.base_request_uri = API_AI_AGENT_MARKETPLACE_ENDPOINT
        self.timeout = 5
        self.limit_default = 100

    def api(self, q, **kwargs):
        data = {}
        msg = ""
        try:
            if q is None or q == "":
                print ("DEBUG: Input query q is empty, set to mock search result...")
                result = get_mock_search_result()
                return result
            # print ("DEBUG: Input kwargs is %s" % str(kwargs))
            limit = kwargs["limit"] if "limit" in kwargs else self.limit_default
            timeout = kwargs["timeout"] if "timeout" in kwargs else self.timeout
            if not isinstance(limit, int):
                limit = self.limit_default
            if not isinstance(timeout, int):
                timeout = self.timeout
            # required param
            input_param = {}
            input_param["q"] = q 
            input_param["limit"] = limit 
            url = self.base_request_uri
            kwparam_list = []
            for key, value in input_param.items():
                cur_kvparam = "%s=%s" % (str(key), str(value))
                kwparam_list.append(cur_kvparam)
            # print ("DEBUG: kwparam_list is %s" % str(kwparam_list))
            kvparam = "&".join(kwparam_list)
            if kvparam != "":
                url = self.base_request_uri + "?" + kvparam
            else:
                url = self.base_request_uri
            try:
                print ("DEBUG: SearchFunctionAPI fetch url from %s" % url)
                result = requests.get(url, timeout=timeout)
                if result.status_code == 200:
                    data = result.json()
                else:
                    data = {}
                # print ("DEBUG: Response status %d" % (result.status_code))                
            except Exception as e2:
                print ("ERROR: requests.get url failed %s" % url)
                print (e2)
        except Exception as e:
            print ("ERROR: SearchFunctionAPI api() failed q %s and input kwargs %s" % (q, str(kwargs)))
            print (e)
        return data

def get_sug_by_name(content_name):
    """
        input: content_name
        note: only english, number and space are allowed in the content_name
    """
    content_name_clean =re.sub(r'[^a-zA-Z0-9 ]', '', content_name)
    content_name_lower = content_name_clean.lower()
    content_name_lower_seg = content_name_lower.split(" ")
    content_name_sug = "-".join(content_name_lower_seg)
    return content_name_sug

def get_mock_search_result():
    """ read mock data from 
    """
    try:
        if sys.version_info <= (3, 9):
            from importlib_resources import files
        else:
            from importlib.resources import files
        data_folder_path = str(files('ai_agent_marketplace.data'))
        input_file = os.path.join(data_folder_path, "search_api_demo.json")
        print ("DEBUG: get_mock_search_result reading input file %s" % input_file)
        lines = read_file(input_file)
        input_str = lines[0] if len(lines) > 0 else "{}"
        result = json.loads(input_str)
        return result
    except Exception as e:
        print ("ERROR: get_mock_search_result failed...")
        print (e)
        return {}

def get_mock_addservice_result():
    """ read mock data from 
    """
    try:
        if sys.version_info <= (3, 9):
            from importlib_resources import files
        else:
            from importlib.resources import files
        data_folder_path = str(files('ai_agent_marketplace.data'))
        input_file = os.path.join(data_folder_path, "add_service_api_demo.json")
        print ("DEBUG: get_mock_addservice_result reading input file %s" % input_file)
        lines = read_file(input_file)
        input_str = lines[0] if len(lines) > 0 else "{}"
        result = json.loads(input_str)
        return result
    except Exception as e:
        print ("ERROR: get_mock_addservice_result failed...")
        print (e)
        return {}

class AddServiceAPI(BaseAPI):
    """
        Args:
            kwargs key value params
        Output:
            result: dict
    """
    def __init__(self, configs):
        super(AddServiceAPI, self).__init__(configs)
        self.name = API_NAME_ADD_SERVICE
        self.base_request_uri = API_AI_AGENT_MARKETPLACE_ENDPOINT
        self.keys_required = ["content"]
        self.keys_optional = ["website", "field", "subfield", "content_tag_list", "github", "price", "api", "thumbnail_picture", "upload_image_files"]
        self.KEY_PAGE_URL = "url"
        self.timeout = 5

    def api(self, access_key, name, item_info, **kwargs):
        data = {}
        msg = ""
        try:
            # check if it's mock request for demo
            if access_key == MOCK_ACCESS_KEY:
                print ("DEBUG: input access key is mocked setting to mock result, please visit http://www.deepnlp.org/workspace/keys to register your key")
                return get_mock_addservice_result()

            # required param
            input_param = {}
            input_param["access_key"] = access_key
            input_param["content_name"] = name 

            ## required keys
            if_pass_check = True
            for key in self.keys_required:
                if key not in item_info:
                    print ("ERROR: input key %s is required but missing in the item_info %s" % (key, str(item_info)))
                    if_pass_check = False 
                    break 
                else:
                    ## add key value param
                    input_param[key] = item_info[key]
            if not if_pass_check:
                print ("ERROR: Input Param Pass Check failed. ")          
                return data

            ## optional fields
            filled_fields = []
            missing_fields = []
            for key in self.keys_optional:
                if key in item_info:
                    input_param[key] = item_info[key]
                    filled_fields.append(key)
                else:
                    missing_fields.append(key)
            print ("WARN: Calling AddServiceAPI input param optional keys filled fields %s|missing_fields %s" % (str(filled_fields), str(missing_fields)))

            # timeout
            timeout = kwargs["timeout"] if "timeout" in kwargs else self.timeout
            try:
                url = self.base_request_uri
                result = requests.post(url, data = input_param, timeout=timeout)
                if result.status_code == 200:
                    data = result.json()
                    msg = "Success"
                    ai_agent_url = data[self.KEY_PAGE_URL] if self.KEY_PAGE_URL in date else ""
                    print ("DEBUG: Status %d|Msg %s" % (result.status_code, msg))
                    print ("DEBUG: Visit your uploaded AI Agent url at %s" % ai_agent_url)
                else:
                    data = {}
                    msg = "Failure"
                    print ("DEBUG: Status %d|Msg %s" % (result.status_code, msg))                    
            except Exception as e2:
                print ("DEBUG: AddServiceAPI failed with input param %s" % str(input_param))
                print (e2)
        except Exception as e:
            print ("DEBUG: AddServiceAPI failed with error:")
            print (e)
        return data

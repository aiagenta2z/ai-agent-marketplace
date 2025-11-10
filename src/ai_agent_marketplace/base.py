# -*- coding: utf-8 -*-
# @Time    : 2024/06/27

import requests
import logging
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import json
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, Tuple, Union

import os, sys

from .constants import *
from .utils import *

def get_json_response(response):
    try:
        response.raise_for_status()
        if response.text == "":
            print(f"response.text empty|" + response.text + "| consider setting config or endpoint to /tools such as config_name=\"deepnlp_tool\"")
            return {}
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except JSONDecodeError:
        print("Response conten not in valid JSON|" + response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return {}

class Client:
    def __init__(self, endpoint=None):
        self.endpoint = endpoint

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def get(self, resource_id):
        self._check_endpoint()
        url = self._build_resource_url(resource_id)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def add(self, data: Dict, **query_params):
        try:
            ## defaul endpoint
            # self.set_endpoint(endpoint = KEY_ENDPOINT_REGISTER_V2_URL)
            self._check_endpoint()
            timeout = query_params.get(KEY_TIMEOUT, DEFAULT_TIMEOUT)

            input_access_key = query_params.get(KEY_ACCESS_KEY, None)
            env_api_key = os.getenv(KEY_AI_AGENT_MARKETPLACE_ACCESS_KEY)
            final_access_key = None
            if env_api_key is not None:
                final_access_key = env_api_key
            else:
                if input_access_key is not None:
                    final_access_key = input_access_key
            if final_access_key is None:
                return {"code": 500, "message": "Missing access key in environment variables 'AI_AGENT_MARKETPLACE_API_KEY' or input params 'access_key' "}
            # check if it's mock request for demo
            if final_access_key == MOCK_ACCESS_KEY:
                print ("DEBUG: input access key is mocked setting to mock result, please visit https://www.deepnlp.org/workspace/keys to register your key")
                return get_mock_addservice_result()
            github = data.get(KEY_GITHUB, "")

            ## check endpoint
            if self.endpoint == "" or self.endpoint in [KEY_ENDPOINT_REGISTER_V1_URL, KEY_ENDPOINT_REGISTER_V2_URL]:
                ## default endpoint
                self.set_endpoint(endpoint=KEY_ENDPOINT_REGISTER_V2_URL)
                # if github != "":
                #     ## registry from github url using the v2 endpoint
                #     self.set_endpoint(endpoint=KEY_ENDPOINT_REGISTER_V2_URL)
                # else:
                #     ## registry from json using the v1 default endpoint
                #     self.set_endpoint(endpoint=KEY_ENDPOINT_REGISTER_V1_URL)
            else:
                ## customized endpoint
                print(f"INFO: Setting agtm command customized endpoint to '{self.endpoint}'")

            ## check if name,content required keys are filled
            has_required_fields_filled = False 
            if data.get(KEY_NAME, "") != "" and data.get(KEY_CONTENT, "") != "":
                has_required_fields_filled = True
            else:
                has_required_fields_filled = False 
            
            if github != "" and not has_required_fields_filled:
                ## sync from Github URL, suitable for new registry api /api/ai_agent_marketplace/registry, not agent meta provided
                data[KEY_ACCESS_KEY] = final_access_key
                response = requests.post(self.endpoint, json=data, timeout=timeout)
                response.raise_for_status()
                return response.json()
            else:
                ## sync from input URL, suitable for new registry input parameters
                result = registry_api_item_info(self.endpoint, data, **query_params)
                return result

        except Exception as e:
            print (f"AI Agent Marketplace Add Method Failed with error {e}")
            return {"code": 404,
                    "message": "Internal Server Error"}

    def delete(self, resource_id):
        self._check_endpoint()
        url = self._build_resource_url(resource_id)
        response = requests.delete(url)
        response.raise_for_status()
        return self._handle_delete_response(response)

    def list(self, **params):
        self._check_endpoint()
        response = requests.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def search(self, **query_params):
        result = {}
        try:
            self._check_endpoint()
            timeout = query_params.get(KEY_TIMEOUT, DEFAULT_TIMEOUT)
            response = requests.get(self.endpoint, params=query_params, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            print(f"DEBUG: ai_agent_marketplace requests status code {response.status_code}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Error: Timeout {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Error: ConnectionError {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Other requests Error {e}")
        except ValueError as e:
            print(f"Error: Failed Result Json Error: {e}")
        except Exception as e:
            print (f"DEBUG: ai_agent_marketplace search failed with error {e}")
        return result

    def search_batch(self, params_list):
        """
            args:
                params_list: list of kvargs
            output:
                list of tuples, [(params, results)]
        """
        parallel_num = len(params_list)
        results = []
        logging.info(f"Open AI Agent Marketplace function search_batch start Execution, {parallel_num} parallel tasks..")
        with ThreadPoolExecutor(max_workers=parallel_num) as executor:
            future_to_params = {}
            futures = [executor.submit(self.search, **params) for params in params_list]
            assert len(futures) == len(params_list)
            for params, future in zip(params_list, futures):
                future_to_params[future] = params
            for future in as_completed(futures):
                try:
                    result = future.result()
                    params = future_to_params[future] if future in future_to_params else {}
                    results.append((params, result))
                except Exception as e:
                    print(f"Task failed with error: {str(e)}")
        success_cnt = len(results)
        fail_cnt = parallel_num - success_cnt
        logging.info(f"Open AI Agent Marketplace function search_batch End Execution, Success Cnt {success_cnt} Fail Cnt {fail_cnt}...")
        return results

    def get_customized_endpoint(self, params):
        """
            default endpoint:  ${endpoint}/${id}
        """
        id_value = params[KEY_ID] if KEY_ID in params else ""
        return self.endpoint + "/" + id_value

    def _build_resource_url(self, resource_id):
        return urljoin(f"{self.endpoint}/", str(resource_id))

    def _check_endpoint(self):
        if not self.endpoint:
            raise ValueError("API endpoint is not set. Use set_endpoint() to configure it.")

    @staticmethod
    def _handle_delete_response(response):
        if response.status_code == 204:
            return {"status": "success", "message": "Resource deleted successfully"}
        return response.json()

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
        if LOG_ENABLE:
            print ("DEBUG: get_mock_addservice_result reading input file %s" % input_file)
        lines = read_file(input_file)
        input_str = lines[0] if len(lines) > 0 else "{}"
        result = json.loads(input_str)
        return result
    except Exception as e:
        print ("ERROR: get_mock_addservice_result failed...")
        print (e)
        return {}

_schema_default = load_default_schema_file()

def registry_api_item_info(registry_url, item_info, **kwargs):
    """
        Register Agent Info from the 
            --config agent.json file and customized 
            --schema ./schema.json files
            --endpoint
        
        Args:
            registry_url: str
            item_info: dict
    """
    data = {}
    msg = ""
    try:
        # required param
        input_param = {}
        input_param[KEY_ACCESS_KEY] = kwargs.get(KEY_ACCESS_KEY, "")
        input_param[KEY_CONTENT_NAME] = item_info.get(KEY_NAME)

        ## input params have higher priority than default schema
        schema_dict = kwargs.get(KEY_SCHEMA_DICT, _schema_default)

        ## required keys
        if_pass_check = True
        for key in schema_dict.get(KEY_REQUIRED, []):
            if key not in item_info:
                print ("ERROR: Input invalid item_info key %s is required but missing %s" % (key, str(item_info)))
                if_pass_check = False 
                break 
            else:
                input_param[key] = item_info[key]
        if not if_pass_check:
            print ("ERROR: Input Param Pass Check failed. ")          
            return data

        ## optional fields
        filled_fields = []
        missing_fields = []
        for key in REGISTER_KEYS_OPTIONAL:
            if key in item_info:
                input_param[key] = item_info[key]
                filled_fields.append(key)
            else:
                missing_fields.append(key)
        print ("WARN: Calling AddServiceAPI input param optional keys filled fields %s|missing_fields %s" % (str(filled_fields), str(missing_fields)))

        # timeout
        timeout = kwargs[KEY_TIMEOUT] if KEY_TIMEOUT in kwargs else DEFAULT_TIMEOUT
        try:
            result = requests.post(registry_url, json = input_param, timeout=timeout)
            if result.status_code == 200:
                data = result.json()
                msg = "Success"
                ai_agent_url = data[KEY_URL] if KEY_URL in data else ""
                if LOG_ENABLE:
                    print ("DEBUG: Status %d|Msg %s" % (result.status_code, msg))
                    print ("DEBUG: You have successfully create Visit your AI Agent , Visit url at %s." % ai_agent_url)
            else:
                data = {}
                content = result.content
                if LOG_ENABLE:
                    msg = f"Failed and returned content {content}"
                    print (f"DEBUG: Status {result.status_code} and message {msg}")
        except Exception as e2:
                print ("DEBUG: AddServiceAPI failed with input param %s" % str(input_param))
                print (e2)
    except Exception as e:
            print (f"DEBUG: AddServiceAPI failed with error: {e}")
    return data

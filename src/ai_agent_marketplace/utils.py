# -*- coding: utf-8 -*-

import logging
import codecs
import os, sys
import json 
import yaml

from .constants import *

def load_config_file(file_path):
    """Loads a .json or .yaml file and returns the dictionary content."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format. Must be .json or .yaml. Your input {file_path}")
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration file: {e}", file=sys.stderr)
        sys.exit(1)

def load_custom_schema(file_path):
    """Loads a custom schema file (.json or .yaml) and returns a dict with 'required' and 'optional' keys."""
    if not file_path:
        return None  # Use default schema

    try:
        # Re-use your existing load_config_file logic
        schema_content = load_config_file(file_path)

        required_keys = schema_content.get(KEY_REQUIRED, [])
        optional_keys = schema_content.get(KEY_OPTIONAL, []) # Default to empty list if not specified

        if not isinstance(required_keys, list):
             raise ValueError("Custom schema must contain a 'required' key which is a list of strings.")
        if not isinstance(optional_keys, list):
             raise ValueError("The 'optional' key in the custom schema must be a list of strings.")

        print(f"✅ Loaded custom schema from: {file_path}")
        return {
            KEY_REQUIRED: required_keys,
            KEY_OPTIONAL: optional_keys
        }

    except Exception as e:
        print(f"Error loading custom schema file: {e}", file=sys.stderr)
        sys.exit(1)

def load_default_schema_file():
    """
        load default schema file from ./data/schema.json
    """
    if sys.version_info <= (3, 9):
        from importlib_resources import files
    else:
        from importlib.resources import files
    data_folder = str(files('ai_agent_marketplace.data'))
    schema_file = os.path.join(data_folder, "schema.json")
    return load_config_file(schema_file)

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

def git_clone(repo_url, local_path):
    command = f'git clone "{repo_url}" "{local_path}"'
    result = os.system(command)
    
    if result == 0:
        logging.debug("DEBUG: Git clone successful.")
    else:
        logging.debug("DEBUG: Git clone failed!")

def npm_install(repo):
    """
        repo: e.g. @modelcontextprotocol/sdk
    """
    command = f'npm install "{repo}"'
    result = os.system(command)
    
    if result == 0:
        logging.debug("DEBUG: npm installed %s successful." % repo)
    else:
        logging.debug("DEBUG: npm installed %s failed." % repo)

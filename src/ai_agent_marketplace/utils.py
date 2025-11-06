# -*- coding: utf-8 -*-

import logging
import codecs

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

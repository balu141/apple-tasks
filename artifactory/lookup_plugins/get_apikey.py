import requests
import logging
import json
import os
import re
import ast
from ansible import utils, errors
from ansible.plugins.lookup import LookupBase


HEADERS = {'Content-type': 'application/json'}

def get_inst_params(curr_inst, inst_params):
    instance_url = inst_params['url']
    user_name = inst_params['api_user_name']
    user_pass = inst_params['api_user_pass']

    return instance_url, user_name, user_pass

def get_user_apitoken(curr_inst, inst_params):

    instance_url, user_name, user_pass = get_inst_params(curr_inst, inst_params)

    art_url = instance_url + "/api/security/apiKey"

    result = requests.get(art_url, auth=(user_name, user_pass), headers=HEADERS)
    json_result = result.json()
    api_token = json_result['apiKey']
    status_code = result.status_code
    logging.debug("get api key : %s", json_result)
    logging.debug("api token is : %s", api_token)
    logging.debug("get return code: %s", status_code)
    return status_code, api_token

def post_user_apitoken(curr_inst, inst_params):

    instance_url, user_name, user_pass = get_inst_params(curr_inst, inst_params)

    art_url = instance_url + "/api/security/apiKey"

    result = requests.post(art_url, auth=(user_name, user_pass), json='{"apiKey":"test"}', headers=HEADERS)
    json_result = result.json()
    status_code = result.status_code
    logging.debug("post api key : %s", json_result)
    logging.debug("post return code: %s", status_code)
    return status_code, json_result

def check_token_exists(curr_inst, inst_params):

    instance_url, user_name, user_pass = get_inst_params(curr_inst, inst_params)

    art_url = instance_url + "/api/security/apiKey"

    result = requests.get(art_url, auth=(user_name, user_pass), headers=HEADERS)
    json_result = result.json()
    status_code = result.status_code
    logging.debug("check api key : %s", json_result)
    logging.debug("check return code: %s", status_code)

    if not 'apiKey' in json_result:
        return False
    else:
        return True


def get_apikey(curr_inst, inst_params):

    isExists = check_token_exists(curr_inst, inst_params)

    status_code_get =''
    api_token = ''

    if isExists == True:
        logging.debug("api token exists for the user")
        status_code_get, api_token = get_user_apitoken(curr_inst, inst_params)

    else:
        logging.debug("api token does not exist for the user")
        status_code_post, json_result_post = post_user_apitoken(curr_inst, inst_params)
        status_code_get, api_token = get_user_apitoken(curr_inst, inst_params)

    return status_code_get, api_token


class LookupModule(LookupBase):
    def run(self, terms, **kwargs):

        logging.basicConfig(filename="art_apikey_out.log", level=logging.DEBUG)

        result = []

        for term in terms:

                name, value = term.split('=')

                if name == "instances":
                    instances_dict = ast.literal_eval(value)

                    for curr_inst, inst_params in instances_dict.items():
                        logging.debug("current instance : " + curr_inst)

                        status_code, api_token = get_apikey(curr_inst, inst_params)
                        inst_api_config = {}
                        inst_api_config["instance"] = curr_inst
                        inst_api_config["user"] = inst_params['api_user_name']
                        inst_api_config["api_token"] = api_token

                        result.append(inst_api_config)

        return result

    		
		
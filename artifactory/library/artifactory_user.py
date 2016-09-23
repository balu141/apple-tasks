#!/usr/bin/env python

DOCUMENTATION = '''
---
module: artifactory_user
short_description: artifactory_user
description:
  - This module is used to create/update Artifactory Users in multiple Artifactory instances using Artifactory REST API
author: Vineela Reddy N
'''

EXAMPLES = '''
artifactory_user: 
  create_user: "apg-ro"
  topology: "full-mesh"
  instances:
    "{{ artifactory_instances }}"
'''

from ansible.module_utils.basic import *
import requests
import logging
import json
import os
import re

HEADERS = {'Content-type': 'application/json'}


def get_inst_params(data, curr_inst):
    """
    Function to get the instance connection params like url, user name and api key
    """

    instance_url = data['instances'][curr_inst]['url']
    user_name = data['instances'][curr_inst]['username']
    api_key = data['instances'][curr_inst]['apikey']

    return instance_url, user_name, api_key


def set_user_data(data):
    """
    Function to set the json config params for art user
    """
    create_user_config = get_create_user_data()
    create_user_config['name'] = data['create_user']

    if data['ro_user_email']:
        create_user_config['email'] = data['ro_user_email']
    else:
        create_user_config['email'] = data['create_user'] + "@apple.com"

    if data['ro_user_email']:
        create_user_config['email'] = data['ro_user_email']
    # else:
    #     create_user_config['email'] = data['create_user'] + "@apple.com"    

    # create_user_config['password'] = "***" ## TBD

    if data['options']:
        options = data['options']

        for cfg_key, cfg_value in options.items():
            create_user_config[cfg_key] = cfg_value

    return create_user_config


def get_create_user_data():
    """
    Function to get the json config template for art user
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_user.json')
    create_user_data = json.load(open(filename))
    return create_user_data


def get_art_user(data, curr_inst):
    """
    Function to get the art user
    """
    create_user = data['create_user']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/users/" + create_user
    result = requests.get(art_url, auth=(user_name, api_key), headers=HEADERS)
    return result


def create_art_user(in_create_user_config, data, curr_inst):
    """
    Function to create art user
    """
    create_user = data['create_user']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/users/" + create_user
    result = requests.put(art_url, auth=(user_name, api_key), json=in_create_user_config, headers=HEADERS)
    return result.status_code


def update_art_user(data, curr_inst, json_result_new):
    """
    Function to update art user
    """
    create_user = data['create_user']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/users/" + create_user
    result = requests.post(art_url, auth=(user_name, api_key), json=json_result_new, headers=HEADERS)
    return result.status_code


def art_compare_config(data, json_result):
    """
    Function to compare config for the existing art user
    with the user input config
    """
    options = data['options']

    json_result_new = json_result.copy()

    for cfg_key, cfg_value in options.items():
        json_result_new[cfg_key] = cfg_value

    logging.debug("\n existing user config : %s \n", json_result)
    logging.debug("\n update user config : %s \n", json_result_new)

    if ( json_result == json_result_new ):
        logging.debug("user config is the same")
        return False, json_result
    else:
        logging.debug("user config is different")
        return True, json_result_new


def check_user_exists(data, curr_inst):
    """
    Function to check if the given art user exists or not
    """
    result = get_art_user(data, curr_inst)

    status_code = result.status_code
    json_result = result.json()
    
    if status_code == 200:
        return True, status_code, json_result
    elif status_code == 404:
        return False, status_code, json_result


def art_user(data, curr_inst):
    """
    Wrapper function to perform the workflow
    on the given art user
    """
    create_user = data['create_user']

    ### Check if the User already exists
    is_exists, status_code, json_result = check_user_exists(data, curr_inst)

    return_status_code = ''
    ### If User exists, compare the config
    if is_exists == True and data['options']:
        is_different, json_result_new = art_compare_config(data, json_result)

        ### If different config
        if is_different == True:
            ### Update the User config
            return_status_code = update_art_user(data, curr_inst, json_result_new)

        elif is_different == False:
            return_status_code = 203

    ### User does not exist, so create a new User
    elif is_exists == False:

        ### Create the local repository in current instance for current art instance
        create_curr_inst_config = set_user_data(data)
        return_status_code = create_art_user(create_curr_inst_config, data, curr_inst)

    else:
        return_status_code = 203

    meta_failure = { 'status' : return_status_code, 'response' : "Error creating/updating user : " + create_user }

    if return_status_code == 201:
        meta_success = { 'status' : return_status_code, 'response' : "User created successfully : " + create_user }
        return False, True, meta_success

    if return_status_code == 200:
        meta_success = { 'status' : return_status_code, 'response' : "User updated successfully : " + create_user }
        return False, True, meta_success    

    elif return_status_code == 203:
        meta_success = { 'status' : return_status_code, 'response' : "No change in User Config " + create_user }
        return False, False, meta_success

    elif return_status_code == 404:
        return True, False, meta_failure

    else:
        return True, False, meta_failure

def main():

    logging.basicConfig(filename="art_user_out.log", level=logging.DEBUG)

    module = AnsibleModule(
        argument_spec=dict(
            create_user=dict(required=True),
            ro_user_email=dict(required=None),
            ro_user_pass=dict(required=None),
            instances=dict(required=True),
            options=dict(default=None)
        ),
        supports_check_mode=True
    )

    instances = module.params.get('instances')

    ### List contains the response out for each instance
    push_result = []

    ### To create topology, need to loop through instance by instance
    for curr_inst,inst_params in instances.items():

        is_error, has_changed, result = art_user(module.params, curr_inst)
        push_result.append(result)

    if not is_error:
        module.exit_json(changed=has_changed, meta=push_result)
    else:
        module.fail_json(msg="Could not create artifactory user", meta=push_result)


if __name__ == '__main__':
    main()

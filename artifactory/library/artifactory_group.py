#!/usr/bin/env python

DOCUMENTATION = '''
---
module: artifactory_group
short_description: artifactory_group
description:
  - This module is used to create/update Artifactory Groups in multiple Artifactory instances using Artifactory REST API
author: Vineela Reddy N
'''

EXAMPLES = '''
artifactory_group: 
  create_group: "apg-ro"
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


def set_group_data(data):
    """
    Function to set the json config for art group
    """
    create_group_config = get_create_group_data()
    create_group_config['name'] = data['create_group']
    return create_group_config


def get_create_group_data():
    """
    Function to get the json config template for art group
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_group.json')
    create_group_data = json.load(open(filename))
    return create_group_data


def get_art_group(data, curr_inst):
    """
    Function to get art group
    """
    create_group = data['create_group']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/groups/" + create_group
    result = requests.get(art_url, auth=(user_name, api_key), headers=HEADERS)
    return result


def create_art_group(in_create_group_config, data, curr_inst):
    """
    Function to create art group
    """
    create_group = data['create_group']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/groups/" + create_group
    result = requests.put(art_url, auth=(user_name, api_key), json=in_create_group_config, headers=HEADERS)
    return result.status_code


def update_art_group(data, curr_inst, json_result_new):
    """
    Function to update art group
    """
    create_group = data['create_group']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/groups/" + create_group
    result = requests.post(art_url, auth=(user_name, api_key), json=json_result_new, headers=HEADERS)
    return result.status_code


def art_compare_config(data, json_result):
    """
    Function to compare the existing group config
    with user input config
    """
    options = data['options']

    json_result_new = json_result.copy()

    for cfg_key, cfg_value in options.items():
        json_result_new[cfg_key] = cfg_value

    logging.debug("\n existing group config : %s \n", json_result)
    logging.debug("\n update group config : %s \n", json_result_new)

    if ( json_result == json_result_new ):
        logging.debug("group config is the same")
        return False, json_result
    else:
        logging.debug("group config is different")
        return True, json_result_new


def check_group_exists(data, curr_inst):
    """
    Function to check if the given art group exists or not
    """
    result = get_art_group(data, curr_inst)

    status_code = result.status_code
    json_result = result.json()
    
    if status_code == 200:
        return True, status_code, json_result
    elif status_code == 404:
        return False, status_code, json_result


def art_group(data, curr_inst):
    """
    Wrapper function to perform workflow on the
    given art group
    """
    create_group = data['create_group']

    ### Check if the Group already exists
    is_exists, status_code, json_result = check_group_exists(data, curr_inst)

    return_status_code = ''
    ### If Group exists, compare the config
    if is_exists == True and data['options']:
        is_different, json_result_new = art_compare_config(data, json_result)

        ### If different config
        if is_different == True:
            ### Update the Group config
            return_status_code = update_art_group(data, curr_inst, json_result_new)

        elif is_different == False:
            return_status_code = 203

    ### Group does not exist, so create a new Group
    elif is_exists == False:

        ### Create group current instance for current art instance
        create_curr_inst_config = set_group_data(data)

        return_status_code = create_art_group(create_curr_inst_config, data, curr_inst)

    else:
        return_status_code = 203

    meta_failure = { 'status' : return_status_code, 'response' : "Error creating/updating group : " + create_group }

    if return_status_code == 201:
        meta_success = { 'status' : return_status_code, 'response' : "Group created successfully : " + create_group }
        return False, True, meta_success

    if return_status_code == 200:
        meta_success = { 'status' : return_status_code, 'response' : "Group updated successfully : " + create_group }
        return False, True, meta_success    

    elif return_status_code == 203:
        meta_success = { 'status' : return_status_code, 'response' : "No change in Group Config " + create_group }
        return False, False, meta_success

    elif return_status_code == 404:
        return True, False, meta_failure

    else:
        return True, False, meta_failure

def main():

    logging.basicConfig(filename="art_group_out.log", level=logging.DEBUG)

    module = AnsibleModule(
        argument_spec=dict(
            create_group=dict(required=True),
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

        is_error, has_changed, result = art_group(module.params, curr_inst)
        push_result.append(result)

    if not is_error:
        module.exit_json(changed=has_changed, meta=push_result)
    else:
        module.fail_json(msg="Could not create artifactory group", meta=push_result)


if __name__ == '__main__':
    main()

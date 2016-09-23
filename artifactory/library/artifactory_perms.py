#!/usr/bin/env python

DOCUMENTATION = '''
---
module: artifactory_perms
short_description: artifactory_perms
description:
  - This module is used to create/update Artifactory Permission Targets in multiple Artifactory instances using 
  Artifactory REST API
author: Vineela Reddy N
'''

EXAMPLES = '''
artifactory_perms: 
  create_perms: "apg-ro"
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


def set_perms_data(data):
    """
    Function to set json config params for permissions target
    """
    create_perms_config = get_create_perms_data()
    create_perms_config['name'] = data['create_perms']
    create_perms_config['repositories'] = data['repositories']
    add_user = data['create_perms']
    user = {}
    perm_list =[]

    if data['perms_type'] == "readonly":
        perm_list = ["r"]

    elif data['perms_type'] == "publish":
        perm_list = ["r", "w", "n"]
        
    user[add_user] = perm_list
    create_perms_config["principals"]["users"].update(user)

    return create_perms_config


def get_create_perms_data():
    """
    Function to get the json config template for permissions target
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_permissions_target.json')
    create_perms_data = json.load(open(filename))
    return create_perms_data


def get_art_perms(data, curr_inst):
    """
    Function to get artifactory permissions target
    using python requests module
    """
    create_perms = data['create_perms']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/permissions/" + create_perms
    result = requests.get(art_url, auth=(user_name, api_key), headers=HEADERS)
    return result


def create_art_perms_target(in_create_perms_config, data, curr_inst):
    """
    Function to create art permissions target
    """
    create_perms = data['create_perms']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/permissions/" + create_perms
    result = requests.put(art_url, auth=(user_name, api_key), json=in_create_perms_config, headers=HEADERS)
    return result.status_code


def update_art_perms_target(data, curr_inst, json_result_new):
    """
    Function to update art permissions target
    """
    create_perms = data['create_perms']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/security/permissions/" + create_perms
    result = requests.put(art_url, auth=(user_name, api_key), json=json_result_new, headers=HEADERS)
    return result.status_code


def art_compare_config(data, json_result):
    """
    Function to compare the existing art permissions config
    with the user input config
    """
    options = data['options']

    json_result_new = json_result.copy()

    for cfg_key, cfg_value in options.items():
        if cfg_key == "repositories":
            json_result_new[cfg_key] = sorted(cfg_value)
        else:
            json_result_new[cfg_key] = cfg_value

    logging.debug("existing config : %s", json_result)
    logging.debug("updated config : %s", json_result_new)

    if ( json_result == json_result_new):
        logging.debug("perms config is the same")
        return False, json_result
    else:
        logging.debug("perms config is different")
        return True, json_result_new


def check_perms_exists(data, curr_inst):
    """
    Function to check if art perms config exists or not
    """
    result = get_art_perms(data, curr_inst)
    status_code = result.status_code
    json_result = result.json()

    if status_code == 200:
        return True, status_code, json_result
    elif status_code == 404:
        return False, status_code, json_result


def art_perms(data, curr_inst):
    """
    Wrapper function to perform the workflow
    on the given art permissions target
    """
    create_perms = data['create_perms']

    ### Check if the perms already exists
    is_exists, status_code, json_result = check_perms_exists(data, curr_inst)

    return_status_code = ''
    ### If Perms exists, compare the config
    if is_exists == True and data['options']:
        is_different, json_result_new = art_compare_config(data, json_result)

        ### If different config
        if is_different == True:
            ### Update the perms config
            return_status_code = update_art_perms_target(data, curr_inst, json_result_new)
            if return_status_code == 201:
                return_status_code = 200

        elif is_different == False:
            return_status_code = 203

    ### Perms does not exist, so create a new permission target
    elif is_exists == False:

        ### Create the Permissions target in current instance
        create_curr_inst_config = set_perms_data(data)
        return_status_code = create_art_perms_target(create_curr_inst_config, data, curr_inst)

    else:
        return_status_code = 203

    meta_failure = { 'status' : return_status_code, 'response' : "Error creating/updating Permissions Target : " + create_perms }

    if return_status_code == 201:
        meta_success = { 'status' : return_status_code, 'response' : "Permissions Target created successfully : " + create_perms }
        return False, True, meta_success

    elif return_status_code == 200:
        meta_success = { 'status' : return_status_code, 'response' : "Permissions Target updated successfully : " + create_perms }
        return False, True, meta_success

    elif return_status_code == 203:
        meta_success = { 'status' : return_status_code, 'response' : "No change in Permissions Config " + create_perms }
        return False, False, meta_success

    elif return_status_code == 404:
        return True, False, meta_failure

    else:
        return True, False, meta_failure


def main():

    logging.basicConfig(filename="art_perms_out.log", level=logging.DEBUG)

    module = AnsibleModule(
        argument_spec=dict(
            create_perms=dict(required=True),
            perms_type=dict(default='readonly'),
            repositories=dict(required=True),
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

        is_error, has_changed, result = art_perms(module.params, curr_inst)
        push_result.append(result)

    if not is_error:
        module.exit_json(changed=has_changed, meta=push_result)
    else:
        module.fail_json(msg="Could not create artifactory permissions target", meta=push_result)


if __name__ == '__main__':
    main()

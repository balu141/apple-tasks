#!/usr/bin/env python

DOCUMENTATION = '''
---
module: artifactory_repo
short_description: artifactory_repo
description:
  - This module is used to manage Artifactory repositories for multiple Artifactory instances using the Artifactory REST API's
options:
  repo_key:
    description:
      Dictionary with repository key name 
  package_type:
    description:
      Dictionary with package type like generic|maven|npm|sbt etc.
  repo_type:
    description:
      Dictionary with repo type like local|virtual|remote
  repo_layout:
    description:
      Dictionary with repo layout like maven-2-default|simple-default|npm-default etc.
  topology:
    description:
      Dictionary with topology values like none|full-mesh. Currently only these two are supported
  instances:
    description:
      Dictionary data structure having artifactory instances details on instance name, instance url, user name, api key
author: Vineela Reddy N
'''

EXAMPLES = '''
artifactory_repo: 
  repo_key: "retail-zaos-generic-local"
  package_type: "generic"
  repo_type: "local"
  repo_layout: "simple-default"
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


def get_push_replication_data():
    """
    Function to get the json config template for creating
    push replication
    """   
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_push_replication.json')
    create_push_repl_data = json.load(open(filename))
    return create_push_repl_data


def set_repo_data(data):
    """
    Wrapper function for each set repo type
    takes the data object and repo type
    creates the repository config for that type
    returns back a json config object
    """
    create_repo_config =''
    repo_type = data['repo_type']

    if repo_type == "local":
        create_repo_config = set_create_repo_local_data(data)
    elif repo_type == "virtual":
        create_repo_config = set_create_repo_virtual_data(data)
    elif repo_type == "remote":
        create_repo_config = set_create_repo_remote_data(data)

    return create_repo_config


def get_create_repo_local_data():
    """
    Function to get the json config template for creating
    art local repository
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_repo_local.json')
    create_local_repo_data = json.load(open(filename))
    return create_local_repo_data


def set_create_repo_local_data(data):
    """
    Function to set the json config parameters for creating
    art local repository
    """
    create_local_repo_config = get_create_repo_local_data()

    create_local_repo_config['key'] = data['repo_key']
    create_local_repo_config['packageType'] = data['package_type']
    create_local_repo_config['repoLayoutRef'] = data['repo_layout']
    create_local_repo_config['handleReleases'] = data['isRelease']
    create_local_repo_config['handleSnapshots'] = data['isSnapshot']
    create_local_repo_config['maxUniqueSnapshots'] = data['max_uniq_snap']
    create_local_repo_config['snapshotVersionBehavior'] = data['snap_bh']
    create_local_repo_config['suppressPomConsistencyChecks'] = data['suppressPomCheck']

    if data['options']:
        options = data['options']

        for cfg_key, cfg_value in options.items():
            create_local_repo_config[cfg_key] = cfg_value

    return create_local_repo_config


def get_create_repo_virtual_data():
    """
    Function to get the json config template for creating
    art virtual repository
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_repo_virtual.json')
    create_local_repo_data = json.load(open(filename))
    return create_local_repo_data


def set_create_repo_virtual_data(data):
    """
    Function to set the json config parameters for creating
    art virtual repository
    """
    create_virtual_repo_config = get_create_repo_virtual_data()

    create_virtual_repo_config['key'] = data['repo_key']
    create_virtual_repo_config['packageType'] = data['package_type']
    create_virtual_repo_config['repoLayoutRef'] = data['repo_layout']
    create_virtual_repo_config['repositories'] = data['repositories']
    create_virtual_repo_config['defaultDeploymentRepo'] = data['repositories'][0]

    if data['options']:
        options = data['options']

        for cfg_key, cfg_value in options.items():
            create_virtual_repo_config[cfg_key] = cfg_value

    return create_virtual_repo_config


def get_create_repo_remote_data():
    """
    Function to get the json config template for creating
    art remote repository
    """
    dir = os.getcwd()
    filename = os.path.join(dir, 'json_files/create_repo_remote.json')
    create_remote_repo_data = json.load(open(filename))
    return create_remote_repo_data


def set_create_repo_remote_data(data):
    """
    Function to set the json config parameters for creating
    art remote repository
    """
    create_remote_repo_config = get_create_repo_remote_data()

    create_remote_repo_config['key'] = data['repo_key']
    create_remote_repo_config['packageType'] = data['package_type']
    if not data['repo_layout']:
        create_remote_repo_config['repoLayoutRef'] = "simple-default"

    if data['options']:
        options = data['options']

        for cfg_key, cfg_value in options.items():
            create_remote_repo_config[cfg_key] = cfg_value

    return create_remote_repo_config


def get_art_repo(data, curr_inst):
    """
    Function to get artifactory repo using python requests module
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/repositories/" + repo_key
    result = requests.get(art_url, auth=(user_name, api_key), headers=HEADERS)
    return result


def create_art_repo(in_create_repo_config, data, curr_inst):
    """
    Function to make rest api call for artifactory repo
    using python requests module
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/repositories/" + repo_key
    result = requests.put(art_url, auth=(user_name, api_key), json=in_create_repo_config, headers=HEADERS)
    return result.status_code


def check_push_replication_exists(data, curr_inst):
    """
    Function to get push replication for curr instance local repository
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/replications/" + repo_key
    result = requests.get(art_url, auth=(user_name, api_key), headers=HEADERS)
    return result.status_code, result.json()


def create_push_replication(create_push_repl_config, data, curr_inst):
    """
    Function to create push replication for the current instance
    local repository
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/replications/multiple/" + repo_key
    result = requests.put(art_url, auth=(user_name, api_key), json=create_push_repl_config, headers=HEADERS)
    return result.status_code


def update_push_replication(in_push_repl_config, data, curr_inst):
    """
    Function to update push replication for the current instance 
    local repository
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/replications/multiple/" + repo_key
    result = requests.post(art_url, auth=(user_name, api_key), json=in_push_repl_config, headers=HEADERS)
    return result.status_code


def update_art_repo(data, curr_inst, json_result_new):
    """
    Function to update a repository if there is a change
    in the configuration
    """
    repo_key = data['repo_key']
    instance_url, user_name, api_key = get_inst_params(data, curr_inst)

    art_url = instance_url + "/api/repositories/" + repo_key
    result = requests.post(art_url, auth=(user_name, api_key), json=json_result_new, headers=HEADERS)
    return result.status_code


def get_project_from_key(repo_key, repo_type, package_type):
    """
    Function to get the project name for a given repo key
    """
    logging.debug("repo key is : " + repo_key)
    str_repo_key = re.compile("([\w-]+)"+ ".*" + package_type + ".*" + repo_type + ".*")
    str_repo_new = str_repo_key.search(repo_key).group(1)
    str_key_new = str_repo_new[:-1]
    return str_key_new


def art_compare_replication(push_list, push_json_result):
    """
    Function to compare the existing replication config
    with the generated replication config
    """
    if ( push_list == push_json_result ):
        return True
    else:
        return False


def art_create_topology(data, curr_inst):
    """
    Function to create the topology for a given topology option
    """
    repo_type = data['repo_type']
    repo_key = data['repo_key']
    package_type = data['package_type']

    ### Topology 'full-mesh', wil create local repositories in each art instance for all the art instances
    if data['topology'].lower() == "full-mesh":

        str_key_new = get_project_from_key(repo_key , repo_type, package_type)

        ### Select repo list for virtual repository
        sel_repo_list = []
        sel_repo_list.append(repo_key)

        push_list = []
        instances = data['instances']

        ### To create topology, need to loop through instance by instance
        for other_inst,other_inst_params in instances.items():
            if not other_inst == curr_inst:
                logging.debug("other instance is : " + other_inst)
                logging.debug("current instance is : " + curr_inst)

                json_local_new = {}
                json_local_new = data.copy()

                ### Build the local repo key for the remaining art instances
                repo_key_local_new = str_key_new + "-" + package_type + "-" + repo_type + "-" + other_inst

                json_local_new['repo_key'] = repo_key_local_new
                json_local_new['topology'] = "none"

                err, changed, result = art_repo(json_local_new, curr_inst)

                sel_repo_list.append(repo_key_local_new)
                logging.debug("sel repo list : %s", sel_repo_list)

                ### Dynamic config for multi push replication for each local instance               
                dynamic_config = {}   
                dynamic_config['url'] = other_inst_params['url'] + "/" + repo_key + "-" + curr_inst
                dynamic_config['username'] = other_inst_params['username']
                dynamic_config['password'] = other_inst_params['apikey']
                dynamic_config['repoKey'] = repo_key
                dynamic_config['socketTimeoutMillis'] = 15000
                dynamic_config['enableEventReplication'] = True
                dynamic_config['enabled'] = True
                dynamic_config['syncDeletes'] = False
                dynamic_config['syncProperties'] = True
                dynamic_config['cronExp'] = "0 0/9 14 * * ?"

                push_list.append(dynamic_config)

        ### Build the virtual repo key for the current art instance
        repo_key_virtual = str_key_new + "-" + package_type + "-" + "virtual"

        json_virtual_new = data.copy()

        json_virtual_new['repo_key'] = repo_key_virtual
        json_virtual_new['repo_type'] = "virtual"
        json_virtual_new['repositories'] = sel_repo_list
        json_virtual_new['topology'] = "none" 

        err, changed, result = art_repo(json_virtual_new, curr_inst)

        ### Create the multi push replication now for current instance local repository

        ## Base config for creating the multi push replication
        create_push_repl_config = get_push_replication_data()

        ### Update with the dynamic config
        create_push_repl_config['replications'] = push_list

        ### Check if push replication exists
        push_status_code, push_json_result = check_push_replication_exists(data, curr_inst)
        err_response_text = "Could not find replication"

        if push_status_code == 404 and err_response_text in push_json_result['errors'][0]['message']:
            logging.debug("creating new multi push replication for : " + curr_inst)
            logging.debug("create push replication config : %s", create_push_repl_config)
            ### Create the multi push replication now for current instance local repository

            create_status_code = create_push_replication(create_push_repl_config, data, curr_inst)      
            return create_status_code

        elif push_status_code == 200:

            logging.debug("\n create push replication config : %s \n", push_list)
            logging.debug("\n existing replication config : %s \n", push_json_result)
            is_same_config = art_compare_replication(push_list, push_json_result)

            if is_same_config == False:
                logging.debug("\n replication config is different \n")
                update_status_code = update_push_replication(create_push_repl_config, data, curr_inst)
                return 202

            else:
                logging.debug("\n replication config is the same \n")
                return 200


    elif topology.lower() == "half-mesh":
        logging.debug("do something here if you need half-mesh!!!!!")


def art_compare_config(data, json_result):
    """
    Function to compare the existing repository config
    with the input config params
    """
    options = data['options']

    #### This piece of code is a workaround for the bug in artifactory
    ### for remote repo - 'description' config param
    if data['repo_type'] == "remote":
        if 'description' in json_result and json_result['description']:
            str_new = json_result['description'].replace('(local file cache)', '')
            str_new_text = str_new.strip()
            json_result['description'] = str_new_text

    json_result_new = {}
    json_result_new = json_result.copy()

    for cfg_key, cfg_value in options.items():
        json_result_new[cfg_key] = cfg_value

    logging.debug("\n existing repo config : %s \n", json_result)
    logging.debug("\n update repo config : %s \n", json_result_new)

    if ( json_result == json_result_new ):
        logging.debug("config is the same")
        return False, json_result
    else:
        logging.debug("config is different")
        return True, json_result_new


def check_repo_exists(data, curr_inst):
    """
    Function to check for an art instance, the given repository exists
    or not
    """
    repo_key = data['repo_key']
    result = get_art_repo(data, curr_inst)
    status_code = result.status_code

    curr_repo_key = ''
    if result.json():
        json_result = result.json()
        # logging.debug("json response from api call %s", json_result)

        if status_code == 200 and 'key' in json_result:
            curr_repo_key = json_result['key']

    if status_code == 200 and curr_repo_key == repo_key:
        return True, status_code, json_result
    else: ## status_code == 400 and can be any other
        return False, status_code, json_result


def art_repo(data, curr_inst):
    """
    Wrapper function to manage art repositories for the below -
    check repository exists
    get and set the json config template
    get repository
    create repository for a given topology
    """
    topology = data['topology']
    repo_key = data['repo_key']

    ### Check if the repo already exists
    is_exists, status_code, json_result = check_repo_exists(data, curr_inst)

    return_status_code = ''
    ### If repo exists, compare the config
    if is_exists == True and data['options']:
        is_different, json_result_new = art_compare_config(data, json_result)
        logging.debug("json result of existing repository : %s", json_result)

        ### If different config
        if is_different == True:

            ### Update the repo config
            return_status_code = update_art_repo(data, curr_inst, json_result_new)
            return_status_code = 201

        elif is_different == False:
            return_status_code = 203

    ### Repo does not exist, so create a new repo
    elif is_exists == False and status_code == 400:

        ### Create the local repository in current instance for current art instance
        create_curr_inst_config = set_repo_data(data)
        logging.debug("create repo config : %s", create_curr_inst_config)
        return_status_code = create_art_repo(create_curr_inst_config, data, curr_inst)
        logging.debug("remote repository creation return code : %s", return_status_code)

    else:
        return_status_code = 203

    if not topology == "none":

        ### Create topology to create the remaining repositories for that topo type
        return_status_code = art_create_topology(data, curr_inst)

        #meta_success = { 'status' : return_status_code, 'response' : "Topology of type : " + topology + " for repo : " + repo_key + " in instance : " + curr_inst + " created successfully" }
        meta_failure = { 'status' : return_status_code, 'response' : "Error creating topology for : " + repo_key }

        if return_status_code == 201:
            meta_success = { 'status' : return_status_code, 'response' : "Topology of type : " + topology + " for repo : " + repo_key + " in instance : " + curr_inst + " created successfully" }
            return False, True, meta_success

        elif return_status_code == 202:
            meta_success = { 'status' : return_status_code, 'response' : "Topology of type : " + topology + " for repo : " + repo_key + " in instance : " + curr_inst + " updated successfully" }
            return False, False, meta_success

        elif return_status_code == 200:
            meta_success = { 'status' : return_status_code, 'response' : " No change in replication config" }
            return False, False, meta_success

        else:
            return True, False, meta_failure

    else:
        
        meta_failure = { 'status' : return_status_code, 'response' : "Error creating/updating repository : " + repo_key }

        if return_status_code == 200:
            meta_success = { 'status' : return_status_code, 'response' : "Repository created successfully : " + repo_key }
            return False, True, meta_success

        elif return_status_code == 201:
            meta_success = { 'status' : return_status_code, 'response' : "Repository updated successfully : " + repo_key }
            return False, True, meta_success

        elif return_status_code == 203:
            meta_success = { 'status' : return_status_code, 'response' : "No change in repository config : " + repo_key }
            return False, False, meta_success

        else:
            return True, False, meta_failure

def main():

    logging.basicConfig(filename="art_repo_out.log", level=logging.DEBUG)

    module = AnsibleModule(
        argument_spec=dict(
            repo_key=dict(required=True),
            package_type=dict(required=True),
            repo_type=dict(required=True),
            repo_layout=dict(default='simple-default'),
            isRelease=dict(default='False'),
            isSnapshot=dict(default='False'),
            suppressPomCheck=dict(default='False'),
            snap_bh=dict(default='non-unique'),
            max_uniq_snap=dict(default='0'),
            topology=dict(default='none'),
            instances=dict(required=True, default=None),
            options=dict(default=None),
            repositories=dict(default=None)
        ),
        supports_check_mode=True
    )

    instances = module.params.get('instances')
    topology = module.params.get('topology')
    repo_type = module.params.get('repo_type')

    instances_len = len(instances)

    logging.debug("default topology value : " + topology)
    logging.debug("instances are : %s", instances)

    #### When Topology not none and no. of art instances less than 1
    if not topology == "none" and instances_len < 2 :
        result = { 'response' : "Topology requires more than one artifactory instance" }
        module.fail_json(changed=False, msg="Could not create topology", meta=result)

    if not topology == "none" and not repo_type == "local" :
        result = { 'response' : "Topology can only be implemented for local repositories" }
        module.fail_json(changed=False, msg="Could not create topology", meta=result)

    ### List contains the response out for each instance
    push_result = []

    ### To create topology, need to loop through instance by instance
    for curr_inst,inst_params in instances.items():
        logging.debug("current instance is : " + curr_inst)

        is_error, has_changed, result = art_repo(module.params, curr_inst)
        push_result.append(result)

    if not is_error:
        module.exit_json(changed=has_changed, meta=push_result)
    else:
        module.fail_json(msg="Could not create art repository", meta=push_result)


if __name__ == '__main__':
    main()

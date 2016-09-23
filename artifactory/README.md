################################ DESCRIPTION ######################################

artifactory-onboarding playbook for automating artifactory workflow 

for creation of repositories, users and permission targets.

This playbook runs on the localhost.

###################################################################################

What does this playbook exactly do ?

Creates artifactory local repositories of types -

generic, docker, sbt, npm, pypi, gems, maven release, mavem snapshot

Creates artifactory virtual repositories of types -

maven, docker with references to respective local repositories

Creates artifactory read only and publish users.

Creates artifactory read only and publish permission targets.


-----------------------------------------------------------------------------------

What does this playbook ask for ?

Prompts the user for project name, 

readonly user password, readonly user email

publish user password, publish user email

-----------------------------------------------------------------------------------

Do I need to set/give vault password ?

Yes, to store the artifactory admin user API key.

Define the vault_admin_api_key in the vault file.
for eg. env/labt/group_vars/all/vault

Run ansible-vault and provide the password as prompted -

ansible-vault encrypt env/labt/group_vars/all/vault

-----------------------------------------------------------------------------------

How to execute this playbook for all the create roles, say for test artifactory instance ?

ansible-playbook -i env/labt artifactory-onboarding.yml --ask-vault-pass (if vault files is not configured in ansible.cfg)

-----------------------------------------------------------------------------------

How to execute this playbook for each role ?

Look up for each role tag in the master yaml file - artifactory-onboarding.yml and execute with that role tag

all examples :

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-user-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-user-publish"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-repo-local"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-maven-virtual"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-docker-virtual"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-perms-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-perms-publish"

-----------------------------------------------------------------------------------

Is there a clean up or delete yaml?

Please refer artifactory-test.yml

How to use it?

eg. ansible-playbook -i env/labt artifactory-test.yml --tags="delete-user-ro"

-----------------------------------------------------------------------------------
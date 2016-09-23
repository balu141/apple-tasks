Role Name
=========

To create artifactory permissions target ro and publish

Example Playbook
----------------

To create artifactory permissions target for readonly and publish :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-perms-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-perms-publish"

Role Name
=========

To create artifactory user ro and publish

Example Playbook
----------------

To create artifactory readonly and publish users :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-user-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-user-publish"


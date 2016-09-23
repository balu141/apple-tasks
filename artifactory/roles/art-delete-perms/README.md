Role Name
=========

To delete artifactory permissions target - ro and publish

Example Playbook
----------------

To delete artifactory permissions target readonly and publish :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="delete-perms-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="delete-perms-publish"


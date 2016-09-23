Role Name
=========

To delete artifactory ro user and publish user

Example Playbook
----------------

To delete artifactory users readonly and publish :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="delete-user-ro"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="delete-user-publish"


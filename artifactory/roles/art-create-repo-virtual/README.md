Role Name
=========

To create artifactory virtual repository

Example Playbook
----------------

To create artifactory maven and docker virtual repositories :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-maven-virtual"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-docker-virtual"

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-generic-virtual"

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).

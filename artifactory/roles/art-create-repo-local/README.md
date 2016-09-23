Role Name
=========

To create a local artifactory repository

Example Playbook
----------------

To create artifactory local repositories of type docker,sbt,npm,generic,gems,maven release and snapshot :-

ansible-playbook -i env/labt artifactory-onboarding.yml --tags="create-repo-local"


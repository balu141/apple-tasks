# java installation

### vagrant

    ansible-playbook java.yml

### DC

    ansible-playbook -i <inventory> java.yml --become --become-user=iagcit -u <user> --ask-become-pass -k
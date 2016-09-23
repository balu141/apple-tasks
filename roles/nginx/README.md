# nginx role

### vagrant

    ansible-playbook nginx.yml

### DC

    ansible-playbook -i <inventory> nginx.yml --become --become-user=iagcit -u <user> --ask-become-pass -k
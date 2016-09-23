# nexus-iq installation

### vagrant

    ansible-playbook nexus-iq.yml

### DC

    ansible-playbook -i <inventory> nexus-iq.yml --become --become-user=iagcit -u <user> --ask-become-pass -k
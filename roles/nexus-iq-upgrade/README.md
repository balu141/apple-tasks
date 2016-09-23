# nexus-iq upgrade

### vagrant

    ansible-playbook nexus-iq-upgrade.yml-v

### DC

    ansible-playbook -i <inventory> nexus-iq-upgrade.yml --become --become-user=iagcit -u <user> --ask-become-pass -k
# nexus-pro upgrade

### vagrant

    ansible-playbook nexus-upgrade.yml

### DC

    ansible-playbook -i <inventory> nexus-upgrade.yml --become --become-user=iagcit -u <user> --ask-become-pass -k

# nexus-oss upgrade

### vagrant

    ansible-playbook nexus-upgrade.yml

### DC

    ansible-playbook -i <inventory> nexus-upgrade.yml --become --become-user=iagcit -u <user> --ask-become-pass -k
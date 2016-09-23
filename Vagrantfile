# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
# Creating docker.dev
  config.vm.box = "geerlingguy/centos7"
  config.vm.hostname = "nexus.dev"
  #config.vm.provision "shell", inline: <<-SHELL
  #  mkdir /opt/local/
  #  chown vagrant:vagrant /opt/local/
  #  echo "HOME=/opt/local" >> /home/vagrant/.bashrc
  #  source /home/vagrant/.bashrc
  #SHELL
  config.vm.network :private_network, ip: "10.0.15.25"
  #config.vm.provision "shell", inline: "mkdir /opt/local/"
  #config.vm.provision "shell", inline: "chown vagrant:vagrant /opt/local/"
  #config.vm.provision "shell", inline: "chmod -R 755 /opt/local"
  #config.vm.provision :shell, path: "bootstrap.sh"
#  config.vm.provision :ansible do |ansible|
#  ansible.playbook = "playbook.yml"
#  ansible.raw_arguments  = "--ask-vault-pass"
#    ansible.verbose = true
#    ansible.limit = "all"
#    ansible.verbose = "v"
#   ansible.inventory_path = "./env/vagrant/inventory"
#    ansible.tags = "ansible-devel"
#    ansible.ask_vault_pass = true
#    ansible.tags = "docker"
#    ansible.tags = "base,ansible-devel,linuxbrew"
#    ansible.raw_arguments = ["--connection=paramiko"]
#  end
  config.vm.provider "virtualbox" do |vb|
        vb.customize ['modifyvm', :id, '--memory', '1024']
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
end

### provenance-stats

##Work in progress. Do not use!
It works on Ubuntu 14.04 LTS 32 bit only.

- ubuntu.yml: Ansible Playbook that sets up development environment for [SPADE][1], tailored for --insert details--.
- ubuntu.sh: Automates the install process by invoking Ansible.
- localhost: Required for Ansible.

### Usage

- Install Ansible:
```
sudo add-apt-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

- Let Ansible install and setup the machine:
```
source <(curl -s https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/ubuntu.sh)
```
(for debug commands, read top of ubuntu.yml)
      

  [1]: https://github.com/ashish-gehani/SPADE

  

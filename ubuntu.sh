wget https://github.com/hasanatkazmi/provenance-stats/raw/master/ubuntu.yml
wget https://github.com/hasanatkazmi/provenance-stats/raw/master/localhost
ansible-playbook -K -i localhost ubuntu.yml

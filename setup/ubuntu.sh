wget https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/setup/ubuntu.yml
wget https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/setup/localhost
ansible-playbook -K -i localhost ubuntu.yml

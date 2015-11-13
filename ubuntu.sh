wget https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/ubuntu.yml
wget https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/localhost
ansible-playbook -K -i localhost ubuntu.yml

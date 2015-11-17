git clone https://github.com/hasanatkazmi/provenance-stats.git
cd provenance-stats
ansible-playbook -K -i localhost ubuntu.yml
bash buildscripts/init.sh

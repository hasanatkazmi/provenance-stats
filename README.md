### provenance-stats

##Work in progress. Do not use!
Tested on Ubuntu 14.04 LTS 32 bit only.

- setup: Scripts related to setting up the system to run tests.
- setup/ubuntu.yml: Ansible Playbook that sets up development environment for [SPADE][1].
- setup/ubuntu.sh: Automates the install process by invoking Ansible. This scripts also builds all required tools and softwares.
- setup/localhost: Required for Ansible.
- setup/buildscripts/*: Scripts for building up dtracker, SPADE and coreutils (including instrumented version).

- testgen: Scripts related to test generation.
- testgen/config.py: Config file for parameterizing test generation.
- testgen/mktests.py: Script that generates test scripts.
- testgen/mkstats.py: Script to generate stats (a CSV file) from the test.

### Prereqs:

- Install Ansible:
```
sudo add-apt-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible git
```

### Machine setup
- Let Ansible install and setup the machine:
```
source <(curl -s https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/setup/ubuntu.sh)
```
(for debug commands, read top of ubuntu.yml)

### Test generaion
- Configure a test:
Edit testgen/config.py to tailor the test accordingly. 
- Generate a test:
Execute testgen/mktests.py to create a test directory.
- Start SPADE
SPADE will be at provenance-stats/staging/SPADE. You can cd there and run ./bin/spade debug|start to start SPADE.
- Run a test:
Exectute <test>/run_all.sh to run all tests. You can also run tests for indiviual reporters by running <test>/<reporter>/run_all_<reporter>.sh. You can furthermore run test for invdivisual utility by executing <test>/<reporter>/<util>/run_util.sh

### Stats generation:      

  [1]: https://github.com/ashish-gehani/SPADE

  

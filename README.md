### Provenance Stats

This framework contains codebase that helps compare different provenance auditing methods. More specifically, this repository is collection of system setup, test generation and test stats generation scripts for instrumentation tradeoff and comparison work at SRI International. 

This framework uses [SPADE] [1] as provenance auditing collection tool. The comparision matrix includes both compile time and runtime instumentation. For compile time insturmenation, we are using LLVM based code injecting tool that is shipped as part of SPADE. For run time instumentation, we use two types of two methods: syscall level provenance tracking using Strace (shipped along with SPADE) and tracking of data during runtime using dtracker tool. These tests are performed on GNU coreutils.

This reporsitoy performs these three tasks:
- Prepares the system for running tests. It uses Ansible [http://docs.ansible.com/] to automate the process of installing all required packages and their dependencies. It also downloads and buils SPADE, dtracker and other tools.
- Test generation scripts that generates more scripts that are used to run a specific test. A config file for test generation is also provided.
- Stats collection scripts that checks the log files created when running the tests and generates a stats file.

This has been tested on Ubuntu 14.04 LTS 32 bit only.

Layout of this repository is as follows:

- `setup`: Scripts related to setting up the system to run tests.
- `setup/ubuntu.yml`: Ansible Playbook that sets up development environment for [SPADE][1].
- `setup/ubuntu.sh`: Automates the install process by invoking Ansible. This scripts also builds all required tools and softwares.
- `setup/localhost`: Required for Ansible.
- `setup/buildscripts/*`: Scripts for building up dtracker, SPADE and coreutils (including instrumented version).
- `testgen`: Scripts related to test generation.
- `testgen/config.py`: Config file for parameterizing test generation.
- `testgen/mktests.py`: Script that generates test scripts.
- `testgen/mkstats.py`: Script to generate stats (a CSV file) from the test.

### 0. Prereqs:

Only ansible and git are required. You can install these in Ubuntu by executing these commands:

```
sudo add-apt-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible git
```

### 1. Machine setup
- Setup the machine using this command:
```
source <(curl -s https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/setup/ubuntu.sh)
```
This installs all required packages using apt-get and/or directly from the provider. It will also download and build all provenance auditing tools used. This step will take considerale time.
(for debug commands, read top of ubuntu.yml)

### 2. Test generaion
- 2.1 Configure a test:
Edit `testgen/config.py` to tailor the test accordingly. This file is well documented and each varible is explained.
- 2.2 Generate a test:
Execute `testgen/mktests.py` to create a test directory.
- 2.3 Start SPADE
SPADE will be at `provenance-stats/staging/SPADE`. Run `./bin/spade start|debug` to start SPADE.
- 2.4 Run a test:
Exectute `<test>/run_all.sh` to run all tests. You can also run tests for individual reporters by running `<test>/<reporter>/run_all_<reporter>.sh`. You can furthermore run test for individual utility by executing `<test>/<reporter>/<util>/run_util.sh`.

### 3.0 Stats generation:      

- Run `testgen/mkstats.py`to generate a CSV file of test stats. By default CSV file location is `<test>/stats.csv`.

  [1]: https://github.com/ashish-gehani/SPADE

  

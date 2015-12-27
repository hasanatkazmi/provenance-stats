### Provenance Stats

This framework contains codebase that helps compare different provenance auditing methods. More specifically, this repository is collection of system setup, test generation and test stats generation scripts for instrumentation tradeoff and comparison work at SRI International.

This framework uses SPADE as provenance auditing collection tool. The comparison matrix includes both compile time and runtime instrumentation. For compile time instrumentation, we are using LLVM based code injecting tool that is shipped as part of SPADE. For run time instrumentation, we use two types of two methods: syscall level provenance tracking using Strace (shipped along with SPADE) and tracking of data during runtime using dtracker tool. These tests are performed on GNU coreutils.

This repository performs these three tasks:
- Prepares the system for running tests. It uses Ansible [http://docs.ansible.com/] to automate the process of installing all required packages and their dependencies. It also downloads and builds SPADE, dtracker and other tools.
- Test generation scripts generate more scripts that are used to run a specific test. A config file for test generation is also provided.
- Stats collection scripts that checks the log files created when running the tests and generates a stats file.

This has been tested on Ubuntu 14.04 LTS 32 bit only with LLVM version 3.6 and GNU coreutils 8.24.

Layout of this repository is as follows:

- `setup`: Scripts related to setting up the system to run tests.
- `setup/ubuntu.yml`: Ansible Playbook that sets up development environment for [SPADE][1].
- `setup/ubuntu.sh`: Automates the install process by invoking Ansible. This script also builds all required tools and softwares.
- `setup/localhost`: Required for Ansible.
- `setup/buildscripts/*`: Scripts for building up dtracker, SPADE and coreutils (including instrumented version).
- `testgen`: Scripts related to test generation.
- `testgen/config.py`: Config file for parameterizing test generation.
- `testgen/mktests.py`: Script that generates test scripts.
- `testgen/mkstats.py`: Script to generate stats (a CSV file) from the test.

### 1. Install Prerequisites

Only ansible and git are required. You can install these in Ubuntu by executing these commands:

```
sudo add-apt-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible git
```

### 2. Setup Machine

Setup the machine using this command:
```
source <(curl -s https://raw.githubusercontent.com/hasanatkazmi/provenance-stats/master/setup/ubuntu.sh)
```
This installs all required packages using apt-get and/or directly from the provider. It will also download and build all provenance-auditing tools used. This step will take considerable time. 
(for debug commands, read top of ubuntu.yml)

For Strace reporter to report correctly, Edit and set `/proc/sys/kernel/yama/ptrace_scope` to `0`.

### 3. Configure a test

Edit `testgen/config.py` to tailor the test accordingly. This file is well documented and each variable is explained.

### 4. Generate a test

Execute `testgen/mktests.py` to create a test directory. Default test directory is test and will be located at root of the repository.

### 5. Start SPADE

SPADE will be at `provenance-stats/staging/SPADE`. Run `./bin/spade start|debug` to start SPADE.

### 6. Run a Test

Exectute `<test>/run_all.sh` to run all tests. You can also run tests for individual reporters by running `<test>/<reporter>/run_all_<reporter>.sh`. You can furthermore run test for individual utility by executing `<test>/<reporter>/<util>/run_util.sh`.

### 7. Stats generation     

Run `testgen/mkstats.py`to generate a CSV file of test stats. By default CSV file location is `<test>/stats.csv`. Each column in the CSV file has is explained here:
- `reporter`: Type of instrumentation that was performed.
- `util`: Specific Coreutil utility that was used in the test.
- `time_avg`: Average time taken of multiple runs of the utility. Unit of time is seconds.
- `time_stddev`: Standard deviation for time in multiple test runs. Unit is seconds.
- `vertices_avg`: Average vertices count for the provenance graph
- `edges_avg`: Average edge count for the provenance graph.

  [1]: https://github.com/ashish-gehani/SPADE

  

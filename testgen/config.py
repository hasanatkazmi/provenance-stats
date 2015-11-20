#!/usr/bin/python

import os, sys, shutil, stat
from textwrap import dedent
from os.path import expanduser
from os.path import join as pj

###############################################################################
### Configuration
###############################################################################
### Runtime options
reporters = ["none", "llvm", "strace", "dtracker"]  # all reporters that we want to test out
runs = 5                                            # number of runs for each util
inputsize = 1024
bash_header = '#!/bin/bash'                         # header to use when writing bash scripts
timeformat_base = '%3R;%3U;%3S;%P'

### Paths and directories
topdir          = pj(expanduser("~"), 'provenance-stats')         # top directory
testdir         = pj(topdir, 'test')                    # test directory - we should not write stuff out of this dir
# inputdir        = pj(topdir, 'testgen', 'input')                   # input dir - copy your input files here
input1_base = "input-"+ str(inputsize)+".txt"                         # input file used to run utils
inputdir = testdir
plotdir		= '/usr/share/nginx/www'		# where to store the plots
bindirs         =  {
    'none':     pj(topdir, 'bins', 'uninstrumented', 'coreutils-8.24', 'src'),            # dir containing the tested binaries
    'strace':   pj(topdir, 'bins', 'uninstrumented', 'coreutils-8.24', 'src'),            # dir containing the tested binaries used by strace reporter
    'llvm':     pj(topdir, 'bins', 'instrumented', 'coreutils-8.24', 'src'),       # dir containing the tested binaries used by llvm reporter
    'dtracker': pj(topdir, 'bins', 'uninstrumented', 'coreutils-8.24', 'src'),            # dir containing the tested binaries used by dtracker reporter
}
spade_controller    = pj(topdir, 'staging', 'SPADE', 'bin', 'spade-controller.sh')     # path to SPADE controller script
spade_dslpipe       = pj(topdir, 'staging', 'SPADE', 'spade_pipe')                     # path to SPADE DSL pipe
dtracker_home       = pj(topdir, 'staging', 'dtracker')                                # location of DataTracker directory
pin_home            = pj(dtracker_home, 'pin')                              # location of the Intel Pin directory


### Formats for producing scripts
utils = {
    'cat'       : ('{input1}',),
    'cp'        : ('{input1} {output1}',),
    'dd'        : ('if={input1} of={output1} bs=2048 conv=noerror,sync',),
    'base64'    : ('{input1}',),
    'cksum'     : ('{input1}',),
    'comm'      : ('{input1} {input1}',),
    'csplit'    : ('{input1} 2 4 6',),
    'cut'       : ('-c2 {input1}',),
    'expand'    : ('{input1}',),
    'fmt'       : ('-w 1 {input1}',),
    'fold'      : ('-w5 {input1}',),
    'head'      : ('-n 2 {input1}',),
    'join'      : ('{input1} {input1}',),
    'md5sum'    : ('{input1}',),
    'nl'        : ('{input1}',),
    'od'        : ('-Ax -c {input1} ',),
    'paste'     : ('-s {input1}',),
    'pr'        : ('-n {input1}',),
    'ptx'       : ('{input1}',),
    'sha1sum'   : ('{input1}',),
    'sha224sum' : ('{input1}',),
    'sha256sum' : ('{input1}',),
    'sha384sum' : ('{input1}',),
    'sha512sum' : ('{input1}',),
    'shuf'      : ('{input1}',),
    'sort'      : ('{input1}',),
    'split'     : ('-l 10 {input1} {output1}',),
    'sum'       : ('{input1}',),
    'tac'       : ('{input1}',),
    'tail'      : ('{input1}',),
    'tee'       : ('{output1} < {input1}',),
    'tr'        : ('[:lower:] [:upper:] < {input1}',),
    'truncate'  : ('-s 1024 {local_input1}',),
    'tsort'     : ('{input1}',),
    'unexpand'  : ('{input1}',),
    'uniq'      : ('{input1}',),
    'wc'        : ('{input1}',),
}
formats = {
    'spade_adddb' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "add storage Graphviz {graphvizdb}\\r"
        expect "Adding storage Graphviz... done\\r"
    ''',
    'spade_rmdb' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "remove storage Graphviz\\r"
        expect "Shutting down storage Graphviz*"
    ''',
    'spade_addstracereporter' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "add reporter Strace {command_line}\\r"
        expect "Adding reporter Strace... done\\r"
    ''',
    'spade_rmstracereporter' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "remove reporter Strace\\r"
        expect "Shutting down reporter Strace... done*"
    ''',
    'spade_adddsl' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "add reporter DSL {spade_dslpipe}\\r"
        expect "Adding reporter DSL... done\\r"
    ''',
    'spade_rmdsl' : '''
        #!/usr/bin/expect -f
        spawn "{spade_controller}"
        expect "shutdown"
        send "remove reporter DSL\\r"
        expect "Shutting down reporter DSL... done\\r"
    ''',
    'none_runbin.sh': '''
        #!/bin/bash
        export TIMEFORMAT='{timeformat}'

        function do_run() {{
            seq 100 | xargs -Iz {command_line}
        }}

        echo 'Running: {command_line}'
	{{ time do_run 1>{logfile} 2>{elogfile}; }} 2> {tlogfile}
    ''',
    'strace_runbin.sh': '''
        #!/bin/bash
        export TIMEFORMAT='{timeformat}'

        function do_run() {{
            {command_line}
        }}

        echo 'Running: {command_line}'
	{{ time do_run 1>{logfile} 2>{elogfile}; }} 2> {tlogfile}
    ''', # strace_runbin.sh is not currently used!
    'llvm_runbin.sh': '''
        #!/bin/bash
        export TIMEFORMAT='{timeformat}'

        function do_run() {{
            #seq 100 | xargs -Iz {command_line}
            {command_line}
        }}

        echo 'Running: {command_line}'
	{{ time do_run 1>{logfile} 2>{elogfile}; }} 2> {tlogfile}
    ''',
    'dtracker_runbin.sh': '''
        #!/bin/bash
        export TIMEFORMAT='{timeformat}'
        export PIN_HOME={pin_home}

        function do_run() {{
            {pin_home}/pin.sh -follow_execv -t {dtracker_home}/obj-ia32/dtracker.so -o {dtracker_home}/rawprov.out -- {command_line}
        }}

	[ -e {spade_dslpipe} ] && rm -f {spade_dslpipe}
	{spade_dbattach}
        {spade_reporter_add}
        echo 'Running: {command_line}'
	{{ time do_run 1>{logfile} 2>{elogfile}; }} 2> {tlogfile}
        {dtracker_home}/raw2dsl.py < {dtracker_home}/rawprov.out > {spade_dslpipe}
        {spade_reporter_rm}
	{spade_dbremove}
    ''',
}

# fix script formats indentation
formats = { k: dedent(v).strip() for k, v in formats.items() }

# fix utils formats
utils_tmp = {}
for k, v in utils.items():
	util_fmt, misc = v[0], v[1:]
	util_fmt = '{util} ' + dedent(util_fmt).strip()
	utils_tmp[k] = (util_fmt,) + misc
utils = utils_tmp
del utils_tmp

# set input1
input1 = pj(inputdir, input1_base)


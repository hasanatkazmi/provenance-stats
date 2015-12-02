#!/usr/bin/python

import os, sys, shutil, stat
from textwrap import dedent
from os.path import join as pj
import collections
from textwrap import wrap

from config import *

###############################################################################
### Utility functions
###############################################################################
def writeScript(filename, fmt, data, open_mode='w', header=None):
    contents = fmt.format(**data)
    exists = os.path.exists(filename)
    with open(filename , open_mode) as f:
        if (header and not exists):
            # write header if file was just created
            f.write(header + '\n')
        f.write(contents + '\n')
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC )


### Generate Input file (Must be in bytes)
def genInput(size):
    global input1
    seed = "1092384956781341341234656953214543219"
    wrap_length = 70
    words = open("lorem.txt", "r").read().replace("\n", '').split()

    def fdata():
        a = collections.deque(words)
        b = collections.deque(seed)
        while True:
            yield ' '.join(list(a)[0:1024])
            a.rotate(int(b[0]))
            b.rotate(1)

    if not os.path.exists(inputdir):
        os.makedirs(inputdir)
    g = fdata()
    with open(input1, 'w') as f:
        while os.path.getsize(input1) < size:
            par = '\n'.join(wrap(g.next(), wrap_length))
            f.write(par)
        f.write('\n\n')
        f.truncate(size)



###############################################################################
### Execution
###############################################################################
# cleanup old stuff
if os.path.exists(testdir):
    shutil.rmtree(testdir)

genInput(inputsize)

# start generating scripts
for reporter in reporters:
    for util, util_specs in sorted(utils.items()):
	util_fmt, util_misc = util_specs[0], util_specs[1:]
        for i in range(1, runs+1):
            out_file_fmt = pj(testdir, reporter, util, '%02d' % (i), '%s')
            _ = lambda f: out_file_fmt % (f)

            # logfiles for unit of testing
            the_runbin = _(reporter+"_runbin.sh")
            the_logfile = _( '%s_%s_out.log' % (reporter, util) )
            the_elogfile = _( '%s_%s_err.log' % (reporter, util) )
            the_tlogfile = _( '%s_%s_time.log' % (reporter, util) )
            the_timeformat = '%s;%s;%s' % (reporter, util, timeformat_base)
            the_bindir = bindirs[reporter]

            # create directories and copy inputs
            os.makedirs(_(''))

            # copy input file if local input is required
            if '{local_input1}' in util_fmt:
                shutil.copyfile(input1, _(input1_base))

            # Initialize database for all reporters.
            if reporter != "none":
                # Create new database script.
                writeScript(filename = _("spade_dbattach.sh"),
                    fmt = formats['spade_adddb'],
                    data = { 'spade_controller': spade_controller, 'graphvizdb': _("graph.dot"), }
                )

                # Remove database script.
                writeScript(filename = _("spade_dbremove.sh"),
                    fmt = formats['spade_rmdb'],
                    data = { 'spade_controller': spade_controller, }
                )

                # Dot to PNG script.
                writeScript(filename = _("genpng.sh"),
                    fmt = "dot -Tpng '{input}' > '{output}'\n",
                    data = { 'input': _("graph.dot"), 'output': _("graph.png"), }
                )

            # Utility runner scripts for none.
            # The command is launched from the runbin script.
            if reporter == "none":

                command_line = util_fmt.format(
                    util = pj(the_bindir, util),
                    input1 =  input1,
                    local_input1 =  _(input1_base),
                    output1 = _("output1.txt" )
                )
                writeScript(filename = the_runbin,
                    fmt = formats['none_runbin.sh'],
                    data = {
                        'command_line': command_line,
                        'timeformat': the_timeformat,
                        'input1':  input1,
                        'local_input1':  _(input1_base),
                        'logfile': the_logfile,
                        'elogfile': the_elogfile,
                        'tlogfile': the_tlogfile,
                    }
                )

            # Utility runner scripts for strace.
            # The command is launched from within SPADE controller.
            # XXX: ???Timing???
            if reporter == "strace":
                command_line = util_fmt.format(
                    util = pj(the_bindir, util),
                    input1 =  input1,
                    local_input1 =  _(input1_base),
                    output1 = _("output1.txt" )
                )
                command_line = "cmd='" + command_line + "'"
                writeScript(filename = _("reporter_attach.sh"),
                    fmt = formats['spade_addreporter'],
                    data = {
                        'command_line' : command_line,
                        'timeformat': the_timeformat,
                        'logfile': the_logfile,
                        'elogfile': the_elogfile,
                        'tlogfile': the_tlogfile,
                        'spade_controller': spade_controller,
                        'reporter': 'Strace',
                    }
                )
                writeScript(filename = _("reporter_remove.sh"),
                    fmt = formats['spade_rmreporter'],
                    data = { 
                        'spade_controller': spade_controller,
                        'reporter': 'Strace',
                    }
                )

            # Utility runner scripts for llvm.
            # The command is launched from the runbin script.
            if reporter == "llvm":
                command_line = util_fmt.format(
                    util = pj(the_bindir, util),
                    input1 =  input1,
                    local_input1 =  _(input1_base),
                    output1 = _("output1.txt" )
                )
                writeScript(filename = the_runbin,
                    fmt = formats['llvm_runbin.sh'],
                    data = {
                        'command_line': command_line,
                        'timeformat': the_timeformat,
                        'input1':  input1,
                        'local_input1':  _(input1_base),
                        'logfile': the_logfile,
                        'elogfile': the_elogfile,
                        'tlogfile': the_tlogfile,
                        'bindir' : the_bindir,
                    }
                )
                # writeScript(filename = _("reporter_attach.sh"),
                #     fmt = formats['spade_addreporter'],
                #     data = {
                #         'command_line' : command_line,
                #         'timeformat': the_timeformat,
                #         'logfile': the_logfile,
                #         'elogfile': the_elogfile,
                #         'tlogfile': the_tlogfile,
                #         'spade_controller': spade_controller,
                #         'reporter': 'LLVM',
                #     }
                # )
                # writeScript(filename = _("reporter_remove.sh"),
                #     fmt = formats['spade_rmreporter'],
                #     data = { 
                #         'spade_controller': spade_controller,
                #         'reporter': 'LLVM',
                #     }
                # )

            # Reporter initialization/runner script for dtracker.
            # The command is launched from the runbin script.
            if reporter == "dtracker":
                # the attach/detach scripts can be added only once if we want
                writeScript(filename = _("spade_adddsl.sh"),
                    fmt = formats['spade_adddsl'],
                    data = { 'spade_controller': spade_controller, 'spade_dslpipe': spade_dslpipe, }
                )
                writeScript(filename = _("spade_rmdsl.sh"),
                    fmt = formats['spade_rmdsl'],
                    data = { 'spade_controller': spade_controller, }
                )

                command_line = util_fmt.format (
                    util = pj(the_bindir, util),
                    input1 =  input1,
                    local_input1 =  _(input1_base),
                    output1 = _("output1.txt" )
                )
                writeScript(filename = the_runbin,
                    fmt = formats['dtracker_runbin.sh'],
                    data = {
                        'command_line': command_line,
                        'timeformat': the_timeformat,
                        'input1':  input1,
                        'local_input1':  _(input1_base),
                        'logfile': the_logfile,
                        'elogfile': the_elogfile,
                        'tlogfile': the_tlogfile,
                        'spade_dbattach' : _("spade_dbattach.sh"),
                        'spade_dbremove' : _("spade_dbremove.sh"),
                        'spade_reporter_add' : _("spade_adddsl.sh"),
                        'spade_reporter_rm' : _("spade_rmdsl.sh"),
                        'pin_home' : pin_home,
                        'dtracker_home': dtracker_home,
                        'spade_dslpipe': spade_dslpipe,
                    }
                )

# write the high level runners
top_runner = pj(testdir, "run_all.sh")
for reporter in reporters:
    reporter_runner = pj(testdir, reporter, "run_all_%s.sh" % (reporter))

    # append line to the top-level runner
    writeScript( filename = top_runner,
        fmt = '{command_line}',
        data = { 'command_line': reporter_runner, },
        open_mode = 'a',
        header = bash_header,
    )

    # write to the reporter runner
    for util in sorted(utils):
        util_runner = pj(testdir, reporter, util, "run_util.sh")

        # append line to the reporter runner
        writeScript( filename = reporter_runner,
            fmt = '{command_line}',
            data = { 'command_line': util_runner, },
            open_mode = 'a',
            header = bash_header,
        )

        # write to the util runner
        for i in range(1, runs+1):
            out_file_fmt = pj(testdir, reporter, util, '%02d' % (i), '%s')
            _ = lambda f: out_file_fmt % (f)

            the_runbin = _(reporter+"_runbin.sh")

            if reporter == "none":
                writeScript( filename = util_runner,
                    fmt = '{command_line}',
                    data = { 'command_line': the_runbin, },
                    open_mode = 'a',
                    header = bash_header,
                )
            if reporter == "strace":
                writeScript(filename = util_runner,
                    fmt = dedent('''
                        {spade_dbattach}
                        {reporter_attach}
                        {reporter_remove}
                        {spade_dbremove}
                        {genpng}
                        '''),
                    data = {
                        'spade_dbattach' : _("spade_dbattach.sh"),
                        'reporter_attach': _("reporter_attach.sh"),
                        'reporter_remove': _("reporter_remove.sh"),
                        'spade_dbremove' : _("spade_dbremove.sh"),
                        'genpng' : _("genpng.sh")
                    },
                    open_mode = 'a',
                    header = bash_header,
                )
            if reporter == "llvm":
                writeScript( filename = util_runner,
                    fmt = dedent('''
                        {spade_dbattach}
                        {command_line}
                        sleep {sleep_time} 
                        {spade_dbremove}
                        {genpng}
                    '''),
                    data = {
                        'spade_dbattach': _("spade_dbattach.sh"),
                        'command_line': the_runbin,
                        'sleep_time': sleep_time,
                        'spade_dbremove': _("spade_dbremove.sh"),
                        'genpng': _("genpng.sh")
                    },
                    open_mode = 'a',
                    header = bash_header,
                )
            if reporter == "dtracker":
                writeScript( filename = util_runner,
                    fmt = dedent('''
                        {spade_dbattach}
                        {command_line}
                        {spade_dbremove}
                        {genpng}
                    '''),
                    data = {
                        'spade_dbattach': _("spade_dbattach.sh"),
                        'command_line': the_runbin,
                        'spade_dbremove': _("spade_dbremove.sh"),
                        'genpng': _("genpng.sh")
                    },
                    open_mode = 'a',
                    header = bash_header,
                )


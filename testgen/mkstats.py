#!/usr/bin/python
####
# Generates CSV file.
####

import matplotlib
matplotlib.use('Agg')

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import glob
from config import *
import subprocess
import csv

db = {
    #(reporter, util) = {
    #    time, vertices, edges, # lists
    #}
}

# excluded_utils = ['ptx', 'od']
excluded_utils = []

def process_time_log(timelog, reporter=None):
    time_labels = ['t', 't_usr', 't_sys', 'cpu']
    with open(timelog, 'r') as f:
        for l in (l.strip() for l in f):
            if not l or l.startswith('#'): continue
            reporter, util, t, t_usr, t_sys, cpu = l.split(';')
            return float(t)


def process_dot_log(dotlog):
    # reads the dot file using gc program to find edges and vertices

    process = subprocess.Popen("gc " + dotlog, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode != 0:
        return None

    for line in process.stdout:
        v,e = [i for i in line.split(" ") if i != ""][:2]
        return (int(v),int(e))


def insert_in_db(reporter, util, time, vertices=None, edges=None):
    global db
    
    # init db
    if not (reporter, util) in db:
        db[(reporter, util)] = {
            "time":[],"vertices":[],"edges":[],
        }

    # add an item
    db[(reporter,util)]["time"].append(time)
    db[(reporter,util)]["vertices"].append(vertices)
    db[(reporter,util)]["edges"].append(edges)

def genstats():
    # returns a list of dictionaries whereas each dictionary contains averages
    global db
    averages = [ 
        # {
            # "reporter": "",
            # "util": "",
            # "time_stddev": "",
            # "time_avg": "",
            # "vertices_avg": "",
            # "edges_avg": "",
        # }, 
    ] # lists of averages

    for (reporter, util), value in db.iteritems():
        averages.append(
            {
            "reporter": reporter,
            "util": util,
            "time_stddev" : np.std(value["time"], dtype=np.float64),
            "time_avg" : np.average(value["time"]),
            "vertices_avg" : np.average(value["vertices"]) if reporter!="none" else 0,
            "edges_avg" : np.average(value["edges"] if reporter!="none" else 0)
        })

    return averages

def writecsv(averages):

    out = csv.DictWriter(open(os.path.join(testdir, "stats.csv"),"w") , delimiter=',',quoting=csv.QUOTE_ALL, fieldnames=["reporter","util","time_stddev","time_avg","vertices_avg","edges_avg"])
    out.writeheader()
    for i in averages: 
        out.writerow(i)



for reporter in reporters:
    for util in sorted(utils):
        if util in excluded_utils: continue;

        # Read time log files for this reporter/util pair.
        glob_pattern_time = '%s/%s/%s/*/*_time.log' % (testdir, reporter, util)
        glob_pattern_dot = '%s/%s/%s/*/graph.dot' % (testdir, reporter, util)

        if reporter == "none":
            for timelogfile in glob.iglob(glob_pattern_time):
                t = process_time_log(timelogfile)

                if t == None:
                    print "time log failure:", timelogfile
                    continue

                insert_in_db(reporter, util, t)


        for timelogfile, dotlogfile in zip(glob.iglob(glob_pattern_time) , glob.iglob(glob_pattern_dot)):
            t = process_time_log(timelogfile, reporter=reporter)
            dot = process_dot_log(dotlogfile)

            if t == None:
                print "time log failure:", timelogfile
                continue
            if dot == None:
                print "dot log failure:", dotlogfile
                continue

            v,e = dot

            insert_in_db(reporter, util, t,v,e)


writecsv(genstats())


#!/usr/bin/env python3
""" This script initializes a new BIDS App Gear using the bids-app-template
    and sets up testing configurations.  It can be run multiple times to
    set up additional tests.
"""

import os
import json
import datetime
import subprocess as sp
import sys
import argparse
import logging
import tempfile
import shutil
import filecmp

# This figures out where things are and reads teh gear's manifest:
from utils.find_gear import *
from utils.get_user_input import *
from utils.datalad import *


if __name__ == '__main__':

    LOG.info('STATUS is '+STATUS)

    msg = 'Starting setup...'
    print(msg)
    LOG.info(msg)

    if STATUS == 'no-gear':
        msg = 'The gear\n  ' + GEAR + '\n'\
              ' does not exist.  Use GitHub to create it first.\nI quit.'
        print(msg)
        LOG.info(msg)
        sys.exit(-1)

    msg = 'GEAR is\n  '+GEAR
    print(msg)
    LOG.info(msg)

    # if the gear has not already been set up, clone the testing template
    # repository and copy files into the gear while supstituting the
    # real gears name. 
    if STATUS == 'no-manifest':

        msg = 'Cloning bids-app-template'
        print(msg)
        LOG.info(msg)

        with tempfile.TemporaryDirectory() as tmpdir:
            
            cmd = 'git clone git@github.com:flywheel-apps/bids-app-template.git '+\
                  tmpdir
            result = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

            # Copy files into the new gear, supstituting the proper name
            for ff in ['Dockerfile','manifest.json','run.py']:
                msg = 'Copying '+ff
                print(msg)
                LOG.info(msg)
                #result = sp.run('ls '+tmpdir, shell=True)
                o = open(GEAR + '/' + ff, "w") 
                for line in open(tmpdir+'/'+ff):
                    line = line.replace('bids-app-template',NAME)
                    if 'COPY test.sh' in line: # don't copy test.sh in Dockerfile
                        if TESTING == 'basic': # unless this is a test
                            o.write(line)
                            o.write('RUN chmod a+x ${FLYWHEEL}/test.sh') 
                    elif "['command'] = ['echo']" in line:
                        if TESTING == 'basic': # if this is a test
                            # have run.py run the test instead of echo
                            o.write("        context.gear_dict['command'] = ['./test.sh']")
                        else:
                            o.write(line)
                    else:
                        o.write(line) 
                o.close()

            msg = 'Copying '+'utils/'
            print(msg)
            LOG.info(msg)
            shutil.copytree(tmpdir + '/utils', GEAR + '/utils')

            if TESTING == 'basic': # also copy in the test executable
                shutil.copyfile(tmpdir + '/test.sh' , GEAR + '/test.sh')

    msg="""\nNow you can set up a new test in one of the following ways:

    1) Initialize a test and create config.json by providing a Flywheel api
       key, destination id and type.  BIDS data will be downloaded from the
       specified session the first time the gear is run.
     
    2) Copy an existing test (using hard links so it won't take up much
       extra space)
    
    3) Download test data and config files from a Flywheel instance
    
    4) Download test data using DataLad (https://www.datalad.org/)

    5) Skip this for now (default).  You can run setup.py any time to add
       another test.
    """
    ans = get_user_input(msg,"Which would you like to do?",['','1','2','3','4','5'])
    # print()

    if ans == '1': # init
        test_name = init_test_directory()
        init_test_subdirs(test_name)
        init_test_config(test_name)

    elif ans == '2': # Copy an existing test
        init_by_copying()

    elif ans == '3': # Download from Flywheel
        print("Downloading from Flywheel...\n")
        print("Aw shucks, this ain't been implemented yet.")
        print('But there is always:')
        print('  fwutil_job_run_local.py')

    elif ans == '4': # Use DataLad
        init_using_datalad()

    # else ans == '5' or '' so drop on out

    msg="""
    What's next?  Edit Dockerfile, manifest.json, run.py and search for 
    'editme'.  The comments will describe the various optional and required
    features for a BIDS App.

    Use setup.py again to create more tests, and build.py and run.py in this 
    test repository to develop your code.
    """
    print(msg)

    LOG.info('Finished.\n')

    return_code = 0

    if TESTING == 'basic':
        LOG.info('Now check the results of setup.py')
        for ff in ['Dockerfile', 'manifest.json', 'run.py', 'test.sh']:
            if os.path.exists(GEAR + '/' + ff):
                if filecmp.cmp(GEAR + '/' + ff, GEAR + '/../test_files/' + ff, 
                               shallow=True):
                    LOG.info('  '+ff+' is same')
                else:
                    LOG.info('  '+ff+' is DIFFERENT')
                    return_code = -1
        LOG.info('Done with '+TESTING+' test.\n')

    sys.exit(return_code)


# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

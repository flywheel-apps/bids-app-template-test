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

# This figures out where things are and reads teh gear's manifest:
from utils.find_gear import *

def setup():

    log.info('STATUS is '+STATUS)

    LOG.info('Starting...')

    # if the gear has not already been set up, clone the testing template
    # repository and copy files into the gear while supstituting the
    # real gears name. 
    if STATUS == 'no-manifest':

        LOG.info('Cloning bids-app-template')

        with tempfile.TemporaryDirectory() as tmpdir:
            
            cmd = 'git clone git@github.com:flywheel-apps/bids-app-template.git '+\
                  tmpdir
            result = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

            for ff in ['Dockerfile','manifest.json','run.py']:
                LOG.info('Copying '+ff)
                #result = sp.run('ls '+tmpdir, shell=True)
                o = open(GEAR+'/'+ff,"w") 
                for line in open(tmpdir+'/'+ff):
                    if 'COPY test.sh' not in line:
                        line = line.replace("bids-app-template",NAME)
                        o.write(line) 
                o.close()

            LOG.info('Copying '+'utils/')
            shutil.copytree(tmpdir+'/utils', GEAR+'/utils')

    # Don't copy the test.sh file in the Dockerfile

    # Set up a new test in one of three different ways.

    # Copy an existing test (using hard links so it won't take up much
    # space)

    # Download test datw and config files from a Flywheel instance

    # Download test data using DataLad

    # What's next?  Edit the Docerfile/manifest.json/run.py and search for 
    # "editme" (and delete "editme" so you won't see this message any more).

    LOG.info('Finished.\n\n')

if __name__ == '__main__':
    setup()

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

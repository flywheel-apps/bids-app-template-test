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

from utils.find_gear import *


# log actions of this script (which can be run multiplte times) to
# the default test log dir with spacial name: 'init_log.txt'
log_name = TEST+'tests/template/logs/init_log.txt'
fmt = '%(levelname)s - %(name)-8s - %(asctime)s -  %(message)s'
logging.basicConfig(format = fmt,
                    filename = log_name,
                    level = logging.DEBUG)

my_name = os.path.basename(__file__)

logging.info(my_name+' starting...')

# if the gear has not already been set up, clone the testing template
# repository and copy files into the gear while supstituting the
# real gears name. 

# Don't copy the test.sh file in the Dockerfile

# Set up a new test in one of three different ways.

# Copy an existing test (using hard links so it won't take up much
# space)

# Download test datw and config files from a Flywheel instance

# Download test data using DataLad

# What's next?  Edit the Docerfile/manifest.json/run.py and search for 
# "editme" (and delete "editme" so you won't see this message any more).

logging.info(my_name+' finished.\n\n')

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

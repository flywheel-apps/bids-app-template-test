""" 
Using the location of this here file, find the path to the gear itself 
assuming this test directory name is the gear name + "-test".

Then:
    Set global variaibles (in ALLCAPPS)
    Change into the gear directory
    Open the manifest.json as MANIFEST
    Make sure the gear name matches and return STATUS
"""

import os
import json
import logging
import sys
import shutil


verbose = True

path_to_me = os.path.dirname(os.path.realpath(__file__))
if verbose:
    print('path_to_me='+path_to_me)

penultimate_dir = path_to_me.split('/')[-2]
if verbose:
    print(f'penultimate_dir={penultimate_dir}')

penultimate_dir_split = penultimate_dir.split('-')
if verbose:
    print(f'penultimate_dir_split={penultimate_dir_split}')

if len(penultimate_dir_split) > 1:
    if penultimate_dir_split[-1] == 'test':
        gear_name = '-'.join(penultimate_dir_split[:-1])
        if verbose:
            print(f'Found {gear_name}')
else:
    raise Exception('ERROR: cannot find gear from test dir path.')

FLY0 = '/flywheel/v0/'
NAME = gear_name
BASE = '/'.join(path_to_me.split('/')[:-2])+'/'
GEAR = BASE+NAME  # note: no ending /
TEST = BASE+NAME+'-test/'

# log actions of this script (which can be run multiplte times) to
# the default test log dir with spacial name: 'init_log.txt'
log_name = TEST+'tests/test/logs/init_log.txt'
if verbose:
    print('log name is "'+log_name+'"')

fmt = '%(levelname)s - %(name)-8s - %(asctime)s -  %(message)s'
logging.basicConfig(format = fmt,
                    filename = log_name,
                    level = logging.DEBUG)

cmd_name = os.path.basename(sys.argv[0])
LOG = logging.getLogger(cmd_name)

msg = 'Finding gear...'
print(msg)
LOG.info(msg)

TESTING = ''
if NAME == 'bids-app-template': # then test the template inside 'gear'

    TESTING = 'basic'

    if cmd_name == 'setup.py':

        old_gear = GEAR
        GEAR = TEST+'tests/test/gear'
        msg = '\nTesting: GEAR changed from "'+old_gear+'" to "'+GEAR+'"\n'
        print(msg)
        LOG.info(msg)

        # remove existing fiiles so they can be re-created:
        for ff in ['Dockerfile', 'manifest.json', 'run.py', 'test.sh']:
            if os.path.exists(GEAR + '/' + ff):
                os.remove(GEAR + '/' + ff)
        if os.path.exists(GEAR + '/utils'):
            shutil.rmtree(GEAR + '/utils')

if verbose:
    print(f'NAME="{NAME}"')
    print(f'BASE="{BASE}"')
    print(f'GEAR="{GEAR}"')
    print(f'TEST="{TEST}"')

# Make sure the gear directory exists
STATUS = 'OK'
if os.path.isdir(GEAR):

    os.chdir(GEAR)

    if os.path.exists('manifest.json'):

        with open('manifest.json', 'r') as f:
            MANIFEST = json.load(f)

        if gear_name != MANIFEST["name"]:
            print('Gear name in manifest, "'+MANIFEST["name"]+'" '+\
                  'does not match gear name found in path, "'+gear_name+'"')
            print('Exiting early')
            sys.exit()
        else:
            msg = 'Gear name in manifest matches gear name found in path'
            print(msg)
            LOG.info(msg+'\n')

    else:
        msg = 'Note: manifest.json does not exist in '+GEAR
        LOG.info(msg+'\n')
        STATUS = 'no-manifest'

else:
    msg = 'ERROR: Path does not exist:\n'
    msg += '  '+GEAR
    LOG.error(msg+'\n')
    STATUS = 'no-gear'


# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

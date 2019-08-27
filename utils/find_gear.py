""" 
Using the location of here file, find the path to the
gear itself assuming this test directory name is the gear name + "_test".

Then:
    Set global variaibles (in ALLCAPPS)
    Change into the gear directory
    Open the manifest.json as MANIFEST
    Make sure the gear name matches
"""

import os
import json


verbose = False

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
GEAR = BASE+NAME
TEST = BASE+NAME+'-test/'

if verbose:
    print(f'NAME="{NAME}"')
    print(f'BASE="{BASE}"')
    print(f'GEAR="{GEAR}"')
    print(f'TEST="{TEST}"')

# Make sure the gear directory exists
if os.path.isdir(GEAR):

    os.chdir(GEAR)

    with open('manifest.json', 'r') as f:
        MANIFEST = json.load(f)

    if gear_name != MANIFEST["name"]:
        print('Gear name in manifest, "'+MANIFEST["name"]+'" '+\
              'does not match gear name found in path, "'+gear_name+'"')
        print('Exiting early')
        sys.exit()
    else:
        if verbose:
            print('Gear name in manifest matches gear name found in path')

else:
    print('ERROR: Path does not exist:')
    print('  '+GEAR)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

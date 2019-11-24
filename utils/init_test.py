#!/usr/bin/env python3
"""Initialize test directories by geting information from the user"""

import os
import subprocess as sp
import shutil

from utils.find_gear import * # variables in ALLCAPS are defined here
from utils.get_user_input import get_verified_input


def init_test_directory():
    """create new test directory with the given name"""

    # name of test will be directory name in 'tests/'
    test_name = 'default' 
    test_name = get_verified_input(test_name,
        "\nPlease enter a name for the new test directory ")

    test_dir = TEST + 'tests/' + test_name
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        # All tests in the tests/ directory are ignored by git except
        # for test/ (and the .gitignore file so that they will not
        # be accidentally pushed to the bids-app-template-test repo.
        msg = 'Created directory:\n  ' + test_dir
        print(msg)
        LOG.info(msg)
    else:
        msg = 'The test directory already exists\n  ' + test_dir
        print(msg)
        LOG.info(msg)

    return test_name


def init_test_subdirs(test_name):
    """Create all necessary test sub-directories if they don't already exist"""

    dirs_to_create = ['input', 'logs', 'output', 'src', 'test_files', 'work']
    for dd in dirs_to_create:
        adir = TEST+"tests/"+test_name+'/'+dd
        if not os.path.exists(adir):
            os.mkdir(adir)

    # create the two files that are imported before and after running the gear in run.py
    files_to_create = ['start.py', 'finish.py']
    for ff in files_to_create:
        fromfile = TEST+'tests/test/src/'+ff
        tofile = TEST+"tests/"+test_name+'/src/'+ff
        if not os.path.exists(tofile):
            shutil.copy(fromfile,tofile)

    msg = 'Created directories: ' + ' '.join(d for d in files_to_create)
    print(msg)
    LOG.info(msg)

    print('\nHere is what is inside "' + test_name + '"')
    sp.run(['ls',TEST + "tests/" + test_name])


def init_test_config(test_name):
    """Generating config.json from manifest.json"""

    msg = init_test_config.__doc__
    print(msg)
    LOG.info(msg)

    with open(GEAR + '/manifest.json') as manifest_file:
        manifest = json.load(manifest_file)
        #print(repr(manifest))

    config = dict()
    config['inputs'] = dict()
    config['destination'] = dict()
    config['config'] = dict()

    if ('key' in manifest['inputs'] and 'base' in manifest['inputs']['key'] and
        manifest['inputs']['key']['base'] == 'api-key'):

        # ask user for key
        api_key = get_verified_input('none', 'Enter an API key for config.json')

        if api_key != '' and api_key != 'none':

            config['inputs']['api_key'] = dict()
            config['inputs']['api_key']['key'] = api_key
            config['inputs']['api_key']['base'] = manifest['inputs']['key']['base']
            config['inputs']['api_key']['read-only'] = manifest['inputs']['key']['read-only']

    # ask user for key (the default here is from the TOME project)
    dest_id = get_verified_input('5dd80e738b0dc70029b59cbe', 
                                 'Enter a destination id for config.json')
    dest_type = get_verified_input('analysis', 'Enter an destination type for config.json')
    # TODO: ask user for a session id directly, then find an apropriate destination from
    # that session.  Any acquisition or analysis should do since it's parent will be the
    # session.

    config['destination']['type'] = dest_type
    config['destination']['id'] = dest_id

    # grab all default items in the manifest and save in config
    for key, val in manifest['config'].items():
        if 'default' in val:
            config['config'][key] = val['default']

    with open(TEST+'tests/'+test_name+'/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

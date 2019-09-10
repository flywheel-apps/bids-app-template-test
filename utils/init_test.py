#!/usr/bin/env python3
"""
"""

import os
import subprocess as sp

from utils.find_gear import *
from utils.get_user_input import *


def init_test_directory():
    """ create new test directory with the given name """

    # name of test will be directory name in 'tests/'
    test_name = 'default' 
    test_name = get_verified_input(test_name,
        "\nPlease enter a name for the new test directory ")

    test_dir = TEST + 'tests/' + test_name
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        with open(TEST + 'tests/.gitignore', 'a') as gf:
            gf.write(test_name+'\n')
    else:
        print('The test directory already exists\n  '+test_dir)

    return test_name


def init_test_subdirs(test_name):
    """ create all necessary test sub-directories if they don't already exist """

    dirs_to_create = ['input', 'logs', 'output', 'src', 'test_files', 'work']
    for dd in dirs_to_create:
        adir = TEST+"tests/"+test_name+'/'+dd
        if not os.path.exists(adir):
            os.mkdir(adir)

    # create the two files that are imported before and after tests in run.py
    files_to_create = ['start.py', 'finish.py']
    for ff in files_to_create:
        afile = TEST+"tests/"+test_name+'/src/'+ff
        if not os.path.exists(afile):
            with open(afile, 'w') as f:
                f.write('\n')
                f.write('\n')
                f.write("# vi:set autoindent ts=4 sw=4 expandtab "+\
                        ": See Vim, :help 'modeline'\n")

    print('\nHere is what is inside "' + test_name + '"')
    sp.run(['ls',TEST + "tests/" + test_name])


def init_test_config(test_name):

    print('generating config.json from manifest.json')

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

    # ask user for key
    dest_id = get_verified_input('5d2761383289d60037e8b180', 
                                 'Enter a destination id for config.json')
    dest_type = get_verified_input('acquisition', 'Enter an destination type for config.json')
    # TODO: askuser for a session id directly, then find an apropriate destination from
    # that session.  Any acquisition or analysis should do since it's parent will be the
    # session.

    config['destination']['type'] = 'acquisition'
    config['destination']['id'] = '5d2761383289d60037e8b180'

    # grab all default items in the manifest and save in config
    for key, val in manifest['config'].items():
        if 'default' in val:
            config['config'][key] = val['default']

    with open(TEST+'tests/'+test_name+'/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

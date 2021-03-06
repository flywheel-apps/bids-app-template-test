#!/usr/bin/env python3
"""
This runs the "default" test or the given tests.  Test names are the
directory names in ./tests/
"""

import os
import json
import datetime
import subprocess as sp
import sys
import argparse

from utils.find_gear import *

def main(test):
    """ Runs gear with the given test files """

    print('\nRunning test "' + test + '"\n')

    if not os.path.exists(TEST + 'tests/' + test):
        print('Sorry, the test "' + test + '" does not exist.  ' + 
              'Create one using ./setup.py')
        exit(-1)

    if not os.path.isfile(TEST + 'tests/' + test + '/config.json'):
        print('Sorry, the test "' + test + '" does not have config.json')
        print('You can run setup.py to create one.')
        exit(-1)

    # Run any desired initialization for this test
    module = ('tests/' + test + '/src/start').replace('/','.')
    print('Running "' + module + '"')
    __import__(module)

    # Set log name to reflect current time (before run)
    log_path = TEST+'tests/'+test+'/logs/'
    cur_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_name = cur_datetime + '_log.txt'

    # Set variables to use in cmd
    if args.shell:
        entry = '/bin/bash'
        dash_args = 'ti'
    else:
        entry = FLY0+'run.py'
        dash_args = 't'

    container_name = cur_datetime + "_" + gear_name + "_" + test

    if 'docker-image' in MANIFEST["custom"]:
        tag = ' '+MANIFEST["custom"]["docker-image"]
    elif 'gear-builder' in MANIFEST["custom"]:
        tag = ' '+MANIFEST["custom"]["gear-builder"]["image"]
    else:
        print('FAIL: cannot determin name and version of gear from manifest.')
        sys.exit(-1)

    cmd= f'docker run -{dash_args}  --name {container_name} '+ \
         '--entrypoint='+entry+' '+ \
         '-v '+TEST+'tests/'+test+'/input:'+FLY0+'input '+ \
         '-v '+TEST+'tests/'+test+'/output:'+FLY0+'output '+ \
         '-v '+TEST+'tests/'+test+'/config.json:'+FLY0+'config.json '+ \
         '-v '+TEST+'tests/'+test+'/work:'+FLY0+'work '+ \
         '-v '+GEAR+':'+FLY0+'src '+ tag

    print('Command:\n\n'+cmd+'\n')

    command = [ w for w in cmd.split() ]

    result = sp.run(command, universal_newlines=True)

    if args.verbose:
        print(f'{cmd.split()[:2]} return code: '+str(result.returncode))
        print('output: \n' + str(result.stdout))


    # save log
    msg = 'Logging output to ' + log_path + log_name
    print(msg)
    LOG.info(msg)
    
    cmd = f'docker logs {container_name} > ' + log_path + log_name
    print('running "' + cmd + '"')
    result = sp.run(cmd, universal_newlines=True, shell=True)
    if args.verbose:
        print(f'{cmd.split()[:2]} return code: '+str(result.returncode))
        print('output: \n' + str(result.stdout))

    # remove the container
    if args.dontrm:
        LOG.info('NOT removing container')
    else:
        LOG.info('Removing container')
        cmd = f'docker rm {container_name}'
        print('running "' + cmd + '"')
        command = [ w for w in cmd.split() ]
        result = sp.run(command, universal_newlines=True)
        if args.verbose:
            print(f'{cmd.split()[:2]} return code: '+str(result.returncode))
            print('output: \n' + str(result.stdout))

    # Run any desired cleanup for this test
    print('Running '+('tests/' + test + '/src/finish').replace('/','.'))
    __import__(('tests/' + test + '/src/finish').replace('/','.'))

    if TESTING == 'basic':
        LOG.info('Now check the results of running')
        # TODO chek the results of running
        LOG.info('Done with '+TESTING+' test.\n')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-t", "--test", default='', nargs='*',
                        help="the test in tests/ to run.  'all' runs all" \
                             " tests.  Can be given as just the test directory"\
                             " name or 'tests/test_directory_name' so it can" \
                             " be chosen using tab-completion.")
    parser.add_argument("-s", "--shell", action="store_true",
                        help="run bash in the container instead of run.py.")
    parser.add_argument("-d", "--dontrm", action="store_true",
                        help="don't remove the container after logging.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print what is going on.")
    args = parser.parse_args()

    re_written_test = []
    for test in args.test:
        if test[-1] == '/':
            test = test[:-1]
        if test[:6] == 'tests/':
            re_written_test.append(test[6:])
        else:
            re_written_test.append(test)
    args.test = re_written_test

    if args.test == []: # no arguments, run default
        test = 'default'  # run only the default test
        main(test)  # run the test for this test template

    # check for "run.py all"
    elif args.test[0] in ['all','All','ALL']:

        # run each test in the tests directory
        for test in os.listdir(TEST+'tests'):
            if test[0] != '.' and test[0] != '_':
                print('\n\nRunning test "' + test + '"\n')
                main(test)
        print('\nDone running all tests.\n')

    else:

        # before running the given tests, make sure they exist
        for test in args.test:
            if not os.path.isdir(TEST+'tests/'+test):
                print('ERROR "'+test+'" is not a valid test, choices are:')
                result = sp.run(['ls',TEST+'tests/'])
                sys.exit(-1)

        for test in args.test:
            main(test)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

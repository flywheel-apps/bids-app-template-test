#!/usr/bin/env python3
""" bids-app-template-test run.py
This test runs the "default" test or the given tests.  Test names are the
directory names in bids-app-template-test/tests/.
"""

import os
import json
import datetime
import subprocess as sp
import sys
import argparse

from utils.find_gear import *

verbose = True

def main(test):
    """ Runs gear with the given test files """

    if verbose:
        print('Running test "' + test + '"')

    if not os.path.exists(TEST + 'tests/' + test):
        print('Sorry, the test "' + test + '" does not exist')
        exit(-1)

    if not os.path.isfile(TEST + 'tests/' + test + '/config.json'):
        print('Sorry, the test "' + test + '" does not have config.json')
        print('You can run setup.py to create one.')
        exit(-1)

    # Run any desired initialization for this test
    print('Running '+('tests/' + test + '/src/start').replace('/','.'))
    __import__(('tests/' + test + '/src/start').replace('/','.'))

    if args.shell:
        entry = '/bin/bash'
    else:
        entry = FLY0+'run.py'

    cmd= 'docker run --rm -ti --entrypoint='+entry+' '+\
         '-v '+TEST+'tests/'+test+'/input:'+FLY0+'input '+\
         '-v '+TEST+'tests/'+test+'/output:'+FLY0+'output '+\
         '-v '+TEST+'tests/'+test+'/config.json:'+FLY0+'config.json '+\
         '-v '+TEST+'tests/'+test+'/work:'+FLY0+'work '+\
         '-v '+GEAR+':'+FLY0+'src '+\
        f'{MANIFEST["custom"]["docker-image"]}'

    if verbose:
        print('Command:\n\n'+cmd+'\n')

    command = [ w for w in cmd.split() ]

    if args.shell:
        result = sp.run(command)
    else:
        result = sp.run(command,stdout=sp.PIPE, stderr=sp.PIPE,
                        universal_newlines=True)

    if verbose:
        print(f'{cmd.split()[:2]} return code: '+str(result.returncode))
        print('output: ',result.stdout)

    log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'_log.txt'
    LOG.info('Saving output to '+TEST+'tests/'+test+'/logs/'+log_name)
    if result.stdout:
        with open(TEST+'tests/'+test+'/logs/'+log_name,'w') as f:
            f.write(result.stdout)

    # Run any desired cleanup for this test
    print('Running '+('tests/' + test + '/src/finish').replace('/','.'))
    __import__(('tests/' + test + '/src/finish').replace('/','.'))

    if TESTING == 'basic':
        LOG.info('Now check the results of running')
        LOG.info('Done with '+TESTING+' test.\n')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-t", "--test", default='', nargs='*',
                        help="the test in tests/ to run.  'all' runs all tests.")
    parser.add_argument("-s", "--shell", action="store_true",
                        help="run bash in the container instead of run.py.")
    args = parser.parse_args()

    if args.test == '': # no arguments, run default
        test = 'default'  # run only the default test
        main(test)  # run the test for this test template

    # check for "run.py all"
    elif args.test in ['all','All','ALL']:

        # run each test in the tests directory
        for test in os.listdir(TEST+'tests'):
            run.main(test)
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

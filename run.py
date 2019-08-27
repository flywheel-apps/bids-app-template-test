#!/usr/bin/env python3

import os
import json
import datetime
import subprocess as sp
import sys

from utils.find_gear import *

def main(test):
    """ Runs gear with the given test files """

    print(f'Running test {test}')

    cmd= 'docker run --rm -ti --entrypoint='+FLY0+'run '+\
         '-v '+TEST+'tests/'+test+'/input:'+FLY0+'input '+\
         '-v '+TEST+'tests/'+test+'/output:'+FLY0+'output '+\
         '-v '+TEST+'tests/'+test+'/config.json:'+FLY0+'config.json '+\
         '-v '+TEST+'tests/'+test+'/work:'+FLY0+'work '+\
         '-v '+GEAR+':'+FLY0+'/src '+\
        f'{MANIFEST["custom"]["docker-image"]}'

    print('Command:\n\n'+cmd+'\n')
    command = [ w for w in cmd.split() ]
    result = sp.run(command,stdout=sp.PIPE, stderr=sp.PIPE,
                    universal_newlines=True)
    print(f'{cmd.split()[:2]} return code: '+str(result.returncode))
    #print('output: ',result.stdout)

    log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'_log.txt'
    with open(TEST+'tests/'+test+'/logs/'+log_name,'w') as f:
        f.write(result.stdout)

if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) == 1: # no arguments, run default

        main('default')  # run only the default test

    # check for "run.py all"
    elif len(sys.argv) == 2 and sys.argv[1] in ['all','All','ALL']:

        # run each test in the tests directory
        for test in os.listdir(TEST+'tests'):
            run.main(test)
    else:

        # before running the given tests, make sure they exist
        for arg in sys.argv[1:]:
            if not os.path.isdir(TEST+'tests/'+arg):
                print('ERROR "'+arg+'" is not a valid test, choices are:')
                result = sp.run(['ls',TEST+'tests/'])
                sys.exit(-1)

        for arg in sys.argv[1:]:
            main(arg)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

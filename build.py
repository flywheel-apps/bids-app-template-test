#!/usr/bin/env python3
"""Run Docker build for this gear"""

import os
import subprocess as sp
import sys
import argparse

from utils.find_gear import * # variables in ALLCAPS are defined here


verbose = True

LOG.info('STATUS is '+STATUS)

return_code = -1

if STATUS == 'OK':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n","--no-cache",action='store_true',
                        help="build container without cache")
    args = parser.parse_args()
    #print(args)


    LOG.info('Starting build...')

    if args.no_cache:
        cache = '--no-cache'
    else:
        cache = ''

    if 'docker-image' in MANIFEST["custom"]:
        tag = ' --tag='+MANIFEST["custom"]["docker-image"]
    elif 'gear-builder' in MANIFEST["custom"]:
        tag = ' --tag='+MANIFEST["custom"]["gear-builder"]["image"]
    else:
        print('FAIL: cannot determin name and version of gear from manifest.')
        sys.exit(-1)

    cmd= 'docker build ' + cache + tag + ' ' + GEAR 

    LOG.info('Running "'+cmd+'"')

    if verbose:
        print('Runnning:\n\n'+cmd+'\n')

    command = [ w for w in cmd.split() ]
    result = sp.run(command)

    msg = command[0]+' return code: '+str(result.returncode)+'\n'

    return_code = result.returncode

    LOG.info(msg)
    if verbose:
        print(msg)

    if result.stdout:
        LOG.info(result.stdout+'\n')
        if verbose:
            print(result.stdout)

    if TESTING == 'basic':
        LOG.info('Now check the results of building')
        # TODO chek the results of building
        LOG.info('Done with '+TESTING+' test.\n')

sys.exit(return_code)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

#!/usr/bin/env python3

import os
import subprocess as sp
import sys

from utils.find_gear import *

verbose = True

LOG.info('STATUS is '+STATUS)

return_code = -1

if STATUS == 'OK':

    LOG.info('Starting build...')

    cmd= 'docker build --tag='+MANIFEST["custom"]["docker-image"]+' '+GEAR 

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
        LOG.info('Now check the results')
        LOG.info('Done with '+TESTING+' test.\n')

sys.exit(return_code)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

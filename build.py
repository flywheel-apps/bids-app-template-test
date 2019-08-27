#!/usr/bin/env python3

import os
import subprocess as sp

from utils.find_gear import *

cmd= 'docker build --tag='+MANIFEST["custom"]["docker-image"]+' '+GEAR 

print('Runnning:\n\n'+cmd+'\n')
command = [ w for w in cmd.split() ]
result = sp.run(command)
print(f'{cmd[0]} return code: '+str(result.returncode))
print(result.stdout)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

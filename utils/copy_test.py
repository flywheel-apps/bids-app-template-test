#!/usr/bin/env python3
""" 
Copy a gear test using hard links for the files to avoid wasting a
lot of space.  The files need to be hard links so they will show
up in the Docker container (symbolic links show up as symbolic links
to nowhere).
"""

import os
import shutil
import subprocess as sp


def copy(src, dst):

    if os.path.isdir(src):

        # here's the beef:
        shutil.copytree(src, dst, copy_function=os.link)
        # and remove the old test's logs (if any)
        shutil.rmtree(dst+'/logs')
        os.mkdir(dst+'/logs')

    else:
        print('ERROR: "'+args.src+'" not found.  It should be in')
        print('ls '+TEST+'tests/')
        result = sp.run(['ls',TEST+'tests/'])

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

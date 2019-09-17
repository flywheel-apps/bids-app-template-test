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
import argparse

from .find_gear import *
from .get_user_input import *


def copy(src, dst):
    """ Copies a test directory and deletes all old log files.  """

    if os.path.isdir(src):

        # here's the beef:
        shutil.copytree(src, dst, copy_function=os.link)
        # and remove the old test's logs (if any)
        shutil.rmtree(dst+'/logs')
        os.mkdir(dst+'/logs')

        msg - 'Copied test from\n  ' + src + '\nto\n  ' + dst
        print(msg)
        LOG.info(msg)

    else:
        print('ERROR: "'+args.src+'" not found.  It should be in')
        print('ls '+TEST+'tests/')
        result = sp.run(['ls',TEST+'tests/'])


def init_by_copying():
    """ This is called from setup.py.  To let the user knonw that
    they can call copy_test.py from the command line, this does just that 
    This is a whole lot of wrapping around the tiny bit of code above """

    print("Copying an existing test...\n")

    msg = "Choose a test to copy:\n"
    tests = os.listdir(TEST+'tests/')
    nn = 1
    dir_name = dict()
    choices = []
    for tt in tests:
        if tt[0] != '.':
            msg += "  "+str(nn)+") "+tt+"\n"
            dir_name[nn] = tt
            choices.append(str(nn))
            nn += 1

    not_done = True

    while not_done:

        ans = get_user_input(msg,"Which would you like to use?",choices)

        new_name = input('Please enter a name for the new test: ')

        print("The new test will be created with this command:\n")
        cmd = 'utils/copy_test.py '+dir_name[int(ans)]+' '+new_name
        print('  '+cmd+'\n')
        print('(You can run that command yourself instead of this script)')

        go_nogo = get_user_input("","",['Proceed','Re-enter','Quit?'])

        if go_nogo == 'p':
            not_done = False
        elif go_nogo == 'q':
            sys.exit()

    command = TEST+cmd # add full path
    print('Running: '+command)
    LOG.info('Running" '+command)
    command = [ w for w in command.split() ]
    result = sp.run(command)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src",help="(old) source test direcory name (no path)")
    parser.add_argument("dst",help="(new) destination directory name")
    args = parser.parse_args()

    src = TEST+'tests/'+args.src
    dst = TEST+'tests/'+args.dst

    copy(src,dst)

# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

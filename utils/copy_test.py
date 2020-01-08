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


def copy(src, dst):
    """ Copies a test directory, deletes all old log files.  """

    if os.path.isdir(src):

        try:
            # here's the beef:
            shutil.copytree(src, dst, copy_function=os.link)

        except Exception as e:
            LOG.error(e)
            print(e)
            msg='WARNING: continuing despite errors'
            print(msg)
            LOG.info('WARNING: continuing despite errors')
            

        # and remove the old test's logs (if any)
        shutil.rmtree(dst+'/logs')
        os.mkdir(dst+'/logs')

        # delete the hard-linked config.json and actually
        # copy it so it can be edited without modifying the
        # old config.
        os.remove(dst + '/config.json')
        shutil.copyfile(src + '/config.json',dst + '/config.json')

        msg = 'Copied test from\n  ' + src + '\nto\n  ' + dst
        print(msg)
        LOG.info(msg)

        msg = 'NOTE: all files were copied as HARD links except for \n'+\
              '"confid.json".  Unless you want to modify a file in the \n'+\
              'old test that was copied, DELETE the file and create a new one'
        print(msg)

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
        if tt[0] != '.' and tt[0] != '_':
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

    from find_gear import *
    from get_user_input import *

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src",help="(old) source test direcory name (no path)")
    parser.add_argument("dst",help="(new) destination directory name")
    args = parser.parse_args()

    src = TEST+'tests/'+args.src
    dst = TEST+'tests/'+args.dst

    copy(src,dst)

else:

    from .find_gear import *
    from .get_user_input import *


# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

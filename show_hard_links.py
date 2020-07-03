#!/usr/bin/env python3
"""This displays all files that are hard linked.

    Args:
        test (directory name): optional, name of test to show results for

    This must be run from the top <gearname>-test directory where the
    command is.
"""

import os
import sys


verbose = False

inode_path = dict()
inode_tests = dict()

show_all = True
len_test = 0

if len(sys.argv) == 2:
    test = sys.argv[1]
    len_test = len(test)
    show_all = False

for subdir, dirs, files in os.walk('tests'):
    if verbose:
        print(subdir)
        print(dirs)
        print(files)

    for file in files:

        full_path = os.path.join(subdir, file)

        try:
            i_node = os.stat(full_path).st_ino
        except FileNotFoundError as e:
            print(e)
            continue

        if verbose:
            print(i_node, full_path)

        try:
            inode_path[i_node].append(full_path)
            inode_tests[i_node].append(full_path[0:len_test])
        except KeyError:
            inode_path[i_node] = [full_path]
            inode_tests[i_node] = [full_path[0:len_test]]

print('\nResults', end = '')
if show_all:
    print(':\n')
else:
    print(f' for test {test}:\n')

for kk,vv in inode_path.items():

    if verbose:
        if len(vv) > 1:
            print(kk)
            print(vv)
            print(inode_tests[kk])
            print()

    if len(vv) > 1 and (show_all or test in inode_tests[kk]):

        print('/'.join(vv[0].split('/')[2:]))
        for vvv in vv:
            print('  ' + vvv.split('/')[1])

        print()

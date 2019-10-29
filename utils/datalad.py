
import os
import shutil
import json

from utils.find_gear import * # variables in ALLCAPS are defined here
from utils.get_user_input import get_user_input, get_verified_input
from utils.init_test import init_test_directory, init_test_subdirs, init_test_config


def get_datalad_subject(datasource, setname, subject, bids_dir):
    """ Loads actual data files (not links to) the given subject from the
    given DataLad datset and puts them into the given BIDS directory (path).
    
    e.g. 'dbic', 'QA', 'sub-amit' will load all files for
    
          '///dbic/QA/sub-amit/'
    
    This needs to be done because DataLad "installs" metadata, and then
    "gets" only specific data files that are asked for and uses git-annex
    to do the work.  Only the files for the given subject will be downloaded
    and made into hard links.
    """

    datauri = '///'+datasource+'/'

    dataset = datauri+setname

    cmdset = []

    # grab metadata for whole dataset
    cmdset.append('datalad install '+dataset)
    cmdset.append('datalad get '+setname+'/'+subject+'/')

    # turn symlinks into hard links (files)
    cmdset.append('datalad unlock '+setname+'/'+subject+'/')

    #for cmd in cmdset:
    #    print(cmd)

    os.chdir(bids_dir)

    for cmd in cmdset:
        print('Running: '+cmd)
        LOG.info('Running" '+cmd)
        command = [ w for w in cmd.split() ]
        result = sp.run(command)


def init_using_datalad():
    """ This initializes a test using data from datalad """

    msg = "Useing DataLad...\n"
    print(msg)
    LOG.info(msg)

    if TESTING == 'basic':

        test_name = 'test' # use the existing test directory instead of creating on

    else: # not testing,  initialize actual test

        test_name = init_test_directory()

    init_test_subdirs(test_name)

    # this is where to put the "bids" directory with data:
    work_dir = TEST+"tests/"+test_name+"/work/"
    #print(work_dir)

    # Ideally, this would be a good place to querry DataLad to
    # see what's available.  But for now here are some examples
    # that might be good. TODO add more useful examples.

    # TODO: Add the ability to have setup.py download DataLad data by 
    # putting the URI in the work/bids/ directory.

    msg = """
    Here are some example data sets you can install into the work/bids/ directory:

      1) ///dbic/QA/sub-amit/ - single subject with single session,
                                single anat, dwi, func, 80.8 MB

      2) ///dbic/QA/sub-emmet/ - single subject, multiple sessions with
                                 anat, dwi, fmap, multiple func, 405.4 MB

      3) enter a URI for a subject.  Look here to find datasets:

                http://datasets.datalad.org/?dir=/dbic/QA

      4) don't install anything
    """

    ans = get_user_input(msg,
              "Please choose an option:",['1','2','3','4'])

    if ans == '1':
        print('You chose 1')
        datasource = 'dbic'
        setname    = 'QA'
        subject    = 'sub-amit'

    elif ans == '2':
        print('You chose 2')
        datasource = 'dbic'
        setname    = 'QA'
        subject    = 'sub-emmet'

    elif ans == '3':
        print('You chose 3')

        not_done = True

        while not_done:

            uri = get_verified_input('', 'Please enter a DataLad URI ')

            if len(uri) < 9:
                print('the URI must be in the form of '+
                      '///datasource/setname/subject/')

            else:
                sp = uri[3:].split('/')
                print(sp)
                if len(sp) == 3 or (len(sp) == 4 and sp[3] == ''):
                    datasource = sp[0]
                    setname    = sp[1]
                    subject    = sp[2]
                    not_done = False
                else:
                    print('the URI must be in the form of '+
                          '///datasource/setname/subject/')

    else:
        print('You chose 4, no example data will be installed')
        datasource = ''
        setname = ''
        subject = ''

    # actually grab the data
    if datasource != '':
        msg = 'Downloading ///' + datasource +'/'+ setname +'/'+ subject +\
              '/ into ' + work_dir
        print(msg)
        LOG.info(msg)

        get_datalad_subject(datasource, setname, subject, work_dir)
        os.rename(work_dir + setname, work_dir + 'bids')

    # create config.json in a test directory from manifest.json
    # and ask user for api key

    ff = 'config.json'

    if os.path.exists(TEST+ff):
        msg = 'Using existing config.json file'
        print(msg)
        LOG.info(msg)

    else:
        if TESTING == 'basic': # use the config file in test_files

            msg = 'Copying test_files/'+ff
            print(msg)
            LOG.info(msg)

            api_key = get_verified_input('none', 'Enter an API key for config.json')

            if api_key == 'none' or api_key == '':
                shutil.copyfile(TEST+'test_files/'+ff,TEST+ff)

            else: # copy line-by-line while substituting in API key

                with open(TEST+'tests/'+test_name+'/test_files/'+ff) as config_file:
                    config = json.load(config_file)

                config['inputs']['api_key']['key'] = api_key

                with open(TEST+'tests/'+test_name+'/'+ff, 'w') as outfile:
                    json.dump(config, outfile, indent=4)

        else:
            init_test_config(test_name)


# vi:set autoindent ts=4 sw=4 expandtab : See Vim, :help 'modeline'

# bids-app-template-test
Test environment for bids-app-template 

To create a bids-app gear, *do not* just clone this repository in the usual way, please follow these steps.

## Identify BIDS compatible open source code

* See https://github.com/BIDS-Apps.  Maybe what you want is already there.
* Note the open source license.  It needs to be commercially friendly.

## Create GitHub Project

On https://github.com/flywheel-apps, hit the "new" button. 
  *  Create new repository with owner "flywheel-apps" and give it a lower-case-with-dashes name like "bids-freesurfer".  
  * Give it a description like, "Gear that runs freesurfer on BIDS-curated data".  
  * Keep it private for now, not that nobody should see it, but there's no need for a lot of intrusive questions about it before it is even released for the first time.  
  * Check the "Initialize this repository with a README", add a .gitignore for Python, and set the license to the same license as the open source code.
  * Press the "Create Repository" button.
  * Clone your new project locally: press "Clone or download" and then, create a new branch for editing the repository: 

```
git clone git@github.com:flywheel-apps/bids-app-name.git
cd bids-app-name
git checkout -b dev
git push -u origin dev
```

## Clone this repository using a different name

Clone this testing template in the same directory and be sure to use the name of the new
gear repository created above **with “-test” appended** to the end.  The reason for this naming scheme is that the scripts in the test environment will look for the new gear in the same directory but without the "-test" part.  For example:

`git clone git@github.com:flywheel-apps/bids-app-template-test.git  bids-freesurfer-test`

Create a new branch for editing that repository:
```
cd bids-freesurfer-test
git checkout -b dev
git push -u origin dev
```
It's important to change to a new branch in the "-test" repository because you will want to edit some of the files to make your tests work.  As you improve the way your bids-app is tested, you may also want to submit a pull request to share with the community!

Then run the initialization script inside `bids-freesurfer-test/`:

`./setup.py`

That clone command saves the bids-app-template-test repository as
a test repository for the new gear.  The `setup.py` command clones
the bids-app-template repository on GitHub into a temporary location
and copies the following files into the new gear repository:

`Dockerfile   manifest.json   run.py   utils/`

The `setup.py` command uses the name you gave to the directory (e.g. "bids-freesurfer-test") to set the new gear’s proper name inside Dockerfile and manifest.json (e.g. "bids-freesurfer").  The command also gives you a chance to set up a test configuration but you should probably do that later, after the `manifest.json` file is edited.  After the gear is initialized the first time you run `setup.py`, you can run `setup.py` as many times as you like to add additional test configurations.  For now, after running `setup.py`, choose option 5) (or press return) to skip setting up tests which will be described below.

Now you have two directories: the new gear itself and a “-test” directory, and the real development begins.
See [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears) information on the gear specification and what needs to be in each of the files:
  * manifest.json
  * Dockerfile
  * run.py

The instructions linked above on Building Gears are very general.  The usual `input/` and `output/` folders are available while running in the container, but in addition to that, BIDS-App gears can find BIDS formatted data in the directory `/flywheel/v0/work/bids/` (or just `work/bids/`).

You will be developing and testing the gear locally using the commands inside `<your-new-gear-name>-test/`:

 * `./setup.py` to create a new test configuration,
 * `./build.py` to build the container, and
 * `./run.py` to run the default test or `run.py testname` to run a test called “testname".

The scripts can be run from anywhere.  For instance, to re-build and then run the Docker container from within the bids-app after editing stuff there:

```
cd bids-freesurfer
vim run.py
../bids-freesurfer-test/build.py
../bids-freesurfer-test/run.py
```

Note that the last command assumes that you have already set up the "default" test, but you probably have not done that yet.  It's a good idea to first edit the `Docker`, `manifest.json`, and `run.py` files, and then use `setup.py` to create the "default" test.  This is because running the gear requires a `config.json` file and `setup` can use `manifest.json` to create it.  More on this later.

`./setup.py` will create test configurations in the `tests/` sub-folder of `<your-new-gear-name>-test/`.  The name of the sub-folder is the name of the test.  Test folders contain these:

```config.json input/ output/ src/ test_files/ work/```

All of these items will be mounted inside the running Docker container by the `run.py` script _except_ `test_files/`.
The idea here is that testing your bids-gear may require some initialization before running the gear and some clean-up afterwards.  In the `src/` directory you'll fine two code stubs, `start.py` and `finish.py` to do the set-up and clean-up.  These are called by the `bids-app-test/run.py` script (not the `run.py` in the gear itself) and all of this takes place _outside_ the container in preparation for the test.  Because of this, the `test_files/` directory can be used to hold files that, for instance, need to be copied into the `input/` directory before the test by `start.py`.  Then the gear is run.  `test_files/` can also hold files that, for instance, can be compared with results in the `output/` directory after the gear is run.  So `bids-app-test/run.py` first calls `start.py`, then it runs the gear by calling `Docker run ...`, and finally it calls `finish.py`.

The reason for this `start` `run` `finish` scheme is so multiple different tests can be run one after the other and each one will set up and clean up after itself.  

That's nice, but it assumes a lot of development has already occured and the project is fairly mature.  What about finding out what's going on _inside_ the container?  You'll probably need to do some initial debugging in there by running the gear's `run.py` script from the shell.  To do this, use the `--shell` option when running a test:

```bids-app-test/run.py -s```

Instead of actually running the gear by calling `/flywheel/v0/run.py` it will set the Docker entry point to `/bin/bash`.  Moreover, after running the Docker container in one window you can open another window, temporarily copy (or linking) `bids-gear/run.py` into `bids-gear-test/tests/default/src/run.py` and edit the latter in the second window while running it in the first, as long as you run it from inside the container in the first window with `./src/run.py`.  The trick here is that the test's `src/` directory is mounted inside the container along with all of the things the gear actually needs.  But `src/` is only there for the test and does not besmirch the gear itself so the gear can be pushed to GitHub or uploaded to a Flywheel instance without worrying about extra cruft going along with it.

If you want to use PyCharm, for example, to debug from inside the container, `bids-app-test/run.py` prints out the `docker run ...` command so you can copy and paste all of those `-v` volumes into the configuration and you'll be in the same testing environment.

Now that you know how things generally work, it's time to edit `Docker`, `manifest.json`, and `run.py` (and also the utility scripts in `bids-gear/utils/` as necessary).  The scripts in `utils/` provide functionality that help with BIDS-App gears.  For example, `download()` in `utils/bids.py` is used to download data in BIDS format from a flywheel instance (given the proper settings in the gears `config.json`.  It has a nice feature for debugging: if the BIDS data has already been downloaded, it won't download it again.  That will save a lot of time.  When you edit `bids-gear/run.py`, search for the string "editme".  This will provide help in configuring `run.py` to run your gear and also indicate the optional features (like running bids-validator before running the main code). 

After you've made enough progress editing, you'll run `bids-app-test/build.py` to build the Docker container.



Setting up test inputs

Run `setup.py` and it will ask which option you want to chose:

```
Now you can set up a new test in one of the following ways:

    1) Initialize test directories and crete config.json so that BIDS data
       will be downloaded from a session given a destination id and type.
     
    2) Copy an existing test (using hard links so it won't take up much
       extra space)
    
    3) Download test data and config files from a Flywheel instance
    
    4) Download test data using DataLad (https://www.datalad.org/)

    5) Skip this for now (default).  You can run setup.py any time to add
       another test.
    
Which would you like to do? [1,2,3,4,5] 
```

When running the gear for real on a Flywheel instance, it will download BIDS formatted data every time.  As mentioned eaerlier, `utils/bids.py` won't download data if it is already there.  This allows you to modify the data for a test and it won't be overwritten.  Using option 2) of `setup.py` will allow you to take a good set of data and modify it (being careful to consider the hard links) so that you can create tests for broken BIDS data.

`bids-app-test/run.py` sets up logging into the test's `log/` directory (e.g. `bids-app-test/tests/default/logs`).  Logging output from `bids-app-test/run.py` will go there along with logging output from the gear itself.


As you develop new best practices for developing BIDS-App gears, be sure to add them both here and also in [bids-app-template](https://github.com/flywheel-apps/bids-app-template).

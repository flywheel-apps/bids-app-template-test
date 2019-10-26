# bids-app-template-test
Test environment for [`bids-app-template`](https://github.com/flywheel-apps/bids-app-template).

To create a bids-app gear, *do not* just clone this repository in the usual way, please follow these steps.

Beyond initializing a new gear using `bids-app-template`, the objective of these two templates is to set up for building, running and testing that gear.  Community improvements will evolve best practices so gear development and execution will be efficient and effective.  Additional goals include:

* detecting problems early to prevent the gear from running if it will fail,
* giving clear error and warning messages that describe the problem _and_ point to the code where the issue was detected,
* being a place to hold excellent code snippets and flywheel platform tricks.

Before following the steps below, you should be familiar with [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears).  These templates were initially developed for gears that expect data to be in BIDS format, but any gear can get a great start here.  

## Overview of steps:

- Create a GitHub project and clone it locally
- Clone this test repository using your new gear name plus "-test"
- Run `setup.py` to initialize your new gear
- Edit the gear's python scripts, `manifest.json`, and `Dockerfile`
- Run `setup.py` again to set up tests with data
- Run `build.py` to build the gear from the Dockerfile
- Run `run_tests.py` to run the gear in using test data.

## Identify BIDS compatible open source code

* See https://github.com/BIDS-Apps.  If what you want is already there, your work is well on its way.
* Note the open source license.  It needs to be commercially friendly.

## Create GitHub Project

On https://github.com/flywheel-apps, hit the "new" button. 
  *  Create new repository with owner "flywheel-apps" and give it a lower-case-with-dashes name like "bids-freesurfer".  In the following instructions, it will be called `bids-app`.  
  * Give it a description like, "Gear that runs freesurfer on BIDS-curated data".  
  * Keep it private for now, not that nobody should see it, but there's no need for a lot of intrusive questions about it before it is even released for the first time.  
  * Check the "Initialize this repository with a README", add a .gitignore for Python, and set the license to the same license as the open source code.
  * Press the "Create Repository" button.
  * Clone your new project locally: press "Clone or download" and then, create a new branch for editing the repository: 

```
git clone git@github.com:flywheel-apps/bids-app.git
cd bids-app
git checkout -b dev
git push -u origin dev
cd ..
```

At this point you'll have 3 files in your local gear directory: `.gitignore`, `LICENSE`, and `README.md`, and you have a "dev" branch locally and on GitHub.
If you don't want to create a GitHub repository, you can just create a directory with your new bids-app name.

## Clone this repository using a different name

Clone this testing template in the directory above the new bids-app (so the two will be in the same directory) and be sure to use the name of the new gear repository created above **with “-test” appended** to the end.  For example, run:

```git clone git@github.com:flywheel-apps/bids-app-template-test.git  bids-app-test```

where the `bids-app` part of `bids-app-test` is the name of the new gear you created on GitHub.  The reason for this naming scheme is that the scripts in the test environment will look for the new gear at the same directory level but without the "-test" part in the name.  

Then create a new branch for editing the test repository:
```
cd bids-app-test
git checkout -b dev
```
It's important to change to a new branch in the "-test" repository because you will want to edit some of the files to make your tests work.  As you improve the way your bids-app is tested, you may also want to submit a pull request to share with the community!  Note that if you do not have permission to edit flywheel-apps directly, you will need to fork your own repository and clone it into the proper name as shown above.

## Run `./setup.py`

Now make sure that your new `bids-app` and `bids-app-test` are in the same directory.  Then run the initialization script inside `bids-app-test/`:

`./setup.py`

The `setup.py` command clones the `flywheel-apps/bids-app-template` repository from GitHub into a temporary location and copies only the following files into your new bids-app gear repository:

`Dockerfile   manifest.json   run.py   utils/`

The `setup.py` command uses the name you gave to the directory "bids-app-test" to substitute the new gear’s actual name inside `Dockerfile` and `manifest.json` as it copies them.  The command also gives you a chance to set up a test configuration but you should probably do that later, after the `manifest.json` file is edited.  The gear is initialized the first time you run `setup.py`.  You can run `setup.py` as many times as you like to add additional test configurations.  For now, after running `setup.py`, choose the last option (or press return) to skip setting up tests which will be described below.

## How things work

### Building gears

Now you have two directories: the new gear itself and a “-test” directory.  It's time for the real software development to begin.  See [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears) information on the gear specification and what needs to be in each of the files:
  * manifest.json
  * Dockerfile
  * run.py

The [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears) instructions are very general.  The usual `input/` and `output/` folders are available while running in the container, but in addition to that, BIDS-App gears can find BIDS formatted data in the directory `/flywheel/v0/work/bids/` (or with the relative path `work/bids/` because gears are executed from `/flywheel/v0').

You will be developing and testing the gear locally and can use the helpful commands inside `<your-new-gear-name>-test/`:

 * `./setup.py` to create a new test configuration,
 * `./build.py` to build the container, and
 * `./run_tests.py` to run the "default" test or `run_tests.py -t testname` to run a test called “testname".

The scripts can be run from anywhere.  For instance, to re-build and then run the Docker container from within your new bids-app directory after editing stuff there:

```
cd bids-app
vim run.py
../bids-app-test/build.py
../bids-app-test/run\_tests.py
```

Note that the last command assumes that you have already set up the "default" test, but you probably have not done that yet.  It's a good idea to first edit the `Dockerfile`, `manifest.json`, and `run.py` files, and then use `setup.py` to create the "default" test.  This is because running the gear requires a `config.json` file and `setup` can use `manifest.json` to create it.  More on this later.

### Testing gears

`./setup.py` creates test configurations in the `tests/` sub-folder of `<your-new-gear-name>-test/`.  The name of the sub-folder is the name of the test.  Test folders contain these:

```config.json input/ output/ src/ test_files/ work/```

All of these items will be mounted inside the running Docker container by the `run_tests.py` script _except_ `test_files/`.
The idea here is that testing your bids-gear may require some initialization before running the gear and some clean-up afterwards.  In the `src/` directory you'll fine two code stubs, `start.py` and `finish.py` to do the set-up and clean-up.  These are called by the `bids-app-test/run_tests.py` script and all of this takes place _outside_ the container in preparation for the test.  Because of this, the `test_files/` directory can be used to hold files that, for instance, need to be copied into the `input/` directory before the test by `start.py`.  Then the gear is run.  `test_files/` can also hold files that, for instance, can be compared with results in the `output/` directory after the gear is run.  So `bids-app-test/run_tests.py` first calls `start.py`, then it runs the gear by calling `docker run ...`, and finally it calls `finish.py`.

The reason for this `start` `run` `finish` sequence is so multiple different tests can be run one after the other and each one will set up and clean up after itself.  

That's nice, but it assumes a lot of development has already occurred and the project is fairly mature.  What about finding out what's going on _inside_ the container?  You'll probably need to do some initial debugging in there by running the gear's `run.py` script from the shell.  To do this, use the `--shell` option when running a test:

```bids-app-test/run_tests.py -s```

Instead of actually running the gear by calling `/flywheel/v0/run.py` it will set the Docker entry point to `/bin/bash`.  Moreover, after running the Docker container in one window you can open another window and edit `bids-app/run.py` in that second window while running it inside the container in the first window with `./src/run.py` as opposed to the normal `./run.py` in the running container.  The trick here is that the gear directory `bids-app/` is mounted inside the container as `src/`.  But `src/` is only there for the test and does not besmirch the gear itself so the gear can be pushed to GitHub or uploaded to a Flywheel instance without worrying about extra cruft going along with it.

If you want to use PyCharm to debug from inside the running container, `bids-app-test/run_tests.py` prints out the `docker run ...` command so you can copy and paste all of those `-v` volumes into the configuration and you'll be in the same testing environment.

## Edit gear files

Now that you know how things generally work, it's time to edit `Dockerfile`, `manifest.json`, and `run.py` and also the utility scripts in `utils/` as necessary.  The scripts in the subdirectories of `utils/` provide functionality that help with BIDS-App gears.  For example, `download_bids()` in `utils/bids/download_bids.py` is used to download data in BIDS format from a flywheel instance (given the proper settings in `config.json`).  This function has a nice feature for debugging: if the BIDS data has already been downloaded, it won't download it again.  That will save a lot of time.  When you edit `bids-gear/run.py` and `bids-gear/utils/args.py`, search for the string "editme".  This string marks places in the python code that must be edited and also indicates optional features (like running bids-validator before running the main code). Ideally, you won't have to edit the python modules in `utils/*/*.py` because they are established methods for getting things done.  But if you do need edit them or if you've found a better way to do it, please consider creating a pull request to share with the community.  You can delete any subdirectory module that you don't call.

Each time you edit `Dockerfile`, `manifest.json`, or any python file, run `bids-app-test/build.py` to re-build the Docker container.  When you are done editing, you'll need some test data to debug the gear.

## Set up tests with BIDS data

Run `setup.py` and it will ask which way you want to create a test:

```
Now you can set up a new test in one of the following ways:

    0) Recommended: Initialize a test and create config.json by entering a
       Flywheel api key, destination id and type.  The defaults in manifest.json
       file are used to create config.json so it must  already exist.  BIDS data
       will be downloaded from the specified session the first time the gear is
       run.

    1) Initialize a "blank" test with no data or config.json. You will have
       to put BIDS data into "work/bids" and create config.json yourself.

    2) Copy an existing test (using hard links so it won't take up much
       extra space).  This will copy all of the files so yo will have to
       delete the ones you do not want to keep.
       Note: this will give errors if DataLad was used to grab the
       data: it will complain about the files that are missing
       (because only one subject was actually downloaded).

    3) Download test data and config files from a Flywheel instance

    4) Download test data using DataLad (https://www.datalad.org/)

    5) Skip this for now (default).  You can run setup.py any time to add
       another test.

Which would you like to do? [0, 1,2,3,4,5] 
```

When running the gear for real on a Flywheel instance, it will download BIDS formatted data every time.  As mentioned earlier, `utils/bids.py` won't download data if it is already there.  This allows you to modify the data for a test and it won't be overwritten.  Using option 2) of `setup.py` will allow you to take a good set of data and modify it (being careful to consider the hard links) so that you can create tests for broken BIDS data.

## Logging

The actions of `setup.py`, `build.py`, and `run_tests.py` will be logged in "bids-app-test/tests/test/logs/init_log.txt".  Logs of running the tests you create will be placed in the "logs" directory for the test.  For example, the logs for the th test named "default" will be saved like "tests/default/logs/2019-09-30_15-49-35_log.txt".

## Next steps

Now that you have test data, you'll iterate editing, building and running tests.  Here is what your files might look like for a gear called `bids-app` where you have created two tests called "default" and "test-bad-input".:

```
	├── bids-app
	│   ├── Dockerfile
	│   ├── manifest.json
	│   ├── run.py
	│   └── utils
	│       ├── args.py
	│       ├── bids
	│       ├── dicom
	│       ├── fly
	│       ├── helpers
	│       ├── licenses
	│       └── results
	└── bids-app-test
	    ├── LICENSE
	    ├── README.md
	    ├── build.py
	    ├── run_tests.py
	    ├── setup.py
	    ├── utils
	    └── tests
		├── default                                       <-- the "default" test that you create
		│   ├── config.json
		│   ├── input
		│   ├── logs
		│   │   └── 2019-09-30_15-58-16_log.txt           <-- a log file from running the "default" test
		│   ├── output
		│   ├── src
		│   │   ├── finish.py
		│   │   └── start.py
		│   ├── test_files
		│   └── work
		├── test                                          <-- a test for bids-app-template-test
		│   ├── config.json
		│   ├── README.md
		│   ├── config.json.template
		│   ├── gear
		│   │   ├── LICENSE
		│   │   └── README.md
		│   ├── input
		│   ├── logs
		│   │   └── init_log.txt                          <-- a log file from running setup.py, build.py, and run_test.py
		│   ├── output
		│   ├── src
		│   │   ├── finish.py
		│   │   └── start.py
		│   ├── test_files
		│   └── work
		├── test-bad-input                                <-- another test that you create
		│   ├── config.json
		│   ├── input
		│   ├── logs
		│   │   └── 2019-09-31_15-58-16_log.txt           <-- a log file from running the "test_bad-input" test
		│   ├── output
		│   ├── src
		│   │   ├── finish.py
		│   │   └── start.py
		│   ├── test_files
		│   └── work
		├── ...
```

After the gear runs locally, put it on a Flywheel platform by running `fw gear upload` in the gear's directory.  To be sure that the proper python interpreter is used on the platform to execute the gear's `run.py`, set the `PATH` environment variable in `manifest.json`.  In the running gear (use `./run_tests.py -s`) `echo $PATH` will provide the information to paste into the manifest file.

As you develop new best practices for developing BIDS-App gears, be consider submitting pull requests both here and also in [bids-app-template](https://github.com/flywheel-apps/bids-app-template).

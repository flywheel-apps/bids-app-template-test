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
It's important to change to a change to a new branch because you will want to edit some of the files to make your tests work.  As you improve the way your bids-app is tested, you may also want to submit a pull request to share with the community!

Then run the initialization script inside `bids-freesurfer-test/`:

`./setup.py`

The scripts can be run from anywhere.  For instance, from within the bids-app:

```
cd bids-freesurfer
../bids-freesurfer-test/setup.py
```

That clone command saves the bids-app-template-test repository as
a test repository for the new gear.  The `setup.py` command clones
the bids-app-template repository on GitHub into a temporary location
and copies the following files into the new gear repository:

`Dockerfile   manifest.json   run.py   utils/`

The `setup.py` command uses the name you gave to the directory (e.g. "bids-freesurfer-test") to set
the new gear’s proper name inside Dockerfile and manifest.json (e.g. "bids-freesurfer").  The command
also gives you a chance to set up a test configuration but you can
choose to do that later.  After the gear is initialized the first
time you run `setup.py`, you can run `setup.py` as many times as you like to
add additional test configurations.

Now you have two directories: the new gear itself and a “-test” directory, and the real development begins.
See [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears) information on the gear specification and what needs to be in each of the files:
  * manifest.json
  * Dockerfile
  * run.py

The instructions linkded above on Building Gears are very general.  The usual `input/` and `output/` folders are available while running in the container, but in addition to that, BIDS-App gears can find BIDS formatted data in the directory `/flywheel/v0/work/bids/` (or just `work/bids/`).

develop and test the gear locally using the commands inside `<your-new-gear-name>-test/`:

 * `./setup.py` to create a new test configuration,
 * `./build.py` to build the container, and
 * `./run.py` to run the default test or `run.py testname` to run a test called “testname".

`./setup.py` will create test configurations in the `tests/` sub-folder of `<your-new-gear-name>-test/`.  The name of the sub-folder is the name of the test.  Test folders contain these:
```config.json   input/      logs/       output/     src/        test_files/ work/```
All of these items will be mounted inside the running Docker container by the `run.py` script except for `test_files/`.

As you develop new best practices for developing BIDS-App gears, be sure to add them both here and also in [bids-app-template](https://github.com/flywheel-apps/bids-app-template).

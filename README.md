# bids-app-template-test
Test environment for bids-app-template 

To create a bids-app gear, *do not* just clone this repository, follow these steps.

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
  * Clone your new project locally: press "Clone or download" and then, e.g. `git clone git@github.com:flywheel-apps/bids-fmriprep.git`

## Clone this repository using a different name

Clone this testing template in the same directory and be sure to use the name of the new
gear repository created above **with “-test” appended** to the end.  For example:

`git clone git@github.com:flywheel-apps/bids-app-template-test.git  bids-freesurfer-test`

Then run the initialization script like:

`cd bids-freesurfer-test ; ./setup.py`

That clone command saves the bids-app-template-test repository as
a test repository for the new gear.  The `setup.py` command clones
the bids-app-template repository on GitHub into a temporary location
and copies the following files into the new gear repository:

`Dockerfile   manifest.json   run.py   utils/`

The setup.py command uses the name you gave to the directory (bids-freesurfer-test) to set
the new gear’s proper name in Dockerfile and manifest.json.  The command
also gives you a chance to set up a test configuration but you can
choose to do that later.  After the gear is initialized the first
time you run `setup.py`, you can run `setup.py` as many times as you like to
add additional test configurations.

Now you have two directories: the mew gear itself and a “-test” directory, and the real development begins.
See [Building Gears](https://docs.flywheel.io/hc/en-us/articles/360015513653-Building-Gears) information on the gear specification and what needs to be in each of the files:
  * manifest.json
  * Dockerfile
  * run.py
  
Develop and test the gear locally with the commands inside `\<your-new-gear-name\-test/`:

`./setup.py` to create a new test configurations,
`./build.py` to build the container, 
`./run.py` to run the default test or `run.py testname` command to run a test called “testname".

`./setup.py` will create test configurations, starting with "default" in `\<your-new-gear-name\-test/tests/`.


As you develop new best practices for developing BIDS-App gears, be sure to add them both here and also in [bids-app-template](https://github.com/flywheel-apps/bids-app-template).

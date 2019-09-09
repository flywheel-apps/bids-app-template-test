# bids-app-template-test
Test environment for bids-app-template 

To create a bids-app gear, *do not* just clone this repository, follow these steps.

## Identify BIDS compatible open source code

* See https://github.com/BIDS-Apps.  Maybe what you want is already there.
* Note the open source license.  It need to be commercially friendly.

## Create GitHub Project

On https://github.com/flywheel-apps, hit the "new" button. 
  *  Create new repository with owner "flywheel-apps" and give it a lower-case-with-dashes name like "bids-freesurfer".  
  * Give it a description like, "Gear that runs freesurfer on BIDS-curated data".  
  * Keep it private for now, not that nobody should see it, but there's no need for a lot of intrusive questions about it before it is even released for the first time.  
  * Check the "Initialize this repository with a README", add a .gitignore for Python, and set the license to the same license as the open source code.
  * Press the "Create Repository" button.

## Clone this repository using a different name

Clone this testing template, but be sure to use the name of the new
gear repository created above with “-test” appended to the end, and
then run the initialization script.  For example:

`git clone git@github.com:flywheel-apps/bids-app-template-test.git  bids-freesurfer`

`./bids-mriqc-test/setup.py`

That first command saves the bids-app-template-test repository as
a new test repository for the gear.  The setup.py command clones
the bids-app-template repository on GitHub into a temporary location
and copies the following files into the gear repository you cloned
earlier:

`Dockerfile   manifest.json   run.py   utils/`

The setup.py command uses the name you gave to the directory to set
the gear’s proper name in Dockerfile and manifest.json.  The command
also gives you a chance to set up a test configuration but you can
choose to do it later.  After the gear is initialized the first
time you run setup.py, you can run it as many times as you like to
add a test configuration.

Now you have two directories: the gear itself and a “-test” directory.

Test the gear locally using the test configurations in \<you-gear-name\-test
directory by using:

`build.py` to build the container, 
`run.py` to run the default test or `run.py testname` command to run a test called “testname”, and
`setup.py` to create a new test.

**jupyter-instructortools**

This adds a menu to the Jupyter menubar that automates some useful tasks an instructor might
want to do while building a notebook template for an assignment

**Current Features:**

* Menu activated by a python command.
* Menu items to protect/unprotect selected cells. Protected cells cannot be editted or deleted
by the user. This is a good way to prevent instructions and example code from being damaged
by students.
* Menu item for creating a data input table.
    * Table column and row labels can be locked once set.
    * Number of rows and columns must be chosen on initial creation.
    * Table will survive deletion of all cell output data.
    * Default setting is to make the code cell that creates the table uneditable and
undeletable.
    * Table creation code will work without this package installed in the Jupyter
kernel. Tables are viewable, but not editable in a plain vanilla Jupyter install.
    * This uses the `jupyter-datainputtable` package.
* Menu item to delete instructor tools from a notebook before making the worksheet
available.

**Installation**

Installation using pip into a virtual environment is recommended.

_Production_

1. If not installed, install pipenv:`$ pip3 install --user pipenv`. You may
need to add `~/.local/bin` to your `PATH` to make `pipenv`
available in your command shell. More discussion: 
[The Hitchhiker's Guide to Python](https://docs.python-guide.org/dev/virtualenvs/).
1. Navigate to the directory where this package will be installed.
1. Start a shell in the environment `$ pipenv shell`.
1. Install using pip.
    1. `$ pip install jupyter-instructortools`. This will install Jupyter into the same virtual
    environment if you do not already have it on your machine. If Jupyter is already
    installed the virtual environment will use the existing installation. This takes
    a long time on a Raspberry Pi. It will not run on a 3B+ without at least 1 GB of
    swap. See: [Build Jupyter on a Pi](https://www.uwosh.edu/facstaff/gutow/computer-and-programming-how-tos/installing-jupyter-on-raspberrian).
    1. Still within the environment shell test this by starting jupyter
`$ jupyter notebook`. Jupyter should launch in your browser.
        1. Open a new notebook using the default (Python 3) kernel.
        1. In the first cell import the InstructorTools module:
            `from InstructorTools import *`
        1. The `InstructorTools` menu should be added to the Jupyter menu bar.
1. _Optional_ You can make this environment available to an alternate Jupyter install as a special kernel when you are the user.
    1. Make sure you are running in your virtual environment `$ pipenv shell` in the directory for  virtual
    environment will do that.
    1. Issue the command to add this as a kernel to your personal space: 
    `$ python -m ipykernel install --user --name=<name-you-want-for-kernel>`.
    1. More information is available in the Jupyter/Ipython documentation. A simple tutorial from Nikolai Jankiev
    (_Parametric Thoughts_) can be found [here](https://janakiev.com/til/jupyter-virtual-envs/). 
    
_Development_

Simply replace `$ pip install jupyter-instructortools` with `$ pip install -e jupyter-instructortools` in the _Production_ instructions.

**Issues or comments**

[JupyterPhysSciLab/jupyter-instructortools](https://github.com/JupyterPhysSciLab/jupyter-instructortools)
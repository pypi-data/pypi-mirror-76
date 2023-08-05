# PyProjectManager
Python project manager smooths workflow to create, install and maintain python projects

####Requirements
The package is tested and working with Click 7.1.1. Other required packages are specified in setup files.

###Method of installation

To install Python Project manager from PyPi run this command in terminal

```
pip install pyPman
```

Or

To clone it from github : 

```
git clone https://github.com/sunilk-n/PyProjectManager.git
```
Then use python directly in the main folder
```
python setup.py sdist
```
To get the ".gz" file

###Complete help information about `init`:

* pyPm init : Starts project initialization
* `pyPm init [-p <projectName>]` : Starts project initialization setting projectName as provided
* `pyPm init [-p <projectName> -d <dependancy>]` : Adds 3rd party dependancy modules to the project
    - Usage: `pyPm init -p <projectName> -d <moduleName> [<module_version>]`
        * Ex: `pyPm init -p PyProjectManager -d click` (or)
        * Ex: `pyPm init -p PyProjectManager -d click 7.1.1`
* `pyPm init [-p <projectName> -m <module>]` : Adds user defined module package to the project
    - Usage: `pyPm init -p <projectName> -m <moduleName>`
        * Ex: `pyPm init -p PyProjectManager -m testModule`


###Complete help information about `install`:
* `pyPm install [-p <projectName>]` : Starts installing project to the current directory
    - Usage: `pyPm install -p <projectName>`
        * Ex: `pyPm install -p PyProjectManager`
# mrxcavator

mrxcavator is a CLI client implementation for the service [CRXcavator.io](https://crxcavator.io) being built in relation to Dakota State University's course CSC-842, "Security Tool Development."

## Overview

The following overview was taken from the service's [about](https://crxcavator.io/docs#/README) page:
> CRXcavator automatically scans the entire Chrome Web Store every 3 hours and produces a quantified risk score for each Chrome Extension based on several factors. These factors include permissions, inclusion of vulnerable third party javascript libraries, weak content security policies, missing details from the Chrome Web Store description, and more. Organizations can use this tool to assess the Chrome Extensions they have installed and to move towards implementing explicit allow (whitelisting) for their organization.

The development of this CLI tool will have five "releases" that relate to the course submission deadlines. As releases are produced, this README.md will be updated to share the highlights. At a high-level, this tool will provide some amount of feature parity to the CRXcavator web experience.

1. Release 1 - 05/24/2020
    * Initial creation of mrxcavator, including this README, LICENSE, and requirements.txt
    * Added support to show the installed version (-v or --version)
    * Added support to submit an extension by id (-s or --submit)
    * Added support to request an extension report by id (-r or --report)
    * Generated application documentation (docs/mrxcavator.html) using `pdoc`
    * Validated `flake8`, `mypy`, and `black` run cleanly against the application
    * Commented blocks leverage Google's Python Style Guide for docstrings
    * Functions leverage PEP 484 type hinting to improve documentation & linting
2. Release 2 - 06/07/2020
    * Generated new documentation to reflect changes to functionality
    * Integration of ConfigParser to enable user controllable configuration
    * Support for identifier exclusions for extensions that Chrome bundles in
    * Added API key support to HTTP calls to support future functionality
    * The CRXcavator API base URI is no longer hardcoded; now user configurable
    * Added API key and API URI test-call functionality to validate settings
    * Added locally-installed extension discovery -- hardcoded for right now
    * An extension report now shows the version count that CRXcavator tracks
    * Supports the mass submission of extensions that are installed locally
3. Release 3 - 06/21/2020
4. Release 4 - 07/05/2020
5. Release 5 - 07/19/2020

## Engineering Approach

### [flake8](https://gitlab.com/pycqa/flake8)
>`flake8` is a command-line utility for enforcing style consistency across Python projects. By default it includes lint checks provided by the PyFlakes project, PEP-0008 inspired style checks provided by the PyCodeStyle project, and McCabe complexity checking provided by the McCabe project.

### [mypy](https://github.com/python/mypy)
> `mypy` is an optional static type checker for Python. You can add type hints (PEP 484) to your Python programs, and use mypy to type check them statically. Find bugs in your programs without even running them!

### [pdoc](https://github.com/pdoc3/pdoc)
> `pdoc` the perfect documentation generator for small-to-medium-sized, tidy Python projects. It generates documentation simply from your project's already-existing public modules' and objects' docstrings, like sphinx-apidoc or sphinx.ext.autodoc, but without the hassle of these tools.

### [black](https://github.com/psf/black)
> `black` is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.

### [PEP 484](https://www.python.org/dev/peps/pep-0484/)
> PEP 3107 introduced syntax for function annotations, but the semantics were deliberately left undefined.  There has now been enough 3rd party usage for static type analysis that the community would benefit from a standard vocabulary and baseline tools within the standard library. This PEP introduces a provisional module to provide these standard definitions and tools, along with some conventions for situations where annotations are not available.

### [Google's Python Style Guide](http://google.github.io/styleguide/pyguide.html)
> Python is the main dynamic language used at Google. This style guide is a list of dos and don’ts for Python programs.

**Note:** The use of this guide is primarily for [docstring formatting](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings), which complements type hints nicely.

### [argparse](https://docs.python.org/3.6/library/argparse.html)
> The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments.

## Using mrxcavator

### Installation
1. Python >=3.6 is required for application compatibility (e.g. `brew install python` on macOS)
2. Execute `git clone https://github.com/mstanislav/mrxcavator.git` to download the repository
3. Execute `cd mrxcavator` to enter the application's root folder
4. Execute `pip3 install -r requirements.txt` to install Python dependencies

### Help Output
```
➜  python3 mrxcavator.py
usage: mrxcavator.py [-h] [-s id] [-r id] [-v]

optional arguments:
  -h, --help          show this help message and exit
  -s id, --submit id  submit an extension
  -r id, --report id  get an extension's report
  -v, --version       show program's version number and exit
```

### Submit an Extension
```
➜  python3 mrxcavator.py --submit hdokiejnpimakedhajhdlcegeplioahd

        You've successfully submitted hdokiejnpimakedhajhdlcegeplioahd to CRXcavator.
```

### Get an Extension's Report
```
➜  python3 mrxcavator.py --report hdokiejnpimakedhajhdlcegeplioahd

Overview
================================================================================
    Extension Name: LastPass: Free Password Manager
    Extension ID:   hdokiejnpimakedhajhdlcegeplioahd
    Newest Version: 4.48.0.2 (2020-05-13)
    Store Rating:   4.5433135 stars

Risk
================================================================================
    CSP Policy:     69
    RetireJS:       150
    Web Store:      1

    Permissions:
      >Required:    110
      >Optional:    25

    ** Risk Score:  355 **

```

### Get mrxcavator's Version
```
➜  python3 mrxcavator.py --version
v0.1
```

# mrxcavator

mrxcavator is a CLI implementation for [CRXCavator](https://crxcavator.io) being built as part of DSU's CSC-842, "Security Tool Development" course.

## Overview

The following overview was taken from the project's [about](https://crxcavator.io/docs#/README) page:
> CRXcavator automatically scans the entire Chrome Web Store every 3 hours and produces a quantified risk score for each Chrome Extension based on several factors. These factors include permissions, inclusion of vulnerable third party javascript libraries, weak content security policies, missing details from the Chrome Web Store description, and more. Organizations can use this tool to assess the Chrome Extensions they have installed and to move towards implementing explicit allow (whitelisting) for their organization.

The development of this tool will have five "releases" that related to the course's submission deadlines. As tool releases are produced, this README.md will be updated to share some highlights of what was contributed during that release.

1. Release 1 - 05/24
  * Initial creation of mrxcavator, including this README file
  * Added support to show the version of mrxcavator (-v or --version)
  * Added support to submit an extension by id (-s or --submit)
  * Added support to request an extension report by id (-r or --report)
  * Validated `flake8` and `mypy` run cleanly against the application
  * Commented functions supporting both PEP 484 and Google'd Python Style Guide
  * Generated application documentation (docs/mrxcavator.html) using `pdoc3`
2. Release 2 - 06/07
3. Release 3 - 06/21
4. Release 4 - 07/05
5. Release 5 - 07/19

In general, the tool hopes to provide an easy-to-use interface to submit extensions to CRXcavator, gather results, cache results, provide basic reporting, and likely leverage some CLI-visualization libraries to improve user experience. At this time, no public CLI tool exists for this service, so I feel that the contribution to the community is a good focus of effort.

This application passes both `flake8` and `mypy` code quality analysis.

## Using mrxcavator

## Installation
1. You must be running a Python release >=3.6 for application compatibility
2. Execute `git clone https://github.com/mstanislav/mrxcavator.git` to get it
3. Execute `cd mrxcavator` to enter the application's root folder
4. Execute `pip3 install -r requirements.txt` to install Python dependencies

### Application Help
```
➜  python3 mrxcavator.py
usage: mrxcavator.py [-h] [-s id] [-r id] [-v]

optional arguments:
  -h, --help          show this help message and exit
  -s id, --submit id  submit extension
  -r id, --report id  extension report
  -v, --version       show program's version number and exit
```

### Get mrxcavator's Version
```
➜  python3 mrxcavator.py --version
mrxcavator v0.1
```

### Submit an Extension
```
➜  python3 mrxcavator.py --submit hdokiejnpimakedhajhdlcegeplioahd

        You've successfully submitted hdokiejnpimakedhajhdlcegeplioahd to CRXcavator.
```

### Get an Extension Report
```
➜  python3 mrxcavator.py --report hdokiejnpimakedhajhdlcegeplioahd

Overview
================================================================================
    Extension Name: LastPass: Free Password Manager
    Extension ID:   hdokiejnpimakedhajhdlcegeplioahd
    Newest Version: 4.18.0.4 (2018-10-09)
    Store Rating:   4.594451 stars

Risk
================================================================================
    CSP Policy:     86
    RetireJS:       100
    Web Store:      6

    Permissions:
      >Required:    110
      >Optional:    85

    ** Risk Score:  387 **
```

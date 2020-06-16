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
➜  python3 mrxcavator.py -h
usage: mrxcavator.py [-h] [-c path] [--extension_path directory] [-s [id]]
                     [--submit_all] [-r [id]] [--export file] [--report_all]
                     [--crxcavator_key key] [--crxcavator_uri uri]
                     [--test_crxcavator_key] [--test_crxcavator_uri] [-e] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c path, --config path
                        specify a config file path
  --extension_path directory
                        set path to local Chrome extensions
  -s [id], --submit [id]
                        submit an extension
  --submit_all          submit all installed extensions
  -r [id], --report [id]
                        get an extension's report
  --export file         export result to a specific file
  --report_all          retrieve a report for all installed extensions
  --crxcavator_key key  set CRXcavator API key
  --crxcavator_uri uri  set CRXcavator API URI
  --test_crxcavator_key
                        test configured CRXcavator API key
  --test_crxcavator_uri
                        test configured CRXcavator API URI
  -e, --extensions      list installed extensions
  -v, --version         show program's version number and exit
```

### Submit an Extension
If no extension identifier is passed to the flag, a list of options of locally installed extensions will be given to select from.
```
➜  python3 mrxcavator.py -s hdokiejnpimakedhajhdlcegeplioahd

	You've successfully submitted hdokiejnpimakedhajhdlcegeplioahd.
```

### Submit All Locally Installed Extensions
```
➜  python3 mrxcavator.py --submit_all

Submitting extensions found in ~/Library/Application Support/Google/Chrome/Default/Extensions/

100%|████████████████████████████████████████████████████████████████████████

Successful:
  > Application Launcher for Drive (by Google)
  > Docs
  > Gmail
  > Google Docs Offline
  > Google Drive
  > Google Keep Chrome Extension
  > Save to Google Drive
  > Sheets
  > Slides
  > YouTube
  > Zoom
```

### Get an Extension's Report
If no extension identifier is passed to the flag, a list of options of locally installed extensions will be given to select from.
```
➜  python3 mrxcavator.py -r hdokiejnpimakedhajhdlcegeplioahd

Overview
================================================================================
        Extension Name: LastPass: Free Password Manager
        Extension ID:   hdokiejnpimakedhajhdlcegeplioahd
        Newest Version: 4.49.0.3 (2020-06-03)
        Versions Known: 41
        Store Rating:   4.54 stars

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

### Save an Extension's Report to a File
```
➜   python3 mrxcavator.py -r hdokiejnpimakedhajhdlcegeplioahd --export lastpass.txt

Overview
================================================================================
        Extension Name: LastPass: Free Password Manager
        Extension ID:   hdokiejnpimakedhajhdlcegeplioahd
        Newest Version: 4.49.0.3 (2020-06-03)
        Versions Known: 41
        Store Rating:   4.54 stars

Risk
================================================================================
        CSP Policy:     69
        RetireJS:       150
        Web Store:      1

        Permissions:
          >Required:    110
          >Optional:    25

        ** Risk Score:  355 **


>> Report saved in reports/lastpass.txt <<

➜  cat reports/lastpass.txt
Overview
================================================================================
        Extension Name: LastPass: Free Password Manager
        Extension ID:   hdokiejnpimakedhajhdlcegeplioahd
        Newest Version: 4.49.0.3 (2020-06-03)
        Versions Known: 41
        Store Rating:   4.54 stars

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

### Get Reports For All Locally Installed Extensions
```
➜  python3 mrxcavator.py --report_all

Retrieving extension report(s)...


Overview
================================================================================
        Extension Name: Google Docs Offline
        Extension ID:   ghbmnnjooekpmoecnnnilnnbdlolhkhi
        Newest Version: 1.9.1 (2020-03-04)
        Versions Known: 5
        Store Rating:   2.87 stars

Risk
================================================================================
        CSP Policy:     377
        Web Store:      6

        Permissions:
          >Required:    40

        ** Risk Score:  423 **

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
================================================================================
        Extension Name: Gmail
        Extension ID:   pjkljhegncpnkpknbcohdijeoejaedia
        Newest Version: 8.2 (2019-03-26)
        Versions Known: 2
        Store Rating:   4.53 stars

Risk
================================================================================
        Web Store:      10

        Permissions:
          >Required:    5

        ** Risk Score:  15 **

[...snip...]
```

### List Locally Installed Extensions
```
➜  python3 mrxcavator.py -e

Locally Installed Chrome Extensions:
------------------------------------

* Google Docs Offline
  - Version:	1.11.0
  - Identifier: ghbmnnjooekpmoecnnnilnnbdlolhkhi

* Chrome Media Router
  - Version:	8320.407.0.1
  - Identifier: pkedcjkdefgpdelpbcmbmeomcjbeemfm

* Gmail
  - Version:	8.2
  - Identifier: pjkljhegncpnkpknbcohdijeoejaedia

* Google Drive
  - Version:	14.2
  - Identifier: apdfllckaahabafndbhieahigkjlhalf

* Application Launcher for Drive (by Google)
  - Version:	3.2
  - Identifier: lmjegmlicamnimmfhcmpkclmigmmcbeh

* Slides
  - Version:	0.10
  - Identifier: aapocclcgogkmnckokdopfmhonfmgoek

* Docs
  - Version:	0.10
  - Identifier: aohghmighlieiainnegkcijnfilokake

* Google Keep Chrome Extension
  - Version:	4.20222.540.1
  - Identifier: lpcaedmchfhocbbapmcbpinfpgnhiddi

* Chrome Web Store Payments
  - Version:	1.0.0.5
  - Identifier: nmmhkkegccagdldgiimedpiccmgmieda

* Save to Google Drive
  - Version:	2.1.1
  - Identifier: gmbmikajjgmnabiglmofipeabaddhgne

* YouTube
  - Version:	4.2.8
  - Identifier: blpcfgokakmgnkcojhhkbfbldkacnbeo

* Sheets
  - Version:	1.2
  - Identifier: felcaaldnbdncclmgdcncolpebgiejap
```

### Set the CRXcavator API URI Value
```
➜  python3 mrxcavator.py --crxcavator_uri https://api.crxcavator.io/v1

	The CRXcavator API URI was set successfully!
```

### Set the CRXcavator API Key Value
```
➜  python3 mrxcavator.py --crxcavator_key DEnDIwspwQkiMYZzuFbHOHUqDOpSaDIw

	The CRXcavator API key was set successfully!
```

### Test Current CRXcavator API Base URI Setting
```
➜  python3 mrxcavator.py --test_crxcavator_uri

	The CRXcavator API URI was successfully tested!
```

### Test Current CRXcavator API Key Setting
```
➜  python3 mrxcavator.py --test_crxcavator_key

	The CRXcavator API key was successfully tested!
```

### Get mrxcavator's Version
```
➜  python3 mrxcavator.py --version
v0.3
```

### Example config.ini Contents
```
➜  cat config.ini
[DEFAULT]
crxcavator_api_uri = https://api.crxcavator.io/v1
crxcavator_api_key =
extension_path = ~/Library/Application Support/Google/Chrome/Default/Extensions/

[custom]
```

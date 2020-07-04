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
    * Added --config (-c) that lets a user to specify a configuration filename
    * Added --extension_path that lets a user specify a path to their locally installed extensions
    * Added --export, which can be used with --report to specify a filename where a report will be saved
    * Used `tqdm` to provide draw a progress bar for extension mass submission
    * Added --report_all to generate an extension report summary for all locally installed extensions
    * `PyInquirer` now provides a menu of extensions when a report/submit is called, but no identifier is given
    * Bug Fix: Removed the extension version sub-release from the folder name
    * Bug Fix: --test_crxcavator_key no longer breaks when an API key is not set
    * Bug Fix: An extension report summary now gracefully handles missing sections of content
    * Bug Fix: The "Star Rating" had entirely too much specificity; now it is rounded to two decimal places
    * Bug Fix: An incorrect report identifier no longer returns a broken summary
4. Release 4 - 07/05/2020
    * The --report_all feature now supports also exporting each to a file
    * Using --export now writes to a filename of extension_id.txt if one isn't given
    * A VirusTotal API Key can now be configured and tested for functionality
    * The --extensions command now shows results in a well-formatted table using `termtables`
    * The "help" output now uses argparse "groups" to increase readability
    * A new --graph (-g) command will chart out an extension's risk score over time using `asciichartpy`
    * Changed the overall extension report summary format
    * Added CSP attribute scoring to the report summary
    * Added RetireJS per-rating scores to the report summary
    * The project now is configured to work with `Poetry` and published to PyPI
    * Bug Fix: Gracefully handle a user cancelling a `PyInquirer` prompt
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
usage: mrxcavator.py [-c path] [--extension_path path] [--crxcavator_key key]
                     [--crxcavator_uri uri] [--virustotal_key key]
                     [--test_crxcavator_key] [--test_crxcavator_uri]
                     [--test_virustotal_key] [-s [id]] [--submit_all]
                     [-r [id]] [--report_all] [--export [file]] [-e] [-g [id]]
                     [-v] [-h]

Features:
  -s [id], --submit [id]
                        submit an extension
  --submit_all          submit all installed extensions
  -r [id], --report [id]
                        get an extension's report
  --report_all          retrieve a report for all installed extensions
  --export [file]       export result to a specific file
  -e, --extensions      list installed extensions
  -g [id], --graph [id]
                        get a graph of an extension's risk

Set Configuration:
  -c path, --config path
                        specify a config file path
  --extension_path path
                        set path to local Chrome extensions
  --crxcavator_key key  set CRXcavator API key
  --crxcavator_uri uri  set CRXcavator API URI
  --virustotal_key key  set VirusTotal API key

Test Configuration:
  --test_crxcavator_key
                        test CRXcavator API key
  --test_crxcavator_uri
                        test CRXcavator API URI
  --test_virustotal_key
                        test VirusTotal API key

Miscellaneous:
  -v, --version         show program's version number and exit
  -h, --help            show program's help information and exit
```

### Submit an Extension
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
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
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
```
➜  python3 mrxcavator.py -r bmnlcjabgnpnenekpadlanbbkooimhnj

Extension Overview
============================================================
  Extension Name:	Honey
  Extension ID:		bmnlcjabgnpnenekpadlanbbkooimhnj

  Newest Version:	12.3.0 (2020-06-26)
  Versions Known:	42
  Store Rating:		4.84 stars

  Total Risk Score:	657


Content Security Policy
============================================================
  386	Total
------------------------------------------------------------
  25	child-src
  25	connect-src
  25	font-src
  25	form-action
  25	frame-ancestors
  25	frame-src
  25	img-src
  25	manifest-src
  25	media-src
  1	object-src
  25	plugin-types
  25	sandbox
  10	script-src
  25	strict-dynamic
  25	style-src
  25	upgrade-insecure-requests
  25	worker-src


RetireJS
============================================================
  130	Total
------------------------------------------------------------
  0	Low
  40	Medium
  90	High
  0	Critical


Web Store
============================================================
  0	Total
------------------------------------------------------------


Permissions
============================================================
  135	Total
------------------------------------------------------------
  135	Required
  0	Optional
```

### Save an Extension's Report to a File
```
➜   python3 mrxcavator.py -r hdokiejnpimakedhajhdlcegeplioahd --export lastpass.txt

Extension Overview
============================================================
  Extension Name:	LastPass: Free Password Manager
  Extension ID:		hdokiejnpimakedhajhdlcegeplioahd

  Newest Version:	4.51.0.1 (2020-07-02)
  Versions Known:	43
  Store Rating:		4.54 stars

  Total Risk Score:	354


Content Security Policy
============================================================
  69	Total
------------------------------------------------------------
  1	child-src
  37	connect-src
  1	font-src
  1	form-action
  1	frame-ancestors
  8	frame-src
  4	img-src
  1	manifest-src
  1	media-src
  1	object-src
  1	plugin-types
  1	sandbox
  1	script-src
  1	strict-dynamic
  7	style-src
  1	upgrade-insecure-requests
  1	worker-src


RetireJS
============================================================
  150	Total
------------------------------------------------------------
  20	Low
  40	Medium
  90	High
  0	Critical


Web Store
============================================================
  0	Total
------------------------------------------------------------


Permissions
============================================================
  135	Total
------------------------------------------------------------
  110	Required
  25	Optional


>> Report saved in reports/lastpass.txt <<
```

### Get Reports For All Locally Installed Extensions
```
➜  python3 mrxcavator.py --report_all

Retrieving extension report(s)...


Extension Overview
============================================================
  Extension Name:	Google Docs Offline
  Extension ID:		ghbmnnjooekpmoecnnnilnnbdlolhkhi

  Newest Version:	1.9.1 (2020-03-04)
  Versions Known:	5
  Store Rating:		2.87 stars

  Total Risk Score:	423


Content Security Policy
============================================================
  377	Total
------------------------------------------------------------
  25	child-src
  25	connect-src
  25	font-src
  25	form-action
  25	frame-ancestors
  25	frame-src
  25	img-src
  25	manifest-src
  25	media-src
  1	object-src
  25	plugin-types
  25	sandbox
  1	script-src
  25	strict-dynamic
  25	style-src
  25	upgrade-insecure-requests
  25	worker-src


Web Store
============================================================
  6	Total
------------------------------------------------------------
  1	Address
  1	Email
  2	Last Updated
  2	Rating


Permissions
============================================================
  40	Total
------------------------------------------------------------
  40	Required
  0	Optional

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extension Overview
============================================================
  Extension Name:	Honey
  Extension ID:		bmnlcjabgnpnenekpadlanbbkooimhnj

  Newest Version:	12.3.0 (2020-06-26)
  Versions Known:	42
  Store Rating:		4.84 stars

  Total Risk Score:	657


Content Security Policy
============================================================
  386	Total
------------------------------------------------------------
  25	child-src
  25	connect-src
  25	font-src
  25	form-action
  25	frame-ancestors
  25	frame-src
  25	img-src
  25	manifest-src
  25	media-src
  1	object-src
  25	plugin-types
  25	sandbox
  10	script-src
  25	strict-dynamic
  25	style-src
  25	upgrade-insecure-requests
  25	worker-src


RetireJS
============================================================
  130	Total
------------------------------------------------------------
  0	Low
  40	Medium
  90	High
  0	Critical


Web Store
============================================================
  0	Total
------------------------------------------------------------


Permissions
============================================================
  135	Total
------------------------------------------------------------
  135	Required
  0	Optional

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[...snip...]
```

### List Locally Installed Extensions
```
➜  python3 mrxcavator.py -e

Extensions Found in ~/Library/Application Support/Google/Chrome/Default/Extensions/
┌────────────────────────────────────────────┬───────────────┬──────────────────────────────────┐
│ Name                                       │ Version       │ Identifier                       │
╞════════════════════════════════════════════╪═══════════════╪══════════════════════════════════╡
│ Google Docs Offline                        │ 1.11.0        │ ghbmnnjooekpmoecnnnilnnbdlolhkhi │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Honey                                      │ 12.2.1        │ bmnlcjabgnpnenekpadlanbbkooimhnj │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Gmail                                      │ 8.2           │ pjkljhegncpnkpknbcohdijeoejaedia │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Bitwarden - Free Password Manager          │ 1.45.0        │ nngceckbapebfimnlniiiahkandclblb │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Google Drive                               │ 14.2          │ apdfllckaahabafndbhieahigkjlhalf │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Application Launcher for Drive (by Google) │ 3.2           │ lmjegmlicamnimmfhcmpkclmigmmcbeh │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Slides                                     │ 0.10          │ aapocclcgogkmnckokdopfmhonfmgoek │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Cisco Webex Extension                      │ 1.9.0         │ jlhmfgmfgeifomenelglieieghnjghma │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Docs                                       │ 0.10          │ aohghmighlieiainnegkcijnfilokake │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Google Keep Chrome Extension               │ 4.20265.788.1 │ lpcaedmchfhocbbapmcbpinfpgnhiddi │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Zoom                                       │ 5.0.4169.628  │ hmbjbjdpkobdjplfobhljndfdfdipjhg │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Save to Pocket                             │ 3.0.6.8       │ niloccemoadcdkdjlinkgdfekeahmflj │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Save to Google Drive                       │ 2.1.1         │ gmbmikajjgmnabiglmofipeabaddhgne │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ YouTube                                    │ 4.2.8         │ blpcfgokakmgnkcojhhkbfbldkacnbeo │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Sheets                                     │ 1.2           │ felcaaldnbdncclmgdcncolpebgiejap │
└────────────────────────────────────────────┴───────────────┴──────────────────────────────────┘
```

### Show a Graph of an Extension's Risk Score Over Time
```
➜  python3 mrxcavator.py -g bmnlcjabgnpnenekpadlanbbkooimhnj
     668 ┤
     655 ┤                                     ╭╮
     641 ┤                                     │╰──
     628 ┤                 ╭╮                  │
     614 ┤                 ││               ╭──╯
     601 ┤     ╭─╮╭─╮      ││        ╭──────╯
     587 ┤     │ ││ │      ││        │
     574 ┤     │ ││ │      │╰─╮      │
     560 ┤     │ ││ │      │  │      │
     547 ┤     │ ││ │      │  │      │
     533 ┤     │ ││ │      │  │      │
     520 ┼─────╯ ╰╯ ╰──────╯  ╰──────╯
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

### Set the VirusTotal API Key Value
```
➜  python3 mrxcavator.py --virustotal_key d42d8fb60105539a632d209ed35a42515722a79be2c39f5635d3790b25433acc

	The VirusTotal API key was set successfully!
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

### Test Current VirusTotal API Key Setting
```
➜  python3 mrxcavator.py  --test_virustotal_key

	The VirusTotal API key was successfully tested!
```

### Use a Custom Configuration File
```
➜  python3 mrxcavator.py --config testing.ini

	testing.ini does not exist, or is corrupted. Creating it...

➜  cat testing.ini
[DEFAULT]
crxcavator_api_uri = https://api.crxcavator.io/v1
crxcavator_api_key =
virustotal_api_key =
extension_path = ~/Library/Application Support/Google/Chrome/Default/Extensions/

[custom]
```

### Get mrxcavator's Version
```
➜  python3 mrxcavator.py --version
v0.4
```

### Example config.ini Contents
```
➜  cat config.ini
[DEFAULT]
crxcavator_api_uri = https://api.crxcavator.io/v1
crxcavator_api_key =
virustotal_api_key =
extension_path = ~/Library/Application Support/Google/Chrome/Default/Extensions/

[custom]
```

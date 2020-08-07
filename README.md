# mrxcavator

mrxcavator is a CLI client implementation for the service [CRXcavator.io](https://crxcavator.io).

## Overview

The following overview was taken from the service's [about](https://crxcavator.io/docs#/README) page:
> CRXcavator automatically scans the entire Chrome Web Store every 3 hours and produces a quantified risk score for each Chrome Extension based on several factors. These factors include permissions, inclusion of vulnerable third party javascript libraries, weak content security policies, missing details from the Chrome Web Store description, and more. Organizations can use this tool to assess the Chrome Extensions they have installed and to move towards implementing explicit allow (whitelisting) for their organization.

## Using mrxcavator

### Installation
**Python >=3.6.1 is required for application compatibility.**

#### PyPI
* Execute `pip3 install mrxcavator`
* Execute `mrxcavator`

#### Git
* Execute `git clone https://github.com/mstanislav/mrxcavator.git` to download the repository
* Execute `cd mrxcavator` to enter the application's root folder
* Execute `pip3 install -r requirements.txt` to install Python dependencies
* Execute `python3 mrxcavator.py`

### Help Output
```
➜  mrxcavator -h
usage: mrxcavator    [-c filename] [--extension_path path]
                     [--crxcavator_key key] [--crxcavator_uri uri]
                     [--virustotal_key key] [--test_crxcavator_key]
                     [--test_crxcavator_uri] [--test_virustotal_key] [-s [id]]
                     [--submit_all] [-r [id]] [--report_all]
                     [--report_all_table] [--export [filename]]
                     [--input [filename]] [-e] [-g [id]] [-vt [id]] [-v] [-h]

Features:
  -s [id], --submit [id]
                        submit an extension
  --submit_all          submit all installed extensions
  -r [id], --report [id]
                        get an extension's report
  --report_all          retrieve a report for all installed extensions
  --report_all_table    retrieve a table of details for installed extensions
  --export [filename]   export a report to a specific filename
  --input [filename]    load a specific filename for extension identifiers
  -e, --extensions      list installed extensions
  -g [id], --graph [id]
                        get a graph of an extension's risk
  -vt [id], --virustotal [id]
                        get VirusTotal data for an extension's external calls

Set Configuration:
  -c filename, --config filename
                        specify a configuration filename
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
➜  mrxcavator -s hdokiejnpimakedhajhdlcegeplioahd

	You've successfully submitted hdokiejnpimakedhajhdlcegeplioahd.
```

### Submit All Locally Installed Extensions
This feature supports `--input [filename]` to load extension identifiers from a text file.
```
➜  mrxcavator --submit_all

Submitting extensions found in ~/Library/Application Support/Google/Chrome/Default/Extensions/

100%|████████████████████████████████████████████████████████████████████████

Successful:
  > Application Launcher for Drive (by Google)
  > Bitwarden - Free Password Manager
  > Cisco Webex Extension
  > Gmail
  > Google Docs Offline
  > Google Drive
  > Google Keep Chrome Extension
  > Honey
  > Save to Google Drive
  > Save to Pocket
  > YouTube
  > Zoom
```

### Get an Extension's Report
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
```
➜  mrxcavator -r bmnlcjabgnpnenekpadlanbbkooimhnj

Extension Overview
============================================================
  Extension Name:       Honey
  Extension ID:         bmnlcjabgnpnenekpadlanbbkooimhnj
  Web Site:             https://www.joinhoney.com

  Newest Version:       12.4.0 (2020-07-23)
  Versions Known:       45
  Store Rating:         4.84 stars

  Total Risk Score:     604


Content Security Policy
============================================================
  386   Total
------------------------------------------------------------
  25    child-src
  25    connect-src
  25    font-src
  25    form-action
  25    frame-ancestors
  25    frame-src
  25    img-src
  25    manifest-src
  25    media-src
  1     object-src
  25    plugin-types
  25    sandbox
  10    script-src
  25    strict-dynamic
  25    style-src
  25    upgrade-insecure-requests
  25    worker-src


RetireJS
============================================================
  80    Total
------------------------------------------------------------
  0     Low
  80    Medium
  0     High
  0     Critical


Permissions
============================================================
  135   Total
------------------------------------------------------------
  135   Required
  0     Optional
```

### Save an Extension's Report to a File
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
```
➜  mrxcavator -r hdokiejnpimakedhajhdlcegeplioahd --export lastpass.txt

Extension Overview
============================================================
  Extension Name:       LastPass: Free Password Manager
  Extension ID:         hdokiejnpimakedhajhdlcegeplioahd
  Web Site:             https://www.lastpass.com/

  Newest Version:       4.53.0.2 (2020-07-29)
  Versions Known:       45
  Store Rating:         4.54 stars

  Total Risk Score:     395


Content Security Policy
============================================================
  70    Total
------------------------------------------------------------
  1     child-src
  37    connect-src
  1     font-src
  1     form-action
  1     frame-ancestors
  8     frame-src
  5     img-src
  1     manifest-src
  1     media-src
  1     object-src
  1     plugin-types
  1     sandbox
  1     script-src
  1     strict-dynamic
  7     style-src
  1     upgrade-insecure-requests
  1     worker-src


RetireJS
============================================================
  190   Total
------------------------------------------------------------
  20    Low
  80    Medium
  90    High
  0     Critical


Permissions
============================================================
  135   Total
------------------------------------------------------------
  110   Required
  25    Optional


External Calls
============================================================
  - https://www.dropbox.com/logout
  - https://www.netflix.com/Login
  - https://blog.lastpass.com/2019/03/new-improved-look-lastpass.html/
  - http://nowhere.co
  - https://lastpass.com/?securitychallenge=1
  - https://lastpass.com/
  - https://mint.intuit.com/login.event?task=S
  - https://accounts.lastpass.com/federated/oidcredirect.html
  - https://lastpass.com/forgot.php
  - https://www.logmeininc.com/legal/privacy?fromwebsite=1
  - https://lastpass.com/safariAppExtension.php?source=dropdown
  - https://lastpass.com/?ac=1
  - https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail&$expand=extensions
  - https://lastpass.com/experience-update
  - https://lastpass.com/fake/fake.php
  - https://support.logmeininc.com/lastpass/help/lastpass-authenticator-lp030014
  - https://lastpass.com/features_joinpremium4.php?a=1
  - https://www.lastpass.com/families/
  - https://www.lastpass.com/families
  - https://lastpass.eu/
  - http://link.lastpass.com/InpUsrLpEmb


>> Report saved in /Users/mstanislav/.mrxcavator/reports/lastpass.txt <<
```

### Get Reports For All Locally Installed Extensions
This feature supports `--input [filename]` to load extension identifiers from a text file.
```
➜  mrxcavator --report_all

Extension Overview
============================================================
  Extension Name:       Honey
  Extension ID:         bmnlcjabgnpnenekpadlanbbkooimhnj
  Web Site:             https://www.joinhoney.com

  Newest Version:       12.4.0 (2020-07-23)
  Versions Known:       45
  Store Rating:         4.84 stars

  Total Risk Score:     604


Content Security Policy
============================================================
  386   Total
------------------------------------------------------------
  25    child-src
  25    connect-src
  25    font-src
  25    form-action
  25    frame-ancestors
  25    frame-src
  25    img-src
  25    manifest-src
  25    media-src
  1     object-src
  25    plugin-types
  25    sandbox
  10    script-src
  25    strict-dynamic
  25    style-src
  25    upgrade-insecure-requests
  25    worker-src


RetireJS
============================================================
  80    Total
------------------------------------------------------------
  0     Low
  80    Medium
  0     High
  0     Critical


Permissions
============================================================
  135   Total
------------------------------------------------------------
  135   Required
  0     Optional

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extension Overview
============================================================
  Extension Name:       Zoom
  Extension ID:         hmbjbjdpkobdjplfobhljndfdfdipjhg

  Newest Version:       5.0.4169.0628 (2020-06-30)
  Versions Known:       26
  Store Rating:         2.76 stars

  Total Risk Score:     251


RetireJS
============================================================
  180   Total
------------------------------------------------------------
  10    Low
  140   Medium
  30    High
  0     Critical


Web Store
============================================================
  6     Total
------------------------------------------------------------
  1     Address
  1     Last Updated
  2     Rating
  1     Rating Users
  1     Website


Permissions
============================================================
  65    Total
------------------------------------------------------------
  65    Required
  0     Optional


External Calls
============================================================
  - https://www.google.com/accounts/Logout
  - http://www.w3.org/1998/Math/MathML
  - https://www.zoom.us

[...snip...]
```

### Get a Report Summary Table for All Locally Installed Extensions
This feature supports `--input [filename]` to load extension identifiers from a text file.
```
➜  mrxcavator --report_all_table
┌────────────────────────────────────────────┬──────────────────────────────────┬───────────────┬────────────┬────────┬──────┐
│ Name                                       │ Identifier                       │ Version       │ Updated    │ Rating │ Risk │
╞════════════════════════════════════════════╪══════════════════════════════════╪═══════════════╪════════════╪════════╪══════╡
│ Google Docs Offline                        │ ghbmnnjooekpmoecnnnilnnbdlolhkhi │ 1.9.1         │ 2020-03-04 │ 2.87   │ 423  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Honey                                      │ bmnlcjabgnpnenekpadlanbbkooimhnj │ 12.4.0        │ 2020-07-23 │ 4.84   │ 604  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Gmail                                      │ pjkljhegncpnkpknbcohdijeoejaedia │ 8.2           │ 2019-03-26 │ 4.53   │ 15   │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Bitwarden - Free Password Manager          │ nngceckbapebfimnlniiiahkandclblb │ 1.45.0        │ 2020-06-30 │ 4.84   │ 509  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Google Drive                               │ apdfllckaahabafndbhieahigkjlhalf │ 14.2          │ 2018-10-16 │ 4.43   │ 41   │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Application Launcher for Drive (by Google) │ lmjegmlicamnimmfhcmpkclmigmmcbeh │ 3.2           │ 2014-11-10 │ 2.95   │ 399  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Cisco Webex Extension                      │ jlhmfgmfgeifomenelglieieghnjghma │ 1.9.0         │ 2020-06-15 │ 2.4    │ 392  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Vue.js devtools                            │ nhdogjmejiglipccpnnnanhbledajbpd │ 5.3.3         │ 2019-11-25 │ 4.64   │ 438  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Zoom                                       │ hmbjbjdpkobdjplfobhljndfdfdipjhg │ 5.0.4169.0628 │ 2020-06-30 │ 2.76   │ 251  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ Save to Pocket                             │ niloccemoadcdkdjlinkgdfekeahmflj │ 3.0.6.8       │ 2019-07-24 │ 4.29   │ 479  │
├────────────────────────────────────────────┼──────────────────────────────────┼───────────────┼────────────┼────────┼──────┤
│ YouTube                                    │ blpcfgokakmgnkcojhhkbfbldkacnbeo │ 4.2.8         │ 2015-09-24 │ 4.52   │ 11   │
└────────────────────────────────────────────┴──────────────────────────────────┴───────────────┴────────────┴────────┴──────┘
```

### List Locally Installed Extensions
```
➜  mrxcavator -e

Extensions Found in ~/Library/Application Support/Google/Chrome/Default/Extensions/
┌────────────────────────────────────────────┬───────────────┬──────────────────────────────────┐
│ Name                                       │ Version       │ Identifier                       │
╞════════════════════════════════════════════╪═══════════════╪══════════════════════════════════╡
│ Google Docs Offline                        │ 1.11.0        │ ghbmnnjooekpmoecnnnilnnbdlolhkhi │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Honey                                      │ 12.3.2        │ bmnlcjabgnpnenekpadlanbbkooimhnj │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Gmail                                      │ 8.2           │ pjkljhegncpnkpknbcohdijeoejaedia │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Bitwarden - Free Password Manager          │ 1.45.0        │ nngceckbapebfimnlniiiahkandclblb │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Google Drive                               │ 14.2          │ apdfllckaahabafndbhieahigkjlhalf │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Application Launcher for Drive (by Google) │ 3.2           │ lmjegmlicamnimmfhcmpkclmigmmcbeh │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Cisco Webex Extension                      │ 1.9.0         │ jlhmfgmfgeifomenelglieieghnjghma │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Google Keep Chrome Extension               │ 4.20282.540.1 │ lpcaedmchfhocbbapmcbpinfpgnhiddi │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Zoom                                       │ 5.0.4169.628  │ hmbjbjdpkobdjplfobhljndfdfdipjhg │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Save to Pocket                             │ 3.0.6.8       │ niloccemoadcdkdjlinkgdfekeahmflj │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ Save to Google Drive                       │ 2.1.1         │ gmbmikajjgmnabiglmofipeabaddhgne │
├────────────────────────────────────────────┼───────────────┼──────────────────────────────────┤
│ YouTube                                    │ 4.2.8         │ blpcfgokakmgnkcojhhkbfbldkacnbeo │
└────────────────────────────────────────────┴───────────────┴──────────────────────────────────┘
```

### Show a Graph of an Extension's Risk Score Over Time
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
```
➜  mrxcavator -g bmnlcjabgnpnenekpadlanbbkooimhnj

674 ┤
668 ┤                                     ╭╮
662 ┤                                     ││
656 ┤                                     │╰────
650 ┤                                     │
644 ┤                 ╭╮                  │
638 ┤                 ││                  │
631 ┤                 ││               ╭──╯
625 ┤                 ││               │
619 ┤                 ││               │
613 ┤     ╭─╮         ││        ╭──────╯
607 ┤     │ │╭─╮      ││        │
601 ┤     │ ││ │      ││        │
595 ┤     │ ││ │      ││        │
589 ┤     │ ││ │      ││        │
583 ┤     │ ││ │      │╰─╮      │
577 ┤     │ ││ │      │  │      │
571 ┤     │ ││ │      │  │      │
565 ┤     │ ││ │      │  │      │
559 ┤     │ ││ │      │  │      │
552 ┤     │ ││ │      │  │      │
546 ┤     │ ││ │      │  │      │
540 ┤     │ ││ │      │  │      │
534 ┤     │ ││ │      │  │      │
528 ┼─────╯ ╰╯ ╰──────╯  ╰╮     │
522 ┤                     ╰─────╯
516 ┤
```

### Retrieve VirusTotal Results for an Extension's "External Call" Hostnames
If no extension identifier is passed to the flag, a list of locally installed extensions will be given to select from.
```
➜  mrxcavator -vt hmbjbjdpkobdjplfobhljndfdfdipjhg

** This API requires throttling. This extension will take approximately 0:01:05 to complete. **

Processing 3 hosts...
 * www.google.com, www.w3.org, www.zoom.us
┌────────────────┬───────────┬───────┐
│ Hostname       │ Positives │ Total │
╞════════════════╪═══════════╪═══════╡
│ www.google.com │ 0         │ 79    │
├────────────────┼───────────┼───────┤
│ www.w3.org     │ 1         │ 79    │
├────────────────┼───────────┼───────┤
│ www.zoom.us    │ 0         │ 79    │
└────────────────┴───────────┴───────┘
```

### Set the CRXcavator API URI Value
```
➜  mrxcavator --crxcavator_uri https://api.crxcavator.io/v1

	The CRXcavator API URI was set successfully!
```

### Set the CRXcavator API Key Value
```
➜  mrxcavator --crxcavator_key DEnDIwspwQkiMYZzuFbHOHUqDOpSaDIw

	The CRXcavator API key was set successfully!
```

### Set the VirusTotal API Key Value
```
➜  mrxcavator --virustotal_key d42d8fb60105539a632d209ed35a42515722a79be2c39f5635d3790b25433acc

	The VirusTotal API key was set successfully!
```

### Test Current CRXcavator API Base URI Setting
```
➜  mrxcavator --test_crxcavator_uri

	The CRXcavator API URI was successfully tested!
```

### Test Current CRXcavator API Key Setting
```
➜  mrxcavator --test_crxcavator_key

	The CRXcavator API key was successfully tested!
```

### Test Current VirusTotal API Key Setting
```
➜  mrxcavator --test_virustotal_key

	The VirusTotal API key was successfully tested!
```

### Use a Custom Configuration File
```
➜  mrxcavator -c testing.ini

	/Users/mstanislav/.mrxcavator/testing.ini does not exist, or is corrupted. Creating it...

➜  cat /Users/mstanislav/.mrxcavator/testing.ini
[DEFAULT]
crxcavator_api_uri = https://api.crxcavator.io/v1
crxcavator_api_key =
virustotal_api_key =
extension_path = ~/Library/Application Support/Google/Chrome/Default/Extensions/

[custom]
```

### Get mrxcavator's Version
```
➜  mrxcavator -v
v0.6.2
```

### Example `config.ini` Contents
```
➜  cat /Users/mstanislav/.mrxcavator/config.ini
[DEFAULT]
crxcavator_api_uri = https://api.crxcavator.io/v1
crxcavator_api_key =
virustotal_api_key =
extension_path = ~/Library/Application Support/Google/Chrome/Default/Extensions/

[custom]
```

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

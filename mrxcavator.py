#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mrxcavator.py: CLI client for CRXcavator.io"""

__author__ = "Mark Stanislav"
__license__ = "MIT"
__version__ = "0.2"

import os
import re
import sys
import json
import inspect
import argparse
import requests
import validators  # type: ignore
import configparser

from packaging import version

CONFIG_FILE = "config.ini"
CRX_PATH = "~/Library/Application Support/Google/Chrome/Default/Extensions"

config = configparser.ConfigParser()


def is_ignored(id: str) -> bool:
    """Returns a boolean to designate if a passed-in extension ID is within the
    ignored list or not. These ignored extensions are ones that get installed
    by Google and normally "hidden" from view (i.e. chrome:///extensions)

    Args:
        id: An extension identifier string.

    Returns:
        A bool.
    """
    ignored = [
        "nmmhkkegccagdldgiimedpiccmgmieda",
        "pkedcjkdefgpdelpbcmbmeomcjbeemfm",
    ]

    if id in ignored:
        return True
    else:
        return False


def error(message: str, fatal=False) -> bool:
    """Prints a passed-in message and then exits with False or a failure exit.

    Args:
        message: A message string.

    Returns:
        False or exits the application with a failure status code.
    """
    print(f"\n\t{message}\n")
    if fatal is True:
        sys.exit(1)
    else:
        return False


def call_api(end_point: str, method: str, values=None, headers=None) -> dict:
    """Calls an API endpoint with a passed-in HTTP method and an optional dict
    of values for APIs that required parameters to be sent in the request.

    Args:
        end_point: An API endpoint path string.
        method: The HTTP method string to use for the API call.
        values: An optional dict of values to pass as API parameters.
        headers: An optional dict of headers to pass to the API.

    Returns:
        A dict of API results or an empty dict.
    """
    endpoint = config.get("custom", "crxcavator_api_uri") + end_point

    if method == "GET":
        response = requests.get(endpoint, json=values, headers=headers)
    elif method == "POST":
        response = requests.post(endpoint, json=values, headers=headers)
    else:
        error(f"'{method}' is not a valid HTTP method.", True)

    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    elif response.status_code == 401:
        error("401 - API Not Authorized - Please check your API token.", True)
    elif response.status_code == 403:
        error("403 - API Error - Please check your API parameters.", True)
    elif response.status_code == 404:
        error("404 - API Not Found - Please check your API endpoint.", True)
    else:
        error("An unknown API error has occurred.", True)

    return {}


def version_count(results: dict) -> int:
    """Returns a count of CRXcavator-tracked versions for an extension.

    Args:
        results: A dict of CRXcavator extension results.

    Returns:
        An int.
    """
    total = 0

    for result in results:
        if result["version"]:
            total += 1

    return total


def get_report_summary(results: dict) -> bool:
    """Prints a formatted report of information for the given extension.

    Args:
        results: A dict of all extension information.

    Returns:
        True.
    """
    id = results[-1]["extension_id"]
    version = results[-1]["version"]
    versions = version_count(results)

    webstore = results[-1]["data"]["webstore"]
    risk = results[-1]["data"]["risk"]

    print(
        inspect.cleandoc(
            f"""
            \t
            Overview
            {'='*80}
            \tExtension Name:\t{webstore['name']}
            \tExtension ID:\t{id}
            \tNewest Version:\t{version} ({webstore['last_updated']})
            \tVersions Known:\t{versions}
            \tStore Rating:\t{webstore['rating']} stars
            \t
            Risk
            {'='*80}
            \tCSP Policy:\t{risk['csp']['total']}
            \tRetireJS: \t{risk['retire']['total']}
            \tWeb Store: \t{risk['webstore']['total']}
            \t
            \tPermissions:
              \t  >Required:\t{risk['permissions']['total']}
              \t  >Optional:\t{risk['optional_permissions']['total']}
            \t
            \t** Risk Score:\t{risk['total']} **
            \t
            """
        )
    )

    return True


def submit_extension(id: str) -> bool:
    """Submits an extension (by ID) for CRXcavator to process.

    Args:
        id: An extension identifier string.

    Returns:
        A boolean.
    """
    result = call_api("/submit", "POST", {"extension_id": id})

    if result["code"] == 802 and is_ignored(id) is False:
        error(f"{id} is not a valid extension. Please check your input.")
        return False
    else:
        return True


def get_report(id: str) -> bool:
    """Requests the CRXcavator report (in JSON) for the given extension ID.

    Args:
        id: An extension identifier string.

    Returns:
        A boolean.
    """
    result = call_api("/report/" + id, "GET")

    if result is None:
        error(f"No reports were found for extension {id}.")
        return False
    else:
        get_report_summary(result)
        return True


def write_config(filename: str) -> bool:
    """Writes the state of ConfigParser to the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.

    Returns:
        A boolean.
    """
    try:
        with open(filename, "w") as fileHandle:
            config.write(fileHandle)
    except IOError:
        error(f"Cannot write to {filename}. Please check permissions.", True)

    return True


def build_config(filename: str) -> bool:
    """Builds a default configuration and says it  to the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.

    Returns:
        A boolean.
    """
    config["DEFAULT"] = {"crxcavator_api_uri": "https://api.crxcavator.io/v1"}
    config.add_section("custom")

    if write_config(filename):
        return True
    else:
        return False


def load_config(filename: str) -> bool:
    """Loads ConfigParser with configuration data from the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.

    Returns:
        A boolean.
    """
    config.read(filename)

    if config.sections() == []:
        error(f"{filename} does not exist, or is corrupted. Creating it...")

        if not build_config(filename):
            return False

    return True


def set_crxcavator_key(filename: str, key: str) -> bool:
    """Configures the CRXcavator API key into the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.
        key: The CRXcavator API key as a string.

    Returns:
        A boolean.
    """
    if len(key) != 32 or re.match("^[a-zA-Z]+$", key) is False:
        error(f"The provided API key, {key}, is incorrectly formatted.", True)
    else:
        config.set("custom", "crxcavator_api_key", key)

        if not write_config(filename):
            return False

    return True


def set_crxcavator_uri(filename: str, uri: str) -> bool:
    """Configures the CRXcavator API URI into the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.
        uri: The CRXcavator URI for API calls as a string.

    Returns:
        A boolean.
    """
    if validators.url(uri) is True:
        config.set("custom", "crxcavator_api_uri", uri)

        if not write_config(filename):
            return False
    else:
        error(f"The provided API URI, {uri}, is incorrectly formatted.", True)

    return True


def test_crxcavator_key() -> bool:
    """Performs an API call to CRXcavator to test the configured API key.

    Args:
        None

    Returns:
        A boolean.
    """
    key = config.get("custom", "crxcavator_api_key")

    if key:
        if call_api("/user/apikey", "GET", {}, {"API-Key": key}):
            return True
        else:
            return False
    else:
        error(f"No CRXcavator API key has been set yet.")
        return False


def test_crxcavator_uri() -> bool:
    """Performs an API call to CRXcavator to test the configured URI.

    Args:
        None

    Returns:
        A boolean.
    """
    result = call_api("", "GET")

    if result["text"] == "CRXcavator":
        return True
    else:
        return False


def get_crx_path(id: str = "") -> str:
    """Returns a filesystem path to the system's Chrome Extension directory. An
    optional extentension ID may be passed in to append to the retuned path.

    Args:
        id: An optional extension identifier string.

    Returns:
        A string with the appropriate filesystem path.
    """
    return os.path.expanduser(CRX_PATH) + "/" + id


def find_extension_directories(path: str) -> list:
    """Return all valid Chrome extension directories from a passed-in path.

    Args:
        path: The filesystem path to Chrome extensions.

    Returns:
        A list containing Chrome extension directories.
    """
    directories = []

    for dir in next(os.walk(get_crx_path()))[1]:
        if len(dir) == 32:
            directories.append(dir)

    return directories


def get_extension_messages_path(path: str) -> str:
    """Return the path to an extension's most appropriate messages.json file.

    Args:
        path: The filesystem path to a specific Chrome extension.

    Returns:
        A string to the most appropriate messages.json file.
    """
    messages_en = f"{path}/_locales/en/messages.json"
    messages_en_US = f"{path}/_locales/en_US/messages.json"
    messages_en_GB = f"{path}/_locales/en_GB/messages.json"

    if os.path.isfile(messages_en_US):
        path = messages_en_US
    elif os.path.isfile(messages_en_GB):
        path = messages_en_GB
    elif os.path.isfile(messages_en):
        path = messages_en
    else:
        path = ""

    return path


def get_extension_messages_name(name: str, messages: dict) -> str:
    manifest_key = re.search("__MSG_(.+?)__", name).group(1)  # type: ignore

    if manifest_key:
        switcher = {
            "APP_NAME": "app_name",
            "CHROME_EXTENSION_NAME": "chrome_extension_name",
            "appName": "appName",
            "extName": "extName",
        }

        messages_key = switcher.get(manifest_key, "")
        name = messages[messages_key]["message"]
    else:
        name = ""

    return name


def get_extension_name(extension: str, version: str) -> str:
    crx_base = f"{get_crx_path(extension)}/{version}/"
    manifest_path = f"{crx_base}/manifest.json"
    messages_path = get_extension_messages_path(crx_base)

    with open(manifest_path) as manifestHandle:
        manifest = json.load(manifestHandle)

    if re.match("^__MSG", manifest["name"]) is None:
        name = manifest["name"]
    elif messages_path != "":
        with open(messages_path) as messagesHandle:
            messages = json.load(messagesHandle)

        name = get_extension_messages_name(manifest["name"], messages)
    else:
        name = "**Unknown Name**"

    return name


def get_latest_extension_version(extension_dir: str) -> str:
    vers = []

    for dir in next(os.walk(get_crx_path(extension_dir)))[1]:
        vers.append(version.parse(dir))

    return str(max(vers))


def get_installed_extensions(path: str) -> list:
    extensions: list = []

    for dir in find_extension_directories(path):
        version = get_latest_extension_version(dir)
        name = get_extension_name(dir, version)
        extensions.append({"name": name, "version": version, "id": dir})

    return extensions


def submit_extensions(extensions: list):
    for extension in extensions:
        if submit_extension(extension["id"]):
            print(f"\tYou've successfully submitted {extension['name']}.")
        else:
            error(f"{id} could not be found in the Chrome store")


if __name__ == "__main__":
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("Please use Python >=3.6 with this program.\n")
        sys.exit(1)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s", "--submit", metavar="id", help="submit an extension"
        )
        parser.add_argument(
            "--submit_all",
            action="store_true",
            help="submit all installed extensions",
        )
        parser.add_argument(
            "-r", "--report", metavar="id", help="get an extension's report"
        )
        parser.add_argument(
            "--crxcavator_key", metavar="key", help="set CRXcavator API key"
        )
        parser.add_argument(
            "--crxcavator_uri", metavar="uri", help="set CRXcavator API URI"
        )
        parser.add_argument(
            "--test_crxcavator_key",
            action="store_true",
            help="test configured CRXcavator API key",
        )
        parser.add_argument(
            "--test_crxcavator_uri",
            action="store_true",
            help="test configured CRXcavator API URI",
        )
        parser.add_argument(
            "-e",
            "--extensions",
            action="store_true",
            help="list installed extensions",
        )
        parser.add_argument(
            "-v", "--version", action="version", version="v" + __version__
        )

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        args = parser.parse_args()

        load_config(CONFIG_FILE)

        if args.submit:
            if submit_extension(args.submit):
                print(f"\n\tYou've successfully submitted {args.submit}.\n")
        elif args.report:
            get_report(args.report)
        elif args.crxcavator_key:
            if set_crxcavator_key(CONFIG_FILE, args.crxcavator_key):
                print(f"\n\tThe CRXcavator API key was set successfully!\n")
        elif args.crxcavator_uri:
            if set_crxcavator_uri(CONFIG_FILE, args.crxcavator_uri):
                print(f"\n\tThe CRXcavator API URI was set successfully!\n")
        elif args.test_crxcavator_key:
            if test_crxcavator_key():
                print(f"\n\tThe CRXcavator API key was successfully tested!\n")
        elif args.test_crxcavator_uri:
            if test_crxcavator_uri():
                print(f"\n\tThe CRXcavator API URI was successfully tested!\n")
            else:
                error("The CRXcavator API URI returned an unexpected result.")
        elif args.extensions:
            for ext in get_installed_extensions(CRX_PATH):
                print(f"\t{ext['name']} [{ext['version']}] ({ext['id']})")
        elif args.submit_all:
            submit_extensions(get_installed_extensions(CRX_PATH))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mrxcavator.py: CLI client for CRXcavator.io"""

__author__ = "Mark Stanislav"
__license__ = "MIT"
__version__ = "0.1"

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


def get_report_summary(result: dict) -> bool:
    """Prints a formatted report of information for the given extension.

    Args:
        result: A dict of extension information.
    Returns:
        True.
    """

    id = result[-1]["extension_id"]
    version = result[-1]["version"]

    result = result[-1]["data"]

    print(
        inspect.cleandoc(
            f"""
            \t
            Overview
            {'='*80}
            \tExtension Name:\t{result['webstore']['name']}
            \tExtension ID:\t{id}
            \tNewest Version:\t{version} ({result['webstore']['last_updated']})
            \tStore Rating:\t{result['webstore']['rating']} stars
            \t
            Risk
            {'='*80}
            \tCSP Policy:\t{result['risk']['csp']['total']}
            \tRetireJS: \t{result['risk']['retire']['total']}
            \tWeb Store: \t{result['risk']['webstore']['total']}
            \t
            \tPermissions:
              \t  >Required:\t{result['risk']['permissions']['total']}
              \t  >Optional:\t{result['risk']['optional_permissions']['total']}
            \t
            \t** Risk Score:\t{result['risk']['total']} **
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

    if result["code"] == 802:
        error(f"{id} is not a valid extension. Please check your input.", True)
    else:
        print(f"\n\tYou've successfully submitted {id} to CRXcavator.\n")

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


def get_crx_path(extension: str = "") -> str:
    return os.path.expanduser(CRX_PATH) + "/" + extension


def find_extension_directories(path: str) -> list:
    directories = []

    for dir in next(os.walk(get_crx_path()))[1]:
        if len(dir) == 32:
            directories.append(dir)

    return directories


def get_extension_name(extension_dir: str) -> str:
    return ""


def get_latest_extension_version(extension_dir: str) -> str:
    vers = []

    for dir in next(os.walk(get_crx_path(extension_dir)))[1]:
        vers.append(version.parse(dir))

    return str(max(vers))


def get_installed_extensions(path: str) -> dict:
    extensions: dict = {}

    for dir in find_extension_directories(path):
        latest_version = get_latest_extension_version(dir)
        print(f"Found {dir} with a latest version of {latest_version}")

    return extensions


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
            submit_extension(args.submit)
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
            get_installed_extensions(CRX_PATH)

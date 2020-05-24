#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mrxcavator.py: CLI client for CRXcavator.io"""

__author__ = "Mark Stanislav"
__license__ = "MIT"
__version__ = "0.1"

import sys
import json
import inspect
import argparse
import requests

crxcavator_api_base = "https://api.crxcavator.io/v1"


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


def call_api(end_point: str, method: str, values=None) -> dict:
    """Calls an API endpoint with a passed-in HTTP method and an optional dict
    of values for APIs that required parameters to be sent in the request.

    Args:
        end_point: An API endpoint path string.
        method: The HTTP method string to use for the API call.
        values: An optional dict of values to pass as API parameters.

    Returns:
        A dict of API results or an empty dict.
    """

    endpoint = crxcavator_api_base + end_point

    if method == "GET":
        response = requests.get(endpoint)
    elif method == "POST":
        response = requests.post(endpoint, json=values)
    else:
        error(f"'{method}' is not a valid HTTP method.")

    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    elif response.status_code == 401:
        error("401 - API Not Authorized - Please check your API token.")
    elif response.status_code == 403:
        error("403 - API Error - Please check your API parameters.")
    elif response.status_code == 404:
        error("404 - API Not Found - Please check your API endpoint.")
    else:
        error("An unknown API error has occurred.")

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
        error(f"No extension called {id} was found. Please check your ID.")
        return False
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
            "-v", "--version", action="version", version="v" + __version__
        )

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        args = parser.parse_args()

        if args.submit:
            submit_extension(args.submit)
        elif args.report:
            get_report(args.report)

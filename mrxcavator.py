#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mrxcavator.py: CLI client for CRXcavator.io"""

__author__ = "Mark Stanislav"
__license__ = "MIT"
__version__ = "0.6.3"


import os
import re
import sys
import math
import time
import json
import itertools
import datetime
import argparse
import requests
import asciichartpy  # type: ignore
import termtables  # type: ignore
import validators  # type: ignore
import configparser

from packaging import version
from tqdm import tqdm  # type: ignore
from typing import Generator, Any
from PyInquirer import prompt  # type: ignore
from urllib.parse import urlparse


ROOT_DIR = "~/.mrxcavator"
REPORT_DIR = "reports"
CONFIG_FILE = "config.ini"
CRX_PATH = "~/Library/Application Support/Google/Chrome/Default/Extensions/"

config = configparser.ConfigParser()
extension_path = ""


def extensions_from_file(filename: str) -> list:
    """Returns a list of extension dicts based on the passed-in file.

    Args:
        filename: A file containing a list of extension identifiers.

    Returns:
        A list of extensions.
    """
    try:
        with open(filename, "r") as fileHandle:
            extensions = []

            for extension in fileHandle.read().splitlines():
                if len(extension) == 32 and extension:
                    extensions.append(
                        {"id": extension, "name": extension, "version": "TBD"}
                    )

            return extensions

    except IOError:
        error(f"Cannot read {filename}. Please check permissions.", True)

    return []


def get_extcalls(results: list) -> list:
    """Returns a list of unique, valid URIs based on the passed-in list.

    Args:
        results: A list of "external calls" from a CRXcavator report.

    Returns:
        A list of items.
    """
    data = []

    for url in results:
        netloc = urlparse(url).netloc

        if validators.domain(netloc) and url not in data:
            data.append(url)

    return data


def chunker(seq: list, size: int) -> Generator:
    """Returns a list of items in groups based on the passed-in size.

    Args:
        seq: A list of items
        size: An integer for the number of items to "chunk" at a time.

    Returns:
        A list of items.
    """
    return (
        seq[pos : pos + size] for pos in range(0, len(seq), size)  # noqa: E203
    )


def get_report_dir() -> str:
    """Returns a string for the filesystem path of where to store reports.

    Args:
        None

    Returns:
        A string for the filesystem path for storing reports.
    """
    return os.path.expanduser(f"{ROOT_DIR}/{REPORT_DIR}/")


def get_root_dir() -> str:
    """Returns a string for the filesystem path for a local mrxcavator content.

    Args:
        None

    Returns:
        A string for the filesystem path for storing local mrxcavator content.
    """
    return os.path.expanduser(f"{ROOT_DIR}/")


def get_virustotal(report: dict, key: str) -> list:
    """Returns a list of VirusTotal results for the passed-in hostnames.

    Args:
        report: A dict of a CRXcavator extension report.
        key: The VirusTotal API key as a string.

    Returns:
        A list of VirusTotal results for passed-in hostnames.
    """
    if "extcalls" not in report[-1]["data"]:
        return []

    urls = report[-1]["data"]["extcalls"]

    data = []
    for url in urls:
        netloc = urlparse(url).netloc

        if validators.domain(netloc) and netloc not in data:
            data.append(netloc)

    seconds = (130 * math.ceil(len(data) / 4)) - 65
    duration = str(datetime.timedelta(seconds=seconds))

    print(
        f"\n** This API requires throttling. This extension will take "
        f"approximately {duration} to complete. **\n"
    )

    print(f"Processing {len(data)} hosts...")

    results = []
    first_chunk = 1

    for group in chunker(data, 4):
        print(f" * {', '.join(group)}")

        if first_chunk == 1:
            first_chunk = 0
        else:
            time.sleep(65)

        submit_virustotal(group, key)
        time.sleep(65)
        results.append(get_virustotal_reports(group, key))

    return list(itertools.chain(*results))


def get_virustotal_table(results: list) -> None:
    """Builds a table of VirusTotal results of an extension's "external calls."

    Args:
        results: A list of VirusTotal results for passed-in hostnames.

    Returns:
        None.
    """
    if len(results) == 0:
        error("No external calls were found for this extension.", True)

    data = []
    for result in results:
        data.append(
            [result["url"], result["vt"]["positives"], result["vt"]["total"]]
        )

    header = [
        "\033[1mHostname\033[0m",
        "\033[1mPositives\033[0m",
        "\033[1mTotal\033[0m",
    ]

    termtables.print(
        data,
        header=header,
        style=termtables.styles.thin_double,
        padding=(0, 1),
        alignment="lll",
    )


def submit_virustotal(hosts: list, key: str) -> bool:
    """Returns a boolean for the state of submitting hostnames to VirusTotal.

    Args:
        hosts: A list of hostnames for the "external calls" of an extension.
        key: The VirusTotal API key as a string.

    Returns:
        A boolean.
    """
    if call_api(
        "/virustotal/report",
        "POST",
        {"apiKey": key, "urls": hosts},
        {},
    ):
        return True
    else:
        return False


def get_virustotal_reports(hosts: list, key: str) -> dict:
    """Returns a dict of VirusTotal results for the passed-in hostnames.

    Args:
        hosts: A list of hostnames for the "external calls" of an extension.
        key: The VirusTotal API key as a string.

    Returns:
        A dict of VirusTotal results for passed-in hostnames.
    """
    reports = call_api(
        "/virustotal/results",
        "POST",
        {"apiKey": key, "urls": hosts},
        {},
    )

    if reports:
        return reports
    else:
        return {}


def extension_is_ignored(id: str) -> bool:
    """Returns a boolean to designate if a passed-in extension ID is within the
    ignored list or not. These ignored extensions are ones that get installed
    by Google and normally "hidden" from view (i.e. chrome:///extensions)

    Args:
        id: An extension identifier string.

    Returns:
        A boolean result.
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
        error("404 - API Not Found - Check your API configuration.", True)
    elif response.status_code == 500:
        error("500 - Server Error - Check your API configuration.", True)
    elif response.status_code == 502:
        error("502 - Bad Gateway - Retrying in five seconds...", False)
        time.sleep(5)
        call_api(end_point, method, values, headers)
    else:
        error("An unknown API error has occurred.", True)

    return {}


def version_count(report: dict) -> int:
    """Returns a count of CRXcavator-tracked versions for an extension.

    Args:
        report: A dict of a CRXcavator extension report.

    Returns:
        An integer count of versions.
    """
    total = 0

    for entry in report:
        if entry["version"]:
            total += 1

    return total


def export_report(id: str, report: str, filename: str) -> bool:
    """Exports a report summary to a file.

    Args:
        id: An extension identifier string.
        report: A string of the report summary.
        filename: The chosen filename as a string.

    Returns:
        A boolean result for exporting the report summary to a file.
    """
    if filename == "empty" or filename == "":
        filename = f"{get_report_dir()}{id}.txt"
    else:
        filename = f"{get_report_dir()}{filename}"

    if save_report(filename, report):
        print(f"\n>> Report saved in {filename} <<\n")
        return True
    else:
        error(f"A report for {id} could not be saved.")
        return False


def get_reports_table(extensions: list) -> None:
    """Builds a table of installed extension details from CRXcavator.

    Args:
        extensions: A list of extension identifier strings.

    Returns:
        None.
    """
    data = []
    for extension in extensions:
        report = get_report(extension["id"])

        if report:
            version = report[-1]["version"]
            webstore = report[-1]["data"]["webstore"]
            risk = report[-1]["data"]["risk"]

            data.append(
                [
                    webstore["name"],
                    extension["id"],
                    version,
                    webstore["last_updated"],
                    round(webstore["rating"], 2),
                    risk["total"],
                ]
            )

    header = [
        "\033[1mName\033[0m",
        "\033[1mIdentifier\033[0m",
        "\033[1mVersion\033[0m",
        "\033[1mUpdated\033[0m",
        "\033[1mRating\033[0m",
        "\033[1mRisk\033[0m",
    ]

    termtables.print(
        data,
        header=header,
        style=termtables.styles.thin_double,
        padding=(0, 1),
        alignment="llllll",
    )


def get_report_summary(report: dict) -> str:
    """Prints a formatted report of information for the given extension.

    Args:
        report: A dict of a CRXcavator extension report.

    Returns:
        A string of the report summary.
    """
    id = report[-1]["extension_id"]
    version = report[-1]["version"]
    versions = version_count(report)

    webstore = report[-1]["data"]["webstore"]
    risk = report[-1]["data"]["risk"]

    output = f"\nExtension Overview\n{'='*60}\n"
    output += f"  Extension Name:\t{webstore['name']}\n"
    output += f"  Extension ID:\t\t{id}\n"

    if webstore["website"] != "":
        output += f"  Web Site:\t\t{webstore['website']}\n"

    output += f"\n  Newest Version:\t{version} ({webstore['last_updated']})"
    output += f"\n  Versions Known:\t{versions}"
    output += f"\n  Store Rating:\t\t{round(webstore['rating'],2)} stars\n"
    output += f"\n  Total Risk Score:\t{risk['total']}"

    if "csp" in risk:
        output += f"\n\n\nContent Security Policy\n{'='*60}"
        output += f"\n  {risk['csp'].get('total', 0)}\tTotal\n{'-'*60}"

        csp_total = risk["csp"]["total"]
        del risk["csp"]["total"]

        csp_attribute_total = 0
        for key in risk["csp"].keys():
            output += f"\n  {risk['csp'][key]}\t{key}"
            csp_attribute_total += int(risk["csp"][key])

        if csp_total > csp_attribute_total:
            remainder = csp_total - csp_attribute_total
            missing = int(remainder / 25)
            output += f"\n  {remainder}\t{missing} attributes not set"

    if "retire" in risk:
        output += f"\n\n\nRetireJS\n{'='*60}"
        output += f"\n  {risk['retire'].get('total', '0')}\tTotal\n{'-'*60}"
        output += f"\n  {risk['retire'].get('low', '0')}\tLow"
        output += f"\n  {risk['retire'].get('medium', '0')}\tMedium"
        output += f"\n  {risk['retire'].get('high', '0')}\tHigh"
        output += f"\n  {risk['retire'].get('critical', '0')}\tCritical"

    webstore_total = risk["webstore"].get("total", "0")

    if webstore_total > 0:
        output += f"\n\n\nWeb Store\n{'='*60}"
        output += f"\n  {risk['webstore'].get('total', '0')}\tTotal\n{'-'*60}"

        del risk["webstore"]["total"]

        for key in risk["webstore"].keys():
            value = key.title().replace("_", " ")
            output += f"\n  {risk['webstore'][key]}\t{value}"

    perms_required = 0
    perms_optional = 0

    if "permissions" in risk:
        perms_required = risk["permissions"].get("total", 0)

    if "optional_permissions" in risk:
        perms_optional = risk["optional_permissions"].get("total", 0)

    perms_total = perms_required + perms_optional

    if perms_total > 0:
        output += f"\n\n\nPermissions\n{'='*60}"
        output += f"\n  {perms_total}\tTotal\n{'-'*60}"
        output += f"\n  {perms_required}\tRequired"
        output += f"\n  {perms_optional}\tOptional"

    if "extcalls" in report[-1]["data"]:
        output += f"\n\n\nExternal Calls\n{'='*60}"
        for result in get_extcalls(report[-1]["data"]["extcalls"]):
            output += f"\n  - {result}"

    return output + "\n"


def save_report(filename: str, content: str) -> bool:
    """Writes passed-in content to the passed-in filename.

    Args:
        filename: The chosen filename as a string.
        content: The chosen content to write as a string.

    Returns:
        A boolean result.
    """
    if not os.path.isdir(get_report_dir()):
        try:
            os.mkdir(get_report_dir())
        except IOError:
            error(
                f"Cannot create {get_report_dir()} - check permissions.",
                True,
            )

    try:
        with open(filename, "w") as fileHandle:
            fileHandle.write(content.strip())
    except IOError:
        error(f"Cannot write to {filename} -  check permissions.", True)

    return True


def submit_extension(id: str) -> bool:
    """Submits an extension (by ID) for CRXcavator to process.

    Args:
        id: An extension identifier string.

    Returns:
        A boolean result.
    """
    result = call_api("/submit", "POST", {"extension_id": id})

    if result["code"] == 802 and extension_is_ignored(id) is False:
        error(f"{id} is not a valid extension. Please check your input.")
        return False
    else:
        return True


def submit_extensions(extensions: list, path: str) -> None:
    """Submits many extensions (by ID) for CRXcavator to process.

    Args:
        extensions: A list of extension identifier strings.
        path: The system's directory path to Chrome extensions as a string.

    Returns:
        None.
    """
    successful = []
    failed = []

    print(f"\nSubmitting extensions found in {path}\n")

    for extension in tqdm(extensions, bar_format="{l_bar}{bar}"):
        if isinstance(extension, dict):
            submit = submit_extension(extension["id"])
        else:
            submit = submit_extension(extension)

        if submit:
            successful.append(extension["name"])
        else:
            failed.append(extension["name"])

    if len(successful) > 0:
        successful.sort()
        print("\nSuccessful:\n  > " + "\n  > ".join(successful))
    if len(failed) > 0:
        failed.sort()
        print("\n\nFailed:\n  > " + "\n  > ".join(failed))


def get_report(id: str) -> dict:
    """Requests the CRXcavator report (in JSON) for the given extension ID.

    Args:
        id: An extension identifier string.

    Returns:
        A dict of report results.
    """
    result = call_api("/report/" + id, "GET")

    if result is None:
        return {}
    else:
        return result


def get_reports(extensions: list, export: bool) -> None:
    """Retrieves a report summary for each passed-in extension ID in a list.

    Args:
        extensions: A list of extension identifier strings.
        export: A boolean for whether to export each report to a file.

    Returns:
        None.
    """
    for extension in extensions:
        if isinstance(extension, dict):
            report = get_report(extension["id"])
        else:
            report = get_report(extension)

        if report:
            summary = get_report_summary(report)
            print(f"{summary}\n{60*'~'}")
            if export is True:
                export_report(extension["id"], summary, "")


def write_config(filename: str) -> bool:
    """Writes the state of ConfigParser to the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.

    Returns:
        A boolean result.
    """
    if not os.path.isdir(get_root_dir()):
        try:
            os.mkdir(get_root_dir())
        except IOError:
            error(
                f"Cannot create {get_root_dir()} - check permissions.",
                True,
            )

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
        A boolean result.
    """
    config["DEFAULT"] = {
        "crxcavator_api_uri": "https://api.crxcavator.io/v1",
        "crxcavator_api_key": "",
        "virustotal_api_key": "",
        "extension_path": CRX_PATH,
    }
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
        A boolean result.
    """
    config.read(filename)

    if config.sections() == []:
        error(f"{filename} does not exist, or is corrupted. Creating it...")

        if not build_config(filename):
            return False

    return True


def set_extension_path(filename: str, path: str) -> bool:
    """Configures the system's directory path to Chrome extensions.

    Args:
        filename: The mrxcavator configuration filename as a string.
        path: The system's directory path to Chrome extensions as a string.

    Returns:
        A boolean result.
    """
    if os.path.isdir(os.path.expanduser(path)) is True:
        if path[-1] != "/":
            path = path + "/"

        config.set("custom", "extension_path", path)

        if not write_config(filename):
            return False
    else:
        error(f"The provided extension path, {path}, does not exist.", True)

    return True


def set_crxcavator_key(filename: str, key: str) -> bool:
    """Configures the CRXcavator API key into the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.
        key: The CRXcavator API key as a string.

    Returns:
        A boolean result.
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
        A boolean result.
    """
    if validators.url(uri) is True:
        config.set("custom", "crxcavator_api_uri", uri)

        if not write_config(filename):
            return False
    else:
        error(f"The provided API URI, {uri}, is incorrectly formatted.", True)

    return True


def set_virustotal_key(filename: str, key: str) -> bool:
    """Configures the VirusTotal API key into the passed-in filename.

    Args:
        filename: The mrxcavator configuration filename as a string.
        key: The VirusTotal API key as a string.

    Returns:
        A boolean result.
    """
    if len(key) != 64 or re.match("^[a-f0-9]+$", key) is False:
        error(f"The provided API key, {key}, is incorrectly formatted.", True)
    else:
        config.set("custom", "virustotal_api_key", key)

        if not write_config(filename):
            return False

    return True


def test_crxcavator_key() -> bool:
    """Performs an API call to CRXcavator to test the configured API key.

    Args:
        None

    Returns:
        A boolean result.
    """
    key = config.get("custom", "crxcavator_api_key")

    if key:
        if call_api("/user/apikey", "GET", {}, {"API-Key": key}):
            return True
        else:
            return False
    else:
        error("No CRXcavator API key has been set yet.")
        return False


def test_crxcavator_uri() -> bool:
    """Performs an API call to CRXcavator to test the configured URI.

    Args:
        None

    Returns:
        A boolean result.
    """
    result = call_api("", "GET")

    if result["text"] == "CRXcavator":
        return True
    else:
        return False


def test_virustotal_key() -> bool:
    """Performs a VirusTotal API call to test the configured API key.

    Args:
        None

    Returns:
        A boolean result.
    """
    key = config.get("custom", "virustotal_api_key")

    if key:
        if call_api(
            "/virustotal/report",
            "POST",
            {"apiKey": key, "urls": ["google.com"]},
            {},
        ):
            return True
        else:
            return False
    else:
        error("No VirusTotal API key has been set yet.")
        return False


def get_crx_path(id: str = "") -> str:
    """Returns a filesystem path to the system's Chrome Extension directory. An
    optional extentension ID may be passed in to append to the retuned path.

    Args:
        id: An optional extension identifier string.

    Returns:
        A string with the appropriate filesystem path for a(n) extension(s).
    """
    return os.path.expanduser(extension_path) + id


def find_extension_directories(path: str) -> list:
    """Return all valid Chrome extension directories from a passed-in path.

    Args:
        path: The filesystem path to Chrome extensions.

    Returns:
        A list containing Chrome extension directories.
    """
    directories = []
    path = get_crx_path()

    if os.path.isdir(os.path.expanduser(path)) is True:
        for dir in next(os.walk(path))[1]:
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
    """Returns the 'name' of a Chrome extension via a messages.json file.

    Args:
        name: The canonical reference string for a messages.json value.
        messages: A dict representation for a represented messages.json file.

    Returns:
        A string for the 'name' of a Chrome extension via a messages.json file.
    """
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


def get_extension_name(id: str, version: str) -> str:
    """Returns the 'name' of a Chrome extension by finding the correct source.

    Args:
        id: An extension identifier string.
        version: The extension version that is used to search file paths.

    Returns:
        A string for the 'name' of a Chrome extension.
    """
    crx_base = f"{get_crx_path(id)}/{version}/"
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


def get_latest_local_version(extension_dir: str) -> str:
    """Returns the latest local version for a passed-in extension path.

    Args:
        extension_dir: A string for the path to a given local extension.

    Returns:
        A string for the version of the most recent local version available.
    """
    vers = []

    for dir in next(os.walk(get_crx_path(extension_dir)))[1]:
        vers.append(version.parse(dir))

    return str(max(vers))


def get_installed_extensions(path: str) -> list:
    """Returns a list of installed extensions based on a passed-in path.

    Args:
        path: A string for the path to installed Chrome extensions.

    Returns:
        A list of extension identifiers that are locally installed for Chrome.
    """
    extensions: list = []

    for dir in find_extension_directories(path):
        version = get_latest_local_version(dir)
        name = get_extension_name(dir, version)

        if extension_is_ignored(dir) is False:
            extensions.append({"name": name, "version": version, "id": dir})

    return extensions


def get_extensions_table(extensions: list, path: str) -> None:
    """Prints a table of installed extensions.

    Args:
        extensions: A list of installed extension meta data.
        path: A string for the path to installed Chrome extensions.

    Returns:
        None.
    """
    print(f"\nExtensions Found in {path}")

    data = []
    for ext in extensions:
        data.append([ext["name"], ext["version"].split("_")[0], ext["id"]])

    header = [
        "\033[1mName\033[0m",
        "\033[1mVersion\033[0m",
        "\033[1mIdentifier\033[0m",
    ]

    termtables.print(
        data,
        header=header,
        style=termtables.styles.thin_double,
        padding=(0, 1),
        alignment="lll",
    )


def get_risk_graph(id: str) -> None:
    """Prints a graph of an extension's risk scores over time.

    Args:
        id: An extension identifier string.

    Returns:
        None.
    """
    results = get_report(id)

    if len(results) == 0:
        error(f"No results were found for {id}.", True)

    data = []
    for item in results:
        data.append(item["data"]["risk"]["total"])

    print(
        asciichartpy.plot(
            data,
            {
                "min": min(data) - 5,
                "max": max(data) + 5,
                "height": 25,
                "format": "{:8.0f}",
            },
        )
    )


def select_extension(extensions: list) -> str:
    """Returns an extension identifier from the passed-in list via PyInquirer.

    Args:
        extensions: A list of extension identifier strings.

    Returns:
        A string of an extension identifier.
    """
    choices = []

    for extension in extensions:
        choices.append({"name": extension["name"], "value": extension["id"]})

    question = [
        {
            "type": "list",
            "name": "id",
            "message": "Please select an extension...",
            "choices": choices,
        }
    ]

    result = prompt(question)

    if "id" in result:
        return result["id"]
    else:
        error("No extension was selected.\n", True)
        return ""


def build_parser() -> Any:
    """Returns a configured object for argparse functionality.

    Args:
        None

    Returns:
        An object for argparse.
    """
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("Please use Python >=3.6 with this program.\n")
        sys.exit(1)
    else:
        parser = argparse.ArgumentParser(add_help=False)

        help_features = parser.add_argument_group("Features")
        help_config = parser.add_argument_group("Set Configuration")
        help_test = parser.add_argument_group("Test Configuration")
        help_misc = parser.add_argument_group("Miscellaneous")

        help_config.add_argument(
            "-c",
            "--config",
            metavar="filename",
            help="specify a configuration filename",
        )

        help_config.add_argument(
            "--extension_path",
            metavar="path",
            help="set path to local Chrome extensions",
        )

        help_config.add_argument(
            "--crxcavator_key", metavar="key", help="set CRXcavator API key"
        )

        help_config.add_argument(
            "--crxcavator_uri", metavar="uri", help="set CRXcavator API URI"
        )

        help_config.add_argument(
            "--virustotal_key", metavar="key", help="set VirusTotal API key"
        )

        help_test.add_argument(
            "--test_crxcavator_key",
            action="store_true",
            help="test CRXcavator API key",
        )

        help_test.add_argument(
            "--test_crxcavator_uri",
            action="store_true",
            help="test CRXcavator API URI",
        )

        help_test.add_argument(
            "--test_virustotal_key",
            action="store_true",
            help="test VirusTotal API key",
        )

        help_features.add_argument(
            "-s",
            "--submit",
            nargs="?",
            const="empty",
            metavar="id",
            help="submit an extension",
        )

        help_features.add_argument(
            "--submit_all",
            action="store_true",
            help="submit all installed extensions",
        )

        help_features.add_argument(
            "-r",
            "--report",
            nargs="?",
            const="empty",
            metavar="id",
            help="get an extension's report",
        )

        help_features.add_argument(
            "--report_all",
            action="store_true",
            help="retrieve a report for all installed extensions",
        )

        help_features.add_argument(
            "--report_all_table",
            action="store_true",
            help="retrieve a table of details for installed extensions",
        )

        help_features.add_argument(
            "--export",
            nargs="?",
            const="empty",
            metavar="filename",
            help="export a report to a specific filename",
        )

        help_features.add_argument(
            "--input",
            nargs="?",
            const="empty",
            metavar="filename",
            help="load a specific filename for extension identifiers",
        )

        help_features.add_argument(
            "-e",
            "--extensions",
            action="store_true",
            help="list installed extensions",
        )

        help_features.add_argument(
            "-g",
            "--graph",
            nargs="?",
            const="empty",
            metavar="id",
            help="get a graph of an extension's risk",
        )

        help_features.add_argument(
            "-vt",
            "--virustotal",
            nargs="?",
            const="empty",
            metavar="id",
            help="get VirusTotal data for an extension's external calls",
        )

        help_misc.add_argument(
            "-v", "--version", action="version", version="v" + __version__
        )

        help_misc.add_argument(
            "-h",
            "--help",
            action="help",
            help="show program's help information and exit",
        )

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        return parser


def main() -> None:
    """Executes mrxcavator's essential functionality.

    Args:
        None

    Returns:
        None
    """
    global config
    global extension_path

    parser = build_parser()
    args = parser.parse_args()

    if args.config:
        config_file = f"{get_root_dir()}{args.config}"
    else:
        config_file = f"{get_root_dir()}{CONFIG_FILE}"

    load_config(config_file)

    extension_path = config.get("custom", "extension_path")

    if args.submit:
        if args.submit == "empty":
            id = select_extension(get_installed_extensions(extension_path))
        else:
            id = args.submit

        if submit_extension(id):
            print(f"\n\tYou've submitted {id}.\n")

    elif args.report:
        if args.report == "empty":
            id = select_extension(get_installed_extensions(extension_path))
        else:
            id = args.report

        results = get_report(id)

        if results:
            report = get_report_summary(results)
            print(report)
        else:
            error(f"The extension {id} was not found.")

        if results and args.export:
            export_report(id, report, args.export)

    elif args.extension_path:
        if set_extension_path(config_file, args.extension_path):
            print("\n\tThe system extension path was set successfully!\n")

    elif args.crxcavator_key:
        if set_crxcavator_key(config_file, args.crxcavator_key):
            print("\n\tThe CRXcavator API key was set successfully!\n")

    elif args.crxcavator_uri:
        if set_crxcavator_uri(config_file, args.crxcavator_uri):
            print("\n\tThe CRXcavator API URI was set successfully!\n")

    elif args.virustotal_key:
        if set_virustotal_key(config_file, args.virustotal_key):
            print("\n\tThe VirusTotal API key was set successfully!\n")

    elif args.test_crxcavator_key:
        if test_crxcavator_key():
            print("\n\tThe CRXcavator API key was successfully tested!\n")

    elif args.test_crxcavator_uri:
        if test_crxcavator_uri():
            print("\n\tThe CRXcavator API URI was successfully tested!\n")
        else:
            error("The CRXcavator API URI returned an unexpected result.")

    elif args.test_virustotal_key:
        if test_virustotal_key():
            print("\n\tThe VirusTotal API key was successfully tested!\n")

    elif args.extensions:
        extensions = get_installed_extensions(extension_path)

        if len(extensions) == 0:
            error("No extensions were found. Check your configuration.")
        else:
            get_extensions_table(extensions, extension_path)

    elif args.submit_all:
        if args.input:
            submit_extensions(extensions_from_file(args.input), args.input)
        else:
            submit_extensions(
                get_installed_extensions(extension_path), extension_path
            )

    elif args.report_all:
        if args.export:
            export = True
        else:
            export = False

        if args.input:
            get_reports(extensions_from_file(args.input), export)
        else:
            get_reports(get_installed_extensions(extension_path), export)

    elif args.report_all_table:
        if args.input:
            get_reports_table(extensions_from_file(args.input))
        else:
            get_reports_table(get_installed_extensions(extension_path))

    elif args.virustotal:
        if args.virustotal == "empty":
            id = select_extension(get_installed_extensions(extension_path))
        else:
            id = args.virustotal

        key = config.get("custom", "virustotal_api_key")

        if key == "":
            error("No VirusTotal API key has been set yet.", True)

        results = get_report(id)

        if results:
            get_virustotal_table(get_virustotal(results, key))
        else:
            error(f"The extension {id} was not found.")

    elif args.graph:
        if args.graph == "empty":
            id = select_extension(get_installed_extensions(extension_path))
        else:
            id = args.graph

        get_risk_graph(id)


if __name__ == "__main__":
    main()

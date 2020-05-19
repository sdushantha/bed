#!/usr/bin/env python
#
# by Siddharth Dushantha 2020
#

import re
import sys
import argparse
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup

# This magic spell lets me erase the current line.
# I can use this to show for example "Downloading..."
# and then "Downloaded" on the line where
# "Downloading..." was.
ERASE_LINE = '\033[2K'

GOOD = f"{Fore.GREEN}✔{Style.RESET_ALL}"
BAD = f"{Fore.RED}✘{Style.RESET_ALL}"


class Cursor:
    def hide():
        print("\033[?25l", end="\r", flush=True)

    def show():
        print("\033[?25h", end="\r", flush=True)


def get_firefox_extension(extension_url):
    """
    Get the file url, extension name and the version of the Chrome extension
    """

    # We have to use a Firefox user agent or else the "Add to Firefox" button wont show
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    response = requests.get(extension_url, headers=headers)
    html = response.text
    s = BeautifulSoup(html, "lxml")

    # Getting all the anchor tags because in one of the anchor tags, is
    # the url to the extension file
    a_tags = s.findAll("a")

    # We are looping through all the anchor tags, and checking if the url in the href
    # is the download link to the file
    for a_tag in a_tags:
        url = a_tag.get('href')
        if "https://addons.mozilla.org/firefox/downloads/file" in url:
            file_url = url

    # Get the version number of the extension by getting the text of the dd
    # tag with the class name Definition-dd AddonMoreInfo-version
    extension_version = s.find("dd", {"class": "Definition-dd AddonMoreInfo-version"}).text

    extension_name = re.findall(r"addon\/(.*)\/", extension_url)[0]

    return file_url, extension_name, extension_version


def get_chrome_extension(extension_url):
    """
    Get the file url, extension name and the version of the Chrome extension
    """
    response = requests.get(extension_url)
    html = response.text
    s = BeautifulSoup(html, "lxml")

    # Source: https://chrome-extension-downloader.com/how-does-it-work.php
    app_id = re.findall(r"detail\/(?:.*)\/((?:[^\?]*))", extension_url)[0]
    file_url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=49.0&x=id%3D{app_id}%26installsource%3Dondemand%26uc"

    # Get the version number of the extension by getting the text of the span
    # tag which has the class name C-b-p-D-Xe h-C-b-p-D-md
    extension_version = s.find("span", {"class": "C-b-p-D-Xe h-C-b-p-D-md"}).text

    extension_name = re.findall(r"detail\/(.*)\/", extension_url)[0]

    return file_url, extension_name, extension_version


def get_opera_extension(extension_url):
    """
    Get the file url, extension name and the version of the Opera extension
    """
    response = requests.get(extension_url)
    html = response.text
    s = BeautifulSoup(html, "lxml")

    extension_version = s.findAll("dd")[2].text
    extension_name = re.findall(r"details\/(.*)\/", extension_url)[0]
    file_url = f"https://addons.opera.com/extensions/download/{extension_name}/"

    return file_url, extension_name, extension_version


def get_browser(extension_url):
    """
    Loop over dictionary with browsers and the regex which matches
    the addon/extension url
    """

    browser_dict = {
        "firefox": {
            "regex": r"https:\/\/addons\.mozilla\.org\/[a-zA-Z-]+\/firefox\/addon\/.*"
            },
        "chrome": {
            "regex": r"https:\/\/chrome\.google\.com\/webstore\/detail\/[a-zA-Z0-9-_]+\/.*"
            },
        "opera": {
            "regex": r"https:\/\/addons\.opera\.com\/.*\/extensions\/details\/.*"
            }
        }

    # Loop over the dictionary and then check if the given extension url matches one
    # of the regexs. If does match, return the browser name
    for browser in browser_dict:
        regex = browser_dict.get(browser).get("regex")

        if re.match(regex, extension_url):
            return browser


def main():
    parser = argparse.ArgumentParser(description="A very simple command line Browser Extension Downloader")
    parser.add_argument('url', action="store")
    args = parser.parse_args()

    url = args.url

    Cursor.hide()

    if get_browser(url) == "chrome":
        print(f"{GOOD} Valid Chrome Web Store url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = get_chrome_extension(url)
        print(ERASE_LINE, end="\r", flush=True)
        print(f"{GOOD} Fetched webpage code code")

        file_extension = "crx"
        browser = "chrome"

    elif get_browser(url) == "firefox":
        print(f"{GOOD} Valid Firefox addon url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = get_firefox_extension(url)
        print(ERASE_LINE, end="\r", flush=True)
        print(f"{GOOD} Fetched webpage code code")

        file_extension = "xpi"
        browser = "firefox"

    elif get_browser(url) == "opera":
        print(f"{GOOD} Valid Opera addon url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = get_opera_extension(url)
        print(ERASE_LINE, end="\r", flush=True)
        print(f"{GOOD} Fetched webpage code code")

        file_extension = "crx"
        browser = "opera"

    else:
        print(f"{BAD} Invalid url")
        Cursor.show()
        sys.exit(1)

    file_url = extension_data[0]
    extension_name = extension_data[1]
    extension_version = extension_data[2]

    file_name = f"{browser}_{extension_name}_{extension_version}.{file_extension}"

    print(f"Downloading {file_name}...", end="\r", flush=True)
    response = requests.get(file_url)

    with open(file_name, "wb") as f:
        f.write(response.content)

    print(ERASE_LINE, end="\r", flush=True)
    print(f"{GOOD} Download complete: {file_name}")

    Cursor.show()


if __name__ == "__main__":
    main()

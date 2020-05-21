#!/usr/bin/env python
#
# by Siddharth Dushantha 2020
#

import sys
import argparse
import requests
from colorama import Fore, Style
from . import utils

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


def main():
    parser = argparse.ArgumentParser(description="A very simple command line Browser Extension Downloader")
    parser.add_argument('url', action="store")
    args = parser.parse_args()

    url = args.url

    Cursor.hide()

    if utils.get_browser(url) == "chrome":
        print(f"{GOOD} Valid Chrome Web Store url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = utils.get_chrome_extension(url)
        print(ERASE_LINE, end="\r", flush=True)
        print(f"{GOOD} Fetched webpage code code")

        file_extension = "crx"
        browser = "chrome"

    elif utils.get_browser(url) == "firefox":
        print(f"{GOOD} Valid Firefox addon url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = utils.get_firefox_extension(url)
        print(ERASE_LINE, end="\r", flush=True)
        print(f"{GOOD} Fetched webpage code code")

        file_extension = "xpi"
        browser = "firefox"

    elif utils.get_browser(url) == "opera":
        print(f"{GOOD} Valid Opera addon url")

        print("Getting webpage source code...", end="\r", flush=True)
        extension_data = utils.get_opera_extension(url)
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

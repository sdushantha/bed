#!/usr/bin/env python
#
# by Siddharth Dushantha 2020
#

import re
import sys
import argparse
import requests
from bs4 import BeautifulSoup


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



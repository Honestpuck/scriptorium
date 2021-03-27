#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "1.0.8"

from os import path
from sys import argv
import plistlib
import xml.etree.ElementTree as ET
import datetime
import logging.handlers
import requests

APPNAME = "PatchManager"
LOGLEVEL = logging.DEBUG

__all__ = [APPNAME]

logger = logging.getLogger(APPNAME)

def setup_logging():
    """Defines a nicely formatted logger"""

    print("logging")
    LOGFILE = "/usr/local/var/log/%s.log" % APPNAME

    logger = logging.getLogger(APPNAME)
    ch = logging.handlers.TimedRotatingFileHandler(
        LOGFILE, when="D", interval=1, backupCount=7
    )
    ch.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(ch)
    logger.setLevel(LOGLEVEL)

def main():
    setup_logging()
    logger.info("Start")
    print(argv)

    # get prefs
    plist = path.expanduser(
        "~/Library/Preferences/com.github.autopkg.plist"
    )
    fp = open(plist, "rb")
    prefs = plistlib.load(fp)
    base = prefs["JSS_URL"] + "/JSSResource/"
    # because we only operate on scripts creeate a URL for the endpoint
    scriptsURL = f"{prefs['JSS_URL']}/JSSResource/scripts"
    # for the whole list JSON is handier so
    hdrs = {"Accept": "application/json"}
    auth = (prefs["API_USERNAME"], prefs["API_PASSWORD"])
    logger.debug("Prefs loaded")

    # main routine
    ret = requests.get(scriptsURL, auth=auth, headers=hdrs)
    if ret.status_code != 200:
        print("script list get failed: %s" % ret.status_code)
        exit()

    # main loop
    for script in ret.json()['scripts']:
        idn = script['id']
        print(f"{idn}: {script['name']}")
        # we want XML so don't set a header
        ret = requests.get(f"{scriptsURL}/id/{idn}", auth=auth)
        if ret.status_code != 200:
            print(f"script get failed: {ret.status_code} : {ret.url}")
            exit()
        xml = ret.text
        root = ET.fromstring(xml)
        text = root.findtext('script_contents')
        if not text:
            print("damn")
        # print(text)

if __name__ == '__main__':
    main()

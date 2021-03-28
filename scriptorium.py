#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "1.0.8"

from os import path
from sys import argv
import argparse
import plistlib
import xml.etree.ElementTree as ET
import datetime
import logging.handlers
import requests

LOGLEVEL = logging.DEBUG
 
# where to stash the XML files
xml_dir = "~/store/scriptorium/xml"

# where to stash the script files
sh_dir = "~/store/scriptorium/shell"

__all__ = [__name__]

logger = logging.getLogger(__name__)

class Jamf():
    """ Exists to carry some variables for talking to JPC"""

    def __init__(self):
        self.scriptsURL = ""
        self.auth = ""
        self.hdrs = ""
        self.cookies = ""


class Parser():
    """ our command line argument parser """

    def __init__(self):
        self.parser = argparse.ArgumentParser()


class Scripts():

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

    def main(self):
        self.setup_logging()
        logger.info("Start")
        jpc = Jamf()
        timmy = Parser()
        args = timmy.parse(sys.argv())
        # get prefs
        plist = path.expanduser(
            "~/Library/Preferences/com.github.autopkg.plist"
        )
        fp = open(plist, "rb")
        prefs = plistlib.load(fp)
        base = prefs["JSS_URL"] + "/JSSResource/"
        # because we only operate on scripts create a URL for the endpoint
        jpc.scriptsURL = f"{prefs['JSS_URL']}/JSSResource/scripts"
        # for the whole list JSON is handier so
        jpc.hdrs = {"Accept": "application/json"}
        jpc.auth = (prefs["API_USERNAME"], prefs["API_PASSWORD"])
        logger.debug("Prefs loaded")

        # main routine
        ret = requests.get(jpc.scriptsURL, auth=jpc.auth, headers=jpc.hdrs)
        if ret.status_code != 200:
            print("script list get failed: %s" % ret.status_code)
            exit()

        # main loop
        for script in ret.json()['scripts']:
            idn = script['id']
            print(f"{idn}: {script['name']}")
            # we want XML so don't set a header
            ret = requests.get(f"{jpc.scriptsURL}/id/{idn}", auth=jpc.auth)
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
    Scripts.main(argv)

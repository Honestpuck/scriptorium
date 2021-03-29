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
xml_dir = "~/work/test/xml"

# where to stash the script files
sh_dir = "~/work/test/scripts"

__all__ = [__name__]

logger = logging.getLogger(__name__)

class Jamf():
    """ Exists to carry some variables for talking to JPC"""

    def __init__(self):
        self.scriptsURL = ""
        self.auth = ""
        self.hdrs = ""
        self.cookies = ""


class Scripts():

    def setup_logging():
        """Defines a nicely formatted logger"""

        LOGFILE = "/usr/local/var/log/%s.log" % __name__

        logger = logging.getLogger(__name__)
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

    def do_list(args, jpc):
        """ subcommand `list` """
        ret = requests.get(jpc.scriptsURL, auth=jpc.auth, headers=jpc.hdrs)
        if ret.status_code != 200:
            print("script list get failed with http error: %s" % 
                ret.status_code)
            exit(1)
        for script in ret.json()['scripts']:
            idn = script['id']
            name = script['name']
            print(f"{idn}:\t{name}")
        exit()

    def do_out(args, jpc):
        """ subcommand `out` """
        ret = requests.get(jpc.scriptsURL, auth=jpc.auth, headers=jpc.hdrs)
        if ret.status_code != 200:
            print("script list get failed with http error: %s" % 
                ret.status_code)
            exit(1)
        for script in ret.json()['scripts']:
            idn = script['id']
            name = script['name']
            # we want XML so don't set a header
            ret = requests.get(f"{jpc.scriptsURL}/id/{idn}", auth=jpc.auth)
            if ret.status_code != 200:
                print(f"script get failed: {ret.status_code} : {ret.url}")
                exit(1)
            xml = ret.text
            root = ET.fromstring(xml)
            text = root.findtext('script_contents')
            xml_filepath = f"{jpc.xml_out}/{name}"
            sh_filepath = f"{jpc.sh_out}/{name}"
            if args.force or not path.isfile(xml_filepath):
                print(f"Writing XML {name}")
                with open(xml_filepath, "w") as fp:
                    fp.write(xml)
            else:
                print(f"XML {name} exists")
            if args.force or not path.isfile(sh_filepath):
                print(f"Writing script {name}")
                with open(sh_filepath, "w") as fp:
                    fp.write(text)
            else:
                print(f"Script {name} exists")
        exit()

    def do_in(args, jpc):
        print("in not implemented")
        exit()

    def do_change(args, jpc):
        print("change not implemented")
        exit()

    def do_rm(args, jpc):
        print("rm not implemented")
        exit()

    def do_add(args, jpc):
        print("add not implemented")
        if args.filename:
            print(args.filename)
        exit()

    def command_parser():
        "build our command line parser"
        parser = argparse.ArgumentParser(
            epilog="for command help: `scriptorium <command> -h`")
        subparsers = parser.add_subparsers(description="", required=True)

        parser_ls = subparsers.add_parser('list',
                        help="lists all scripts on the server")
        parser_ls.set_defaults(func=Scripts.do_list)

        # create parser for `out`
        parser_out = subparsers.add_parser('out', 
                        help="pulls all scripts out of the server")
        parser_out.add_argument("-f", "--force", 
                        help="force overwrite of existing script",
                        action="store_true")
        parser_out.set_defaults(func=Scripts.do_out)
        
        # create parser for 'in'
        parser_in = subparsers.add_parser('in', 
                        help="add new or changed scripts and commit")
        parser_in.add_argument("-p", "--push", 
                        help="do a git push after commit",
                        action="store_true")
        parser_in.set_defaults(func=Scripts.do_in)

        # create parser for `change`
        parser_ch = subparsers.add_parser('change',
                        help="change the name of a script")
        parser_ch.add_argument("name", help="current name of script")
        parser_ch.add_argument("new", help="new name of script")
        parser_ch.set_defaults(func=Scripts.do_change)

        # create parser for `rm`
        parser_rm = subparsers.add_parser('remove', help="remove (or delete) script from system")
        parser_rm.add_argument("name", help="name of script to remove")
        parser_rm.set_defaults(func=Scripts.do_rm)

        # create parser for `add`
        parser_add = subparsers.add_parser('add', help="add script to system")
        parser_add.add_argument("-f", "--filename", help="name of new script")
        parser_add.add_argument("-c", "--category", help="category of script")
        parser_add.add_argument("-n", "--notes")
        group = parser_add.add_mutually_exclusive_group()
        group.add_argument("-a", "--after", 
            help="run script with priority 'after'", action="store_true")
        group.add_argument("-b", "--before", 
            help="run script with priority 'before'", action="store_true")
        group.add_argument("-r", "--reboot", 
        help="run script at reboot", action="store_true")
        parser_add.add_argument("-z", "--zero", help="zero parameters for script")
        parser_add.set_defaults(func=Scripts.do_add)
        
        return parser

    def main(self):
        Scripts.setup_logging()
        logger.info("Start")
        jpc = Jamf()
        # sanity check
        jpc.xml_out = path.expanduser(xml_dir)
        jpc.sh_out = path.expanduser(sh_dir)
        if not path.isdir(jpc.xml_out):
            print ("directory {jpc.xml_out} does not exist")
            exit(1)
        if not path.isdir(jpc.sh_out):
            print ("directory {jpc.sh_out} does not exist")
            exit(1)
        # get prefs
        plist = path.expanduser(
            "~/Library/Preferences/com.github.autopkg.stage.plist"
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

        parser = Scripts.command_parser()
        # handle no arguments on command line
        if len(argv) == 1:
            print("Missing subcommand")
            parser.print_help()
            exit()
        args = parser.parse_args()
        # we never return from below call
        if args:
            args.func(args, jpc)
        else:
            exit

        ret = requests.get(jpc.scriptsURL, auth=jpc.auth, headers=jpc.hdrs)
        if ret.status_code != 200:
            print("script list get failed: %s" % ret.status_code)
            exit()
        for script in ret.json()['scripts']:
            idn = script['id']
            name = script['name']
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

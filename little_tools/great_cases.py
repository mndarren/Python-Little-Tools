#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: great_cases.py
.. created_by:: Darren Xie
.. created_on:: 12/4/2020

Collect great use cases
"""
import os
import re
import argparse
import cx_Oracle
import sys
from codecs import open
from datetime import datetime
from glob import glob
from hashlib import md5

ENV_RE = re.compile(r'\$ENV\{(.+?)}')
PERCENT_RE = re.compile(r'%(.+?)%')


class GreatCases:
    """
    Collect great use cases
    """
    def load_env(self, path_file: str):
        """
        Load environment config files
        :param path_file: Input file name with related path
        """
        try:
            with open(path_file, 'r') as in_fh:
                for cur_line in in_fh:
                    cur_line = cur_line.strip()
                    if cur_line.startswith('#'):
                        continue
                    if '=' not in cur_line:
                        continue
                    stripped_list = cur_line.split('=', 1)  # split from the 1st '=' mark
                    key = stripped_list[0].strip()
                    value = stripped_list[1].strip().replace('\\', '/')

                    if '%' in value:
                        try:
                            while '%' in value:
                                try_k = re.search(PERCENT_RE, value).group(1)
                                value = re.sub(PERCENT_RE, os.environ[try_k].replace('\\', '/'), value, 1)
                        except Exception:
                            raise Exception(f"{try_k} not defined")
                    os.environ[key] = value.replace('/', '\\')
        except IOError:
            raise IOError(f"IOError: open {path_file}\n")

    def assign_opt(self, opt):
        """
        Update argument from the command line with environment varriable value.
        The reason to use loop here is there are more than one $ENV pieces in opt
        :param opt: Passed in the argument value
        :return:  Updated the argument value
        """
        while ENV_RE.search(str(opt)):
            try_k = re.search(ENV_RE, str(opt)).group(1)
            opt = re.sub(ENV_RE, os.environ[try_k].replace('\\', '/'), str(opt), 1)
        return opt.replace('/', '\\') if '/' in str(opt) else opt

    def greatest_filename(self, filename):
        """
        Get greatest filename
        :param filename: input file name
        :return: greatest filename
        """
        mtime = os.stat(filename)[9]
        time_stamp = datetime.fromtimestamp(mtime).strftime("%y%m%d %H:%M")
        print(f"Modify time: {time_stamp}")
        file_list = glob(str(filename))
        # Sort by mtime
        # file_list.sort(key=os.path.getmtime, reverse=True)
        file_list = sorted(file_list, key=os.path.getmtime)
        greates_file = ''
        for file_item in file_list:
            if file_item > greates_file:
                greates_file = file_item
        return greates_file

    def get_opt(self):
        """
        Get argument values
        :return: argument values list
        """
        parser = argparse.ArgumentParser(description='Process command parameters.', add_help=False)
        parser.add_argument('-d', type=str, help='Input date')
        parser.add_argument('-h', action='store_true', help='Display the usage')

        opt_d, opt_h = None, None

        try:
            args = parser.parse_args(sys.argv[1:])
            opt_d, opt_h = args.d, args.h
        except argparse.ArgumentError as e:
            print(str(e))
        print(f"opt_d={opt_d}, opt_h={opt_h}")
        return [opt_d, opt_h]

    def get_file_md5(self, file_name):
        """
        Generate a md5 hash code for an input file
        :param file_name: Input file
        :return: md5 checksum number
        """
        try:
            with open(file_name, 'rb') as in_fh:
                content = in_fh.read()
        except IOError as e:
            raise IOError(f"Cannot open {file_name}: {e.errno}")
        return md5(content).hexdigest()

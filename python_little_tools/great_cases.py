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
import sys
from codecs import open
from datetime import datetime, date, timedelta
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

    def date_conversion(self):
        """
        Collect date conversion approaches
        :return: target date
        """
        # from timestamp to YYYYMMDD
        # file_date = datetime.fromtimestamp(path_file.stat().st_mtime).strftime("%Y%m%d")
        # "20200908" - 12 days = "20200827"
        input_date = "20200908"
        d_date = date(int(input_date[:4]), int(input_date[4:6]), int(input_date[-2:]))
        t_date = d_date - timedelta(days=12)
        target_date = str(t_date).replace('-', '')

        return target_date

    def sort_int_list_by_occur_times(self, items):
        """
        Example: [1, 3, 1, 5, 7, 8, 5, 9, 4, 9, 4, 1]
        sorted = [3, 7, 8, 4, 4, 5, 5, 9, 9, 1, 1, 1]
        :param items: input integer list
        :return: sorted list
        """
        group_dict = {}
        return_list = []
        for num in items:
            if num in group_dict:
                group_dict[num] += 1
            else:
                group_dict[num] = 1
        group_dict = {k: v for k, v in sorted(group_dict.items(), key=lambda x: (x[1], x[0]))}
        for k, v in group_dict.items():
            for i in range(v):
                return_list.append(k)
        return return_list

    def coin_toss_possibility(self, times: int):
        """
        Suppose a coin is tossed 21 times in a row with equal probability of heads and tails.
        What is the probability that the coin is facing the same way 3 times in a row
        (that is 3 heads in a row or 3 tails in a row) exactly once in the 21 tosses?
        Algorithm:
        :return:
        """
        import itertools
        total = 0
        count_000_111 = 0
        with open('temp_coin.txt', 'w') as out_fh:
            for str1 in map(''.join, itertools.product('01', repeat=times)):
                if self.check_string(str1, times):
                    count_000_111 += 1
                    out_fh.write(f"{str1}\n")
                total += 1
        print(f"tosses = {times}, total = {total}, containing 000 or 111 exactly once = {count_000_111}")

    def check_string(self, str1, times):
        count = 0
        for i in range(times-3):
            if ('000' in str1[i:i+3] and '000' not in str1[i+1:] and '111' not in str1[i+1:]
                and '000' not in str1[:i+2] and '111' not in str1[:i+2]) \
                    or ('111' in str1[i:i+3] and '111' not in str1[i+1:] and '000' not in str1[i+1:]
                        and '111' not in str1[:i+2] and '000' not in str1[:i+2]):
                count += 1
                if count > 1:
                    return False
        if count == 1:
            return True
        return False


if __name__ == "__main__":
    # items = [1, 3, 1, 5, 7, 8, 5, 9, 4, 9, 4, 1]
    # return_list = GreatCases().sort_int_list_by_occur_times(items)
    # print(return_list)
    GreatCases().coin_toss_possibility(21)

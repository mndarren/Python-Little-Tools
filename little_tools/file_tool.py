#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: file_tool.py
.. created_by:: Darren Xie
.. created_on:: 11/23/2020

Collect File action tools
"""
import os
import shutil
from glob import glob
from pathlib import Path
from datetime import datetime


class FileTool:
    """Contain all tools for file action"""
    @staticmethod
    def rename_all_ext(dir_path=None):
        """
        Change all files ext name in a dir
        """
        dir = 'default_path'
        if dir_path:
            dir = dir_path
        new_ext = '.sql'
        os.chdir(dir)
        for count, filename in enumerate(os.listdir(dir)):
            pre, ext = os.path.splitext(filename)
            os.rename(filename, pre + new_ext)

    @staticmethod
    def cleanup_folder(folder_path=None):
        """Delete all from a folder"""
        folder = folder_path if folder_path else 'Default_folder'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.chmod(file_path, 0o664)
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path} {e}")

    def walk_all_files_dirs(self, root_path):
        """
        Walk through all files and subdirectories in root path
        Delete files whose mtime <= target data & remove empty folders
        """
        recursive = True
        file_mask = 'Filename_*_[1-9]*'
        target_date = '20201217'
        preserve_sub = False

        for dir_name, subdir_list, file_list in os.walk(root_path):
            if not recursive and dir_name != root_path:
                continue
            files_mask = []
            if file_mask:
                files_mask = glob(str(Path(dir_name).joinpath(file_mask)))
            for fname in file_list:
                path_file = Path(dir_name).joinpath(fname)
                if not file_mask or str(path_file) in files_mask:
                    # get mtime with format YYYYMMDD
                    file_date = datetime.fromtimestamp(path_file.stat().st_mtime).strftime("%Y%m%d")
                    if file_date <= target_date:
                        os.unlink(path_file)
            # remove empty folders
            if not len(subdir_list) and not len(file_list):
                if not preserve_sub:
                    os.rmdir(dir_name)

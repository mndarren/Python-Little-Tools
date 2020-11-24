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


class FileTools:
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

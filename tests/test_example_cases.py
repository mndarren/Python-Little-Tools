#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: test_example_cases.py
.. created_by:: Darren Xie
.. created_on:: 12/01/2020

Test example cases
"""
import unittest
import cx_Oracle
from little_tools.file_tool import FileTool
from unittest.mock import patch, MagicMock
from io import StringIO


class TestExampleCases(unittest.TestCase):
    def test_return_code(self):
        with self.assertRaises(SystemExit) as se:
            FileTool().cleanup_folder()
        self.assertEqual(se.exception.code, 1)

    def test_stdout(self):
        cursor = MagicMock(cx_Oracle.Cursor)
        cursor.execute = MagicMock(return_value='')
        with patch('sys.stdout', new=StringIO()) as out:
            FileTool().cleanup_folder()
            self.assertEqual('something' in out.getvalue())

    @patch('cx_Oracle.connect')
    def test_mock(self, mock_conn):
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__\
            .return_value.fetchone.reutrn_value = ()
        cursor = mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
        cursor.fetchone.side_effect = [('Subject1', 'Body1'), 'Darren.Xie@gmail.com', '']


if __name__ == '__main__':
    unittest.main()

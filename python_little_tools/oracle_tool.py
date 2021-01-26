#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. current_module:: oracle_tool.py
.. created_by:: Darren Xie
.. created_on:: 11/23/2020

Collect Oracle DB tools
"""
import os
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Dict
import logging
import cx_Oracle

ENTRY_NAME1 = 'MyEntry1'  # this name should be listed in your tnsnames.ora file
ENTRY_NAME2 = 'MyEntry2'  # this name should be listed in your tnsnames.ora file
USER_ID = ''
PASSWORD = ''
WALLET_PASS = b'Wallet_Pass0XXX'  # this value must be byte string

JAVA_HOME = ''  # Java home path
CLIENT_PATH = ''  # Oracle Client Path
WALLET_PATH = ''  # Choose a path to store Oracle Wallet
CMD_CREATE = f'mkstore -wrl {WALLET_PATH} -create'

# For connection only
HOST = ''
PORT = ''
SID = ''
SERVICE_NAME = ''


class OracleTool:
    """
    Please confirm ENTRY_NAME in list of tnsnames.ora file;
    Please make sure WALLET_PATH correct in sqlnet.ora file.
    """
    query = 'SELECT name, type FROM SOME_TABLE  FETCH NEXT 5 ROWS ONLY'

    def build_ora_wallet(self):
        os.environ['JAVA_HOME'] = JAVA_HOME
        os.chdir(CLIENT_PATH)
        logger = self.get_log('build_ora_wallet')

        # Create Wallet
        p = Popen(CMD_CREATE, stdin=PIPE, stdout=PIPE, shell=True)
        p.communicate(input=WALLET_PASS * 2)  # need to repeat input
        p.terminate()
        logger.info(f"Created Wallet in {WALLET_PATH}")

        # Insert WALLET ENTRY
        entries = [ENTRY_NAME1, ENTRY_NAME2]
        for entry in entries:
            cmd_entry = f'mkstore -wrl {WALLET_PATH} -createCredential {entry} {USER_ID} {PASSWORD}'
            p = Popen(cmd_entry, stdin=PIPE, stdout=PIPE, shell=True)
            p.communicate(input=WALLET_PASS)  # need to repeat input
            p.terminate()
        logger.info(f"Inserted Wallet Entry.")

        # Test WALLET
        try:
            conn_str = f'/@{ENTRY_NAME1}'
            with cx_Oracle.connect(conn_str) as conn, conn.cursor() as cursor:
                cursor.execute(self.query)
                while row := cursor.fetchone():
                    logger.info(row)
        except cx_Oracle.DatabaseError as e:
            logger.error(str(e))

    def ora_conn(self):
        """
        Simply connect Oracle DB
        """
        logger = self.get_log('ora_conn')
        try:
            dsn = cx_Oracle.makedsn(host=HOST, port=PORT, sid=SID, service_name=SERVICE_NAME)
            with cx_Oracle.connect(USER_ID, PASSWORD, dsn) as conn, conn.cursor() as cursor:
                cursor.execute(self.query)
                while row := cursor.fetchone():
                    logger.info(row)
        except cx_Oracle.DatabaseError as e:
            logger.error(str(e))

    def get_log(self, log_name):
        """
        Get a logger.
        :param log_name: This is log file name
        :return: a logger
        """
        log_path = Path(__file__).absolute().parents[0]
        log_file = log_path.joinpath(f'{log_name}.log')
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%asctimes - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        return logging.getLogger(log_name)

    def assign_field_value_to_var(self):
        """
        Assign field values from DB to variables
        Just code block
        """
        name, type1 = None, None
        try:
            conn_str = f'/@{ENTRY_NAME1}'
            with cx_Oracle.connect(conn_str) as conn, conn.cursor() as cursor:
                cursor.execute(self.query)
                columns = ['name', 'type1']
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                record: [Dict] = cursor.fetchone()
                if record:
                    for k, v in record.items():
                        if v:
                            exec(f"{k} = '{v}")
        except cx_Oracle.DatabaseError as e:
            logger.error(str(e))

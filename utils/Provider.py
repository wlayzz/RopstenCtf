#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*
import os

from dotenv import load_dotenv
from web3 import Web3
from utils.Utils import write_provider_key_to_env_file


class Provider:
    BLOCKCHAIN_URL = 'https://ropsten.infura.io/v3/'

    def __init__(self, logger):
        self.logger = logger

    def initiate_provider(self):
        load_dotenv()
        self.provider_key = os.getenv("provider_key")
        self.address = os.getenv("address")
        if self.provider_key:
            self.web3 = Web3(Web3.HTTPProvider(self.BLOCKCHAIN_URL + self.provider_key))
            self.check_connection()
        else:
            self.logger.error("You must import a provider id first, use --provider-key to import provider key. Use https://infura.io to create a project and get your key.")
            exit()

    def check_connection(self):
        if self.web3.isConnected():
            self.logger.success('Connected to ropsten network')
        else:
            self.logger.error('Cannot connect to ropsten network, check your connection')
            exit()

    def import_key(self, provider_key):
        write_provider_key_to_env_file(provider_key, self.logger)
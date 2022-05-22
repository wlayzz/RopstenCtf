#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

import os
import secrets
from eth_account import Account
from dotenv import load_dotenv

class Wallet:
    def __init__(self, provider, logger):
        self.provider = provider
        self.logger = logger

    def initiate_account(self):
        load_dotenv()
        self.private_key = os.getenv("private_key")
        self.address = os.getenv("address")
        if(self.private_key and self.address):
            acnt = self.provider.web3.eth.account.privateKeyToAccount(self.private_key)
            self.provider.web3.eth.defaultAccount = acnt.address
            self.account_address = acnt.address
        else:
            self.logger.error("You have to generate or import a wallet first, use --import-key to import private key")

    def generate_wallet(self):
        priv = secrets.token_hex(32)
        self.private_key = "0x" + priv
        self.address = Account.from_key(self.private_key).address
        self.__store_key()
        self.logger.info("You can claim $rETH unsing this faucet: https://faucet.egorfine.com/")

    def __store_key(self):
        with open('.env', 'w') as f:
            f.write(f"private_key={self.private_key}\n")
            f.write(f"address={self.address}")
        self.logger.info(f"Your secret key is {self.private_key} (keep this secret)")
        self.logger.info(f"Your public adress is {self.address}")
        self.logger.info(f"These informations are stored in .env file and will be used for smart contract interactions")

    def get_balance(self):
        self.logger.info("You can claim $rETH unsing this faucet: https://faucet.egorfine.com/")
        balance = self.provider.web3.eth.get_balance(self.address)
        balance /= pow(10,18)
        self.logger.success(f"Balance: {balance} $rETH")

    def import_key(self, import_key):
        self.private_key = import_key
        self.address = Account.from_key(self.private_key).address
        self.__store_key()

    def get_info(self):
        self.get_address()
        self.get_balance()

    def get_address(self):
        self.logger.success(f"Public adress: {self.address}")
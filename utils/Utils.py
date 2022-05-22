#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

import os

from dotenv import load_dotenv


def write_private_key_to_env_file(wallet):
    load_dotenv()
    provider_key = os.getenv('provider_key')
    with open('.env', 'w') as f:
        f.write(f"provider_key={provider_key}\n")
        f.write(f"private_key={wallet.private_key}\n")
        f.write(f"address={wallet.address}\n")
    wallet.logger.info(f"Your secret key is {wallet.private_key} (keep this secret)")
    wallet.logger.info(f"Your public adress is {wallet.address}")
    wallet.logger.info("These informations are stored in .env file and will be used for smart contract interactions")


def write_provider_key_to_env_file(provider_key, logger):
    load_dotenv()
    private_key = os.getenv("private_key")
    address = os.getenv("address")
    with open('.env', 'w') as f:
        f.write(f"provider_key={provider_key}\n")
        f.write(f"private_key={private_key}\n")
        f.write(f"address={address}\n")
    logger.info('Provider key saved in .env file')
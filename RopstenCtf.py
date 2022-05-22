#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

import argparse
from rich.console import Console
from utils.Provider import Provider
from utils.Contract import Contract
from utils.Logger import Logger
from utils.Wallet import Wallet


def arg_parse():
    parser = argparse.ArgumentParser(description="Tools")

    # Required arguments
    parser._positionals.title = "{}Required arguments{}".format("\033[1;32m", "\033[0m")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity")

    wallet_mode = argparse.ArgumentParser(add_help=False)
    wallet_mode.add_argument("--info", dest="wallet_info", action="store_true", help="Get wallet information")
    wallet_mode.add_argument("--generate", dest="generate", action="store_true", help="Generate new wallet")
    wallet_mode.add_argument("--balance", dest="balance", action="store_true", help="Get wallet balance")
    wallet_mode.add_argument("--import-key", dest="import_key", action="store", help="Import private key")
    wallet_mode.add_argument("--provider-key", dest="provider_key", action="store", help="Import provider key")

    contract_mode = argparse.ArgumentParser(add_help=False)
    contract_mode.add_argument("--address", dest="contract_address", action="store", help="Address of smart contract")
    contract_mode.add_argument("--info", dest="contract_info", action="store_true", help="Informations of smart contract")
    contract_call_action = contract_mode.add_mutually_exclusive_group(required=False)
    contract_call_action.add_argument("--call", dest="contract_call", action="store_true", help="Call function of smart contract")
    contract_call_action.add_argument("--write", dest="contract_write", action="store_true", help="Call function of smart contract")
    contract_call_action.add_argument("--deploy", dest="contract_deploy", action="store_true", help="Deploy a smart contract")
    contract_call_action.add_argument("--compile", dest="contract_compile", action="store_true", help="Compile a smart contract")
    contract_call = contract_call_action.add_argument_group("Function to call with parameters")
    contract_call.add_argument("-fc", "--function", dest="contract_function", action="store", help="Name of function to call")
    contract_call.add_argument("-p", "--parameters", dest="contract_function_parameters", action="store", help="Parameters of function to call")
    contract_call.add_argument("-f", "--file", dest="contract_source", action="store", help="Path of smart contract to deploy")
    contract_call.add_argument("-a", "--abi", dest="contract_abi", action="store", help="abi of smart contract")
    contract_call.add_argument("-e", "--ether", dest="contract_ether", action="store", default=0, help="abi of smart contract")

    subparsers = parser.add_subparsers(help="actions", dest="action")
    subparsers.add_parser("wallet", parents=[wallet_mode], help="generate new wallet")
    subparsers.add_parser("contract", parents=[contract_mode], help="interact with smart contract")

    options = parser.parse_args()

    return options


if __name__ == "__main__":
    options = arg_parse()
    console = Console()
    logger = Logger(console, options.verbose)

    # Initialisation
    provider = Provider(
        logger=logger
    )
    if options.action == "wallet" and options.provider_key:
        provider.import_key(options.provider_key)
    provider.initiate_provider()

    wallet = Wallet(
        provider=provider,
        logger=logger
    )

    if options.action == "wallet":
        if options.generate:
            wallet.generate_wallet()
        if options.import_key:
            wallet.import_key(options.import_key)
    wallet.initiate_account()

    if options.action == "wallet":
        if options.wallet_info:
            wallet.get_info()
        if options.balance:
            wallet.get_balance()

    if options.action == "contract":
        contract = Contract(
            logger=logger,
            wallet=wallet
        )
        if options.contract_address:
            contract.init_contract_with_adress(options.contract_address, options.contract_abi)
        if options.contract_compile and options.contract_source:
            contract.compile(options.contract_source)
        if options.contract_deploy and options.contract_source and options.contract_deploy_name:
            contract.deploy(options.contract_source)
        if options.contract_info:
            contract.all_functions()
        if options.contract_call:
            contract.call_function(options.contract_function, options.contract_function_parameters)
        if options.contract_write:
            contract.write_function(options.contract_function, options.contract_function_parameters, options.contract_ether)

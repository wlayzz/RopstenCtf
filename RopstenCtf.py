#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

import argparse
from rich.console import Console

from utils.Crypto import Crypto
from utils.Provider import Provider
from utils.Contract import Contract
from utils.Logger import Logger
from utils.Transaction import Transaction
from utils.Wallet import Wallet

def banner():
    art = """
  ___             _            ___ _    __ 
 | _ \___ _ __ __| |_ ___ _ _ / __| |_ / _|
 |   / _ | '_ (_-|  _/ -_| ' | (__|  _|  _|
 |_|_\___| .__/__/\__\___|_||_\___|\__|_|   by @Wlayzz
         |_|                               
         """
    print(art)

def arg_parse():
    banner()
    parser = argparse.ArgumentParser(description="RopstenCtf is an easy tool to interact with the ethereum ropsten network for ctf purpose and more.")

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
    contract_call_action.add_argument("--view", dest="contract_view", action="store_true", help="Call function of smart contract")
    contract_call_action.add_argument("--call", dest="contract_call", action="store_true", help="Call function of smart contract")
    contract_call_action.add_argument("--deploy", dest="contract_deploy", action="store_true", help="Deploy a smart contract")
    contract_call_action.add_argument("--compile", dest="contract_compile", action="store_true", help="Compile a smart contract")
    contract_call = contract_call_action.add_argument_group("Function to call with parameters")
    contract_call.add_argument("-fc", "--function", dest="contract_function", action="store", help="Name of function to call")
    contract_call.add_argument("-p", "--parameters", dest="contract_function_parameters", action="store", help="Parameters of function to call")
    contract_call.add_argument("-f", "--file", dest="contract_source", action="store", help="Path of smart contract to deploy")
    contract_call.add_argument("-a", "--abi", dest="contract_abi", action="store", help="abi of smart contract")
    contract_call.add_argument("-e", "--ether", dest="contract_ether", action="store", default=0, type=int, help="Amount of ether send in transaction, default is 0")

    brute_force = argparse.ArgumentParser(add_help=False)
    brute_force.add_argument('-r', '--range', dest="bf_range", action="store", required=True, help="Range of value to brute force, exemple: 1-100, 15-70")
    brute_force.add_argument('-v', '--value', dest="bf_value", action="store", required=True, help="Value to match with brute force")

    crypto_mode = argparse.ArgumentParser(add_help=False)
    crypto_subparser = crypto_mode.add_subparsers(help="cryto actions", dest="crypto_action")
    crypto_subparser.add_parser("bruteforce", parents=[brute_force], help="Brute force keccak256 hash")
    crypto_mode.add_argument("-n", dest="crypto_input", action="store", help="Input to hash")
    input_type_options = crypto_mode.add_mutually_exclusive_group(required=False)
    input_type_options.add_argument("--uint8", dest="crypto_type", action="store_const", const='uint8', help="Type of input to hash")
    input_type_options.add_argument("--uint24", dest="crypto_type", action="store_const", const='uint24',  help="Type of input to hash")

    transaction_mode = argparse.ArgumentParser(add_help=False)
    transaction_mode_input = transaction_mode.add_mutually_exclusive_group(required=False)
    transaction_mode_input.add_argument("--txn", dest="transaction_txn", action="store", help="Hash of transaction")
    transaction_mode_input.add_argument("--block-id", dest="transaction_block_id", action="store", help="Block id")
    transaction_mode.add_argument("--block-info", dest="transaction_block_info", action="store_true", help="Retrieve informations of block")
    transaction_mode.add_argument("--all", dest="transaction_all", action="store_true", default=False, help="Print all informations, hidden informations are represented by ...")

    subparsers = parser.add_subparsers(help="actions", dest="action")
    subparsers.add_parser("wallet", parents=[wallet_mode], help="manage wallet")
    subparsers.add_parser("contract", parents=[contract_mode], help="interact with smart contract")
    subparsers.add_parser("crypto", parents=[crypto_mode], help="crypto utils for ethereum smart contract")
    subparsers.add_parser("transaction", parents=[transaction_mode], help="retrieve informations of a transaction")

    options = parser.parse_args()

    return options


if __name__ == "__main__":
    options = arg_parse()
    console = Console()
    logger = Logger(console, options.verbose)

    if options.action == "crypto":
        crypto = Crypto(
            logger=logger
        )

        if options.crypto_input:
            crypto.get_keccak_value(options.crypto_input, options.crypto_type)
        if options.crypto_action == "bruteforce":
            if options.bf_range and options.bf_value:
                crypto.bf_keccak256(options.bf_range, options.bf_value, options.crypto_type)
    else:
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
            if options.contract_deploy and options.contract_source:
                contract.deploy(options.contract_source, options.ether)
            if options.contract_info:
                contract.all_functions()
            if options.contract_view:
                contract.call_function(options.contract_function, options.contract_function_parameters)
            if options.contract_call:
                contract.write_function(options.contract_function, options.contract_function_parameters, options.contract_ether)

        if options.action == "transaction":
            transaction = Transaction(
                logger=logger,
                wallet=wallet,
            )
            if options.transaction_txn or options.transaction_block_id:
                if options.transaction_block_info:
                    if options.transaction_txn:
                        transaction.get_block_info_by_txn(options.transaction_txn, options.transaction_all)
                        exit()
                if options.transaction_block_id:
                    transaction.get_block_info_by_block_id(options.transaction_block_id, options.transaction_all)
                    exit()
            if options.transaction_txn:
                transaction.get_transaction_info(options.transaction_txn)
                exit()

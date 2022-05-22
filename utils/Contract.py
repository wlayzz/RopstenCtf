#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : EthereumCtfTool.py
# Author             : Wlayzz (@wlayzz)
# Date created       : 21 May 2022
# Python Version     : 3.*

import requests
from web3 import exceptions
import os

ABI_ENDPOINT = 'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address='
RAW_FORMAT = '&format=raw'

class Contract:
    def __init__(self, wallet, logger):
        self.wallet = wallet
        self.logger = logger

    def init_contract_with_adress(self, address, abi=None):
        self.address = address
        self.logger.info(f'Inspect contract at https://ropsten.etherscan.io/address/{self.address}')
        if abi is None:
            self.abi = self.__get_abi()
        else:
            with open(abi, 'r') as f:
                self.abi = f.read()
        self.contract = self.wallet.provider.web3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def all_functions(self):
        self.logger.success('List of functions:')
        for f in self.contract.all_functions():
            fname = f.fn_name
            parameters = ''
            for i in f.abi["inputs"]:
                parameter = f"{i['name']}:{i['type']}"
                if i != f.abi["inputs"][-1]:
                    parameter += ', '
                parameters += parameter
            self.logger.list(f"{fname}({parameters})")

    def get_function_parameter_type(self, function, parameter, index):
        for f in self.contract.all_functions():
            if function == f.fn_name:
                if f.abi["inputs"][index]['type'] == 'uint256':
                    return int(parameter)
                if f.abi["inputs"][index]['type'] == 'address':
                    return str(parameter)
                if f.abi["inputs"][index]['type'] == 'bytes32':
                    return bytes(parameter, 'utf-8')


    def __get_abi(self):
        endpoint = '%s%s%s' % (ABI_ENDPOINT, self.address, RAW_FORMAT)
        with self.logger.console.status("[bold green]Fetching abi..."):
            response = requests.get(endpoint)
        self.logger.info(f"Fetching abi done")
        return response.content.decode('utf-8')

    def call_function(self, contract_function, contract_function_parameters):
        function = getattr(self.contract.functions, f'{contract_function}')
        if contract_function_parameters:
            parameter = self.get_function_parameter_type(contract_function, contract_function_parameters, 0)
            function_string = f"{contract_function}({parameter})"
            with self.logger.console.status(f"[bold green]Calling function {function_string}..."):
                try:
                    response = function(parameter).call()
                    self.logger.info(f"Calling function done")
                    self.logger.success(f"Reponse {function_string}: {response}")
                except exceptions.SolidityError as error:
                    self.logger.error(error)
        else:
            function_string = f"{contract_function}()"
            with self.logger.console.status(f"[bold green]Calling function {function_string}..."):
                try:
                    response = function().call()
                    self.logger.info(f"Calling function done")
                    self.logger.success(f"Reponse {function_string}: {response}")
                except exceptions.SolidityError as error:
                    self.logger.error(error)

    def write_function(self, contract_function, contract_function_parameters):
        parameters = []
        function = getattr(self.contract.functions, f'{contract_function}')
        web3 = self.wallet.provider.web3
        nonce = web3.eth.get_transaction_count(self.wallet.address)
        if contract_function_parameters is not None:
            parameters = contract_function_parameters.split(',')
        if len(parameters) == 2:
            parameter1 = self.get_function_parameter_type(contract_function, parameters[0], 0)
            parameter2 = self.get_function_parameter_type(contract_function, parameters[1], 1)
            function_string = f"{contract_function}({parameter1},{parameter2})"
            transaction = function(parameter1, parameter2).buildTransaction({
                'gas': 2000000,
                'gasPrice': web3.toWei('40', 'gwei'),
                'from': self.wallet.address,
                'nonce': nonce
            })
        if len(parameters) == 1:
            parameter = self.get_function_parameter_type(contract_function, contract_function_parameters, 0)
            function_string = f"{contract_function}({parameter})"
            transaction = function(parameter).buildTransaction({
                'gas': 2000000,
                'gasPrice': web3.toWei('40', 'gwei'),
                'from': self.wallet.address,
                'nonce': nonce
            })
        if len(parameters) == 0:
            function_string = f"{contract_function}()"
            transaction = function().buildTransaction({
                'gas': 2000000,
                'gasPrice': web3.toWei('40', 'gwei'),
                'from': self.wallet.address,
                'nonce': nonce
            })

        signed_txn = web3.eth.account.signTransaction(transaction, private_key=self.wallet.private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn = web3.toHex(web3.keccak(signed_txn.rawTransaction))
        self.logger.info(f'Inspect transaction here: https://ropsten.etherscan.io/tx/{txn}')
        with self.logger.console.status(f"[bold green]Sending transaction {function_string}, this can take times..."):
            try:
                response = web3.eth.wait_for_transaction_receipt(txn_hash)
                self.logger.info(f"Transaction done")
                self.logger.success(f"Reponse {function_string}:")
                self.parse_write_response(response)
            except exceptions.SolidityError as error:
                self.logger.error(error)
            except exceptions.TimeExhausted as error:
                self.logger.error(error)

    def parse_write_response(self, response):
        status = response["status"]
        self.logger.debug(response)
        if status == 0:
            self.logger.console.print("\t{}[*]{} Transaction status: {}fail{}".format("[bold blue]", "[/bold blue]", "[bold red]", "[/bold red]"), highlight=False)
        else:
            self.logger.console.print("\t{}[*]{} Transaction status: {}success{}".format("[bold blue]", "[/bold blue]", "[bold green]", "[/bold green]"), highlight=False)

    def deploy(self, contract_source):
        contract_name = self.compile(contract_source)

        with open(f'{contract_name}/{contract_name}.abi', 'r') as f:
            contract_abi = f.read()
        with open(f'{contract_name}/{contract_name}.bin', 'r') as f:
            contract_bin = f.read()

        web3 = self.wallet.provider.web3
        contract_ = web3.eth.contract(
            abi=contract_abi,
            bytecode=contract_bin)

        nonce = web3.eth.get_transaction_count(self.wallet.address)
        transaction = contract_.constructor().buildTransaction({
            'gas': 2000000,
            'gasPrice': web3.toWei('40', 'gwei'),
            'from': self.wallet.address,
            'nonce': nonce
        })

        signed_txn = web3.eth.account.signTransaction(transaction, private_key=self.wallet.private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn = web3.toHex(web3.keccak(signed_txn.rawTransaction))
        self.logger.info(f'Inspect transaction here: https://ropsten.etherscan.io/tx/{txn}')
        with self.logger.console.status(f"[bold green]Deployng contract {contract_name}, this can take times..."):
            try:
                response = web3.eth.wait_for_transaction_receipt(txn_hash)
                self.logger.info(f"Transaction done")
                self.logger.success(f"Reponse deploying contract {contract_name}:")
                self.parse_write_response(response)
            except exceptions.SolidityError as error:
                self.logger.error(error)
            except exceptions.TimeExhausted as error:
                self.logger.error(error)

    def compile(self, contract_source):
        contract_name = contract_source.replace('.sol', '')
        os.system(f'solc --abi --bin {contract_source} -o {contract_name} --overwrite')
        return contract_name
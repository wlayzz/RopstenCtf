import requests
from web3 import exceptions

ABI_ENDPOINT = 'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address='
RAW_FORMAT = '&format=raw'


class Contract:
    def __init__(self, address, wallet, logger):
        self.address = address
        self.wallet = wallet
        self.logger = logger
        self.abi = self.__get_abi()
        self.contract = wallet.provider.web3.eth.contract(
            address=self.address,
            abi=self.abi
        )
        """
        self.transaction = {
            'gasPrice': wallet.provider.web3.eth.gas_price,
            'from': self.wallet.account_address
        }
        """

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

    def __get_abi(self):
        endpoint = '%s%s%s' % (ABI_ENDPOINT, self.address, RAW_FORMAT)
        with self.logger.console.status("[bold green]Fetching abi..."):
            response = requests.get(endpoint)
        self.logger.info(f"Fetching abi done")
        return response.content.decode('utf-8')

    def call_function(self, contract_function, contract_function_parameters):
        function = getattr(self.contract.functions, f'{contract_function}')
        if contract_function_parameters:
            function_string = f"{contract_function}({contract_function_parameters})"
            with self.logger.console.status(f"[bold green]Calling function {function_string}..."):
                try:
                    response = function(contract_function_parameters).call()
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
        function = getattr(self.contract.functions, f'{contract_function}')
        web3 = self.wallet.provider.web3
        nonce = web3.eth.get_transaction_count(self.wallet.address)
        if contract_function_parameters:
            function_string = f"{contract_function}({contract_function_parameters})"
            transaction = function(contract_function_parameters).buildTransaction({
                'gas': 70000,
                'gasPrice': self.wallet.provider.web3.toWei('20', 'gwei'),
                'from': self.wallet.address,
                'nonce': nonce
            })
        else:
            function_string = f"{contract_function}()"
            transaction = function().buildTransaction({
                'gas': 70000,
                'gasPrice': self.wallet.provider.web3.toWei('20', 'gwei'),
                'from': self.wallet.address,
                'nonce': nonce
            })

        signed_txn = web3.eth.account.signTransaction(transaction, private_key=self.wallet.private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn = web3.toHex(web3.keccak(signed_txn.rawTransaction))
        self.logger.info(f'Inspect transaction here: https://ropsten.etherscan.io/tx/{txn}')
        with self.logger.console.status(f"[bold green]Calling function {function_string}, this can take times..."):
            try:
                response = web3.eth.wait_for_transaction_receipt(txn_hash)
                self.logger.info(f"Transaction done")
                self.logger.success(f"Reponse {function_string}:")
                self.parse_write_response(response)
            except exceptions.SolidityError as error:
                self.logger.error(error)

    def parse_write_response(self, response):
        status = response["status"]
        if status == 0:
            self.logger.console.print("\t{}[*]{} Transaction status: {}fail{}".format("[bold blue]", "[/bold blue]", "[bold red]", "[/bold red]"), highlight=False)
        else:
            self.logger.console.print("\t{}[*]{} Transaction status: {}success{}".format("[bold blue]", "[/bold blue]", "[bold green]", "[/bold green]"), highlight=False)
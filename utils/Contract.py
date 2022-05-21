import requests

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

    def call_function(self, contract_call_function, contract_call_function_parameters):
        function = getattr(self.contract.functions, f'{contract_call_function}')
        if contract_call_function_parameters:
            function_string = f"{contract_call_function}({contract_call_function_parameters})"
            with self.logger.console.status(f"[bold green]Calling function {function_string}..."):
                response = function(contract_call_function_parameters).call()
        else:
            function_string = f"{contract_call_function}()"
            with self.logger.console.status(f"[bold green]Calling function {function_string}..."):
                response = function().call()
        self.logger.success(f"Calling function {function_string} done")
        self.logger.success(f"Reponse: {response}")



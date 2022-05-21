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
            address = self.address,
            abi = self.abi
        )
        """
        self.transaction = {
            'gasPrice': wallet.provider.web3.eth.gas_price,
            'from': self.wallet.account_address
        }
        """

    def all_functions(self):
        return self.contract.all_functions()

    def __get_abi(self):
        endpoint = '%s%s%s' % (ABI_ENDPOINT, self.address, RAW_FORMAT)
        self.logger.info(f"Fetching abi: {endpoint}")
        response = requests.get(endpoint)
        return response.content.decode('utf-8')


    def call_function(self, contract_call_function, contract_call_function_parameters):
        function = getattr(self.contract.functions, f'{contract_call_function}')
        if contract_call_function_parameters:
            self.logger.info(f"Call function {contract_call_function}({contract_call_function_parameters})")
            response = function(contract_call_function_parameters).call()
        else:
            self.logger.info(f"Call function {contract_call_function}()")
            response = function().call()
        self.logger.success(f"Reponse: {response}")

from web3 import Web3

class Provider:
    BLOCKCHAIN_URL = 'https://ropsten.infura.io/v3/'

    def __init__(self, project_id, logger):
        self.project_id = project_id
        self.web3 = Web3(Web3.HTTPProvider(self.BLOCKCHAIN_URL + self.project_id))
        self.logger = logger

    def get_http_provider(self):
        return self.web3

    def check_connection(self):
        if(self.web3.isConnected()):
            self.logger.success('Connected to ropsten network')
        else:
            self.logger.error('Cannot connect to ropsten network, check your connection')
            exit()
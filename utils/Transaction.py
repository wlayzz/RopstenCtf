from rich import inspect

class Transaction:
    def __init__(self, logger, wallet):
        self.logger = logger
        self.wallet = wallet
        self.web3 = self.wallet.provider.web3

    def retrieve_block_info(self, txn):
        transaction = self.retrieve_transaction_info(txn)
        blockNumber = transaction['blockNumber']
        return self.web3.eth.get_block(blockNumber)

    def get_block_info(self, txn, print_all):
        block = self.retrieve_block_info(txn)
        if not print_all and 'transactions' in block.__dict__:
            block.__dict__['transactions'] = ['...']
        inspect(block, title=f'Block {block["number"]}', value=False, docs=False)

    def retrieve_transaction_info(self, txn):
        return self.web3.eth.get_transaction(txn)

    def get_transaction_info(self, txn):
        transaction = self.retrieve_transaction_info(txn)
        inspect(transaction, title=f'Transaction {txn}', value=False, docs=False)
from rich import inspect

class Transaction:
    def __init__(self, logger, wallet):
        self.logger = logger
        self.wallet = wallet
        self.web3 = self.wallet.provider.web3

    def retrieve_block_info_by_txn(self, txn):
        transaction = self.retrieve_transaction_info(txn)
        blockNumber = transaction['blockNumber']
        return self.web3.eth.get_block(blockNumber)

    def retrieve_block_info_by_block_id(self, block_id):
        return self.web3.eth.get_block(int(block_id))

    def get_block_info_by_txn(self, txn, print_all):
        block = self.retrieve_block_info_by_txn(txn)
        self.print_block(block, print_all)

    def print_block(self, block, print_all):
        if not print_all and 'transactions' in block.__dict__:
            block.__dict__['transactions'] = ['...']
        inspect(block, title=f'Block {block["number"]}', value=False, docs=False)

    def retrieve_transaction_info(self, txn):
        return self.web3.eth.get_transaction(txn)

    def get_transaction_info(self, txn):
        transaction = self.retrieve_transaction_info(txn)
        inspect(transaction, title=f'Transaction {txn}', value=False, docs=False)

    def get_block_info_by_block_id(self, block_id, transaction_all):
        block = self.retrieve_block_info_by_block_id(block_id)
        self.print_block(block, transaction_all)
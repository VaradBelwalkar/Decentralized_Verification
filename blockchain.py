import web3
import json
from web3 import Web3
from web3 import Account


Account.enable_unaudited_hdwallet_features()

url = "https://sepolia.infura.io/v3/<YOUR_API_KEY>"
registeredInstitutes = {"INSTITUTE_1": 1, "INSTITUTE_2": 2, "INSTITUTE_3": 3}

# Set the default account to a mnemonic phrase
mnemonic_phrase = "YOUR MNEMONIC"  # Replace with your actual mnemonic phrase
web3_instance = Web3(Web3.HTTPProvider(url))

# Get the address of your MetaMask account
account = Account.from_mnemonic(mnemonic_phrase)
address = account.address
nonce = web3_instance.eth.get_transaction_count(address)
# Set the default account in web3.py
web3_instance.eth.defaultAccount = address

class Blockchain:
    def __init__(self, institute):
        self.web3 = web3_instance
        self.institute = institute

        with open('contractDetails.json') as f:
            contract_details = json.load(f)
            contract_address = self.web3.to_checksum_address(contract_details["address"])
            abi = contract_details["abi"]

        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

        if institute in registeredInstitutes.keys():
            print(f"Connected to blockchain with account: {institute}")
        else:
            print(f"Connected to blockchain with default account")

    def addBatchMerkleRoot(self, batch, batchMerkleRoot):
        transaction = self.contract.functions.addBatchMerkleRoot(self.institute, batch, batchMerkleRoot).build_transaction({
            'chainId': 11155111,  # Mainnet chain ID, adjust as needed
            'gas': 220000,  # Adjust gas limit as needed
            'gasPrice': self.web3.to_wei('5', 'gwei'),  # Adjust gas price as needed
            'nonce': nonce
        })
        signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key=account._private_key)

        tx_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        self.web3.eth.wait_for_transaction_receipt(tx_hash)


    def verifyBatchMerkleRoot(self, institute, batch, batchMerkleRoot):
        return self.contract.functions.verifyBatchMerkleRoot(institute, batch, batchMerkleRoot).call()

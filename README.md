
# RopstenCtf  
  
<p align="center">  
  RopstenCtf is an easy tool to interact with the ethereum ropsten network for ctf purpose and more.
  <br>
  <a href="https://twitter.com/intent/follow?screen_name=wlayzz" title="Follow"><img src="https://img.shields.io/twitter/follow/wlayzz?label=Wlayzz&style=social"></a>  
  <br>  
</p>  

**Supported features:** 
 - Ethereum wallet manager
 - Deployment and compilation of smart contract
 - Interaction with on chain smart contract
 - Inspection of transactions and block
 - Some Ethereum cryptography utils

## Prerequisites
### Solc *(for smart contract and compilation features only)*

You need the solc binary to use somes features, follow the official documentation [here](Prerequisites) for installation. 

> ⚠️ If you encounter issues installing solc check the [troubleshooting section]().

### Python dependencies
Install the python dependencies by running this commands :

    python3 -m pip install -r requirements.txt

### Infura api key
To interact with ethereum blockchain you need an api key, you can use the Infura provider to generate your key. Check the documentation [here]().

# ~~Quick~~ start
## Wallet
### Import the provider key
Now import the api key generate by infura, by running:

    ./RopstenCtf
###Setup your wallet
#### Generate a new wallet
If you want to import the generated private key in metamask follow the documentation [here](https://metamask.zendesk.com/hc/en-us/articles/360015489331-How-to-import-an-Account#h_01G01W07NV7Q94M7P1EBD5BYM4).

    ./RopstenCtf

#### Import an existing wallet
If you want to import an existing private key, run the following:

    ./RopstenCtf

### Check information about your wallet
If you want to see your balance or your public address, run :

    ./RopstenCtf

Deploying contract:  
./RopstenCtf.py contract --deploy --file FreeMoney.sol --name FreeMoney  
  
Troubleshouting :  
    "FileNotFoundError: [Errno 2] No such file or directory: 'solc'"  
You need to install solc binary :   
sudo apt update  
sudo apt install snapd  
sudo snap install core  
sudo systemctl start snapd  
sudo snap install solc

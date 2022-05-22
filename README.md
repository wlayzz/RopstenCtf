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





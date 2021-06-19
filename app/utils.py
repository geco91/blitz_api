from app.routers import bitcoin
from types import coroutine
import aiohttp
import requests
import json
from decouple import config


class BitcoinConfig:
    def __init__(self) -> None:
        self.network = config("network")

        if(self.network == "testnet"):
            self.ip = config("bitcoind_ip_testnet")
            self.rpc_port = config("bitcoind_port_testnet")
            self.zmq_port = config("bitcoind_port_zmq_testnet")
        else:
            self.ip = config("bitcoind_ip_mainnet")
            self.rpc_port = config("bitcoind_port_mainnet")
            self.zmq_port = config("bitcoind_port_zmq_mainnet")

        self.rpc_url = f"http://{self.ip}:{self.rpc_port}"
        self.zmq_url = f"tcp://{self.ip}:{self.zmq_port}"

        self.username = config("bitcoind_user")
        self.pw = config("bitcoind_pw")


bitcoin_config = BitcoinConfig()


def bitcoin_rpc(method: str, params: list = []) -> requests.Response:
    """Make an RPC request to the Bitcoin daemon 

    Connection parameters are read from the .env file.

    Parameters
    ----------
    method : str
        The method to call.
    params : list, optional
        Any parameters to include with the call
    """
    auth = (bitcoin_config.username, bitcoin_config.pw)
    headers = {"Content-type": "text/plain"}
    data = '{"jsonrpc": "2.0", "method": "' + \
        method + '", "id":"0", "params":' + json.dumps(params) + '}'
    return requests.post(bitcoin_config.rpc_url, auth=auth, headers=headers, data=data)


async def bitcoin_rpc_async(method: str, params: list = []) -> coroutine:
    auth = aiohttp.BasicAuth(bitcoin_config.username, bitcoin_config.pw)
    headers = {"Content-type": "text/plain"}
    data = '{"jsonrpc": "2.0", "method": "' + \
        method + '", "id":"0", "params":' + json.dumps(params) + '}'

    async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
        async with session.post(bitcoin_config.rpc_url, data=data) as resp:
            return await resp.json()
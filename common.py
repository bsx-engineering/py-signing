import dataclasses
import requests
from eip712_structs import make_domain, EIP712Struct


@dataclasses.dataclass
class Config:
    bsx_url: str
    domain: EIP712Struct


def get_config(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


testnet_config_data = get_config("https://api.testnet.bsx.exchange/chain/configs")
TESTNET_CONFIG = Config(
    bsx_url="https://api.testnet.bsx.exchange",
    domain=make_domain(
        name=testnet_config_data["name"],
        version=testnet_config_data["version"],
        chainId=testnet_config_data["chain_id"],
        verifyingContract=testnet_config_data["verifying_contract"],  # note the changed naming convention here
    ),
)
print("TESTNET_CONFIG", TESTNET_CONFIG)

mainnet_config_data = get_config("https://api.testnet.bsx.exchange/chain/configs")
MAINNET_CONFIG = Config(
    bsx_url="https://api.testnet.bsx.exchange",
    domain=make_domain(
        name=mainnet_config_data["name"],
        version=mainnet_config_data["version"],
        chainId=mainnet_config_data["chain_id"],
        verifyingContract=mainnet_config_data["verifying_contract"],  # note the changed naming convention here
    ),
)

print("MAINNET_CONFIG", MAINNET_CONFIG)

X18_DECIMALS = 10 ** 18


# TESTNET_URL = "http://localhost:8090"


def post_request(url, path, payload, api_keys):
    headers = {"accept": "application/json", "content-type": "application/json"}
    if api_keys:
        headers.update(
            {
                "BSX-KEY": api_keys["api_key"],
                "BSX-SECRET": api_keys["api_secret"],
            }
        )
    response = requests.post(f"{url}{path}", json=payload, headers=headers)
    print(response.text)
    response.raise_for_status()
    return response.json()

import logging
import time
from eth_account import Account
from web3 import Web3

from common import TESTNET_CONFIG, X18_DECIMALS, post_request
from structs import Order, SignKey, Register

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

config = TESTNET_CONFIG

# This is the main wallet
account = Account.from_key(
    # "0x22f2f8bd71ba7dc47e762cc70b7e5db5ecc45ea4a7babc5268782c58c79c346e"
    "0x0000000000000000000000000000000000000000000000000000000000000001"
)
print(f"account {account.address}")

signer = Account.from_key(
    # "0xdd86166bd13bbfa046967a9b8aa6e2e3c10a8b0bcef902fe63b01ba873148086"
    "0x0000000000000000000000000000000000000000000000000000000000000002"
)
print(f"signer {signer.address}")

# Sign to register a signer wallet and retrieve the API keys
signing_key_struct = SignKey(account=account.address)
signable_bytes = Web3.keccak(signing_key_struct.signable_bytes(domain=config.domain))
signer_signature = Account._sign_hash(signable_bytes, signer.key).signature.hex()

message = "hello"
nonce = round(time.time())
register_struct = Register(key=signer.address, message=message, nonce=nonce)

register_struct_bytes = Web3.keccak(
    register_struct.signable_bytes(domain=config.domain)
)
account_signature = Account._sign_hash(
    register_struct_bytes, account.key
).signature.hex()

# API payload to register a signer wallet and retrieve the API keys
payload = {
    "user_wallet": account.address,
    "signer": signer.address,
    "nonce": nonce,
    "wallet_signature": account_signature,
    "signer_signature": signer_signature,
    "message": message,
}

headers = {"accept": "application/json", "content-type": "application/json"}

api_keys = post_request(config.bsx_url, "/users/register", payload, api_keys=None)
log.info(f"API keys {api_keys}")

# This is an actual response from the API retrieved from the above code
# api_keys = {
#     "api_key": "fb116b4919fb1afaa22ce4a8b460b43f",
#     "api_secret": "fe75e00fc8a0bfcd84812e48ed8c51c8bfea535bf4a7607cae8e3d6548be63dc",
#     "expired_at": "1707833986392127547",
#     "name": "",
# }


size = 2.1  # size of the base asset (btc/eth/sol)
price = 100.3  # usdc
######### ORDER SIGNING AND SUBMISSION #############
order_struct = Order(
    sender=account.address,
    size=int(size * X18_DECIMALS),  # Size of 2.1
    price=int(price * X18_DECIMALS),  # Limit price of $2500.3
    # a random positive int64, you can use timestamp
    nonce=round(time.time()),
    productIndex=3,
    # 1 for BTC-PERP, 2 for ETH-PERP, 3 for SOL-PERP; see https://api.bsx.exchange/products; each product has a unique "index" field here
    orderSide=0,  # 0 for buy and 1 for sell
)

log.info(f"order struct {order_struct.data_dict()}")

signable_bytes = Web3.keccak(order_struct.signable_bytes(domain=config.domain))

signature = Account._sign_hash(signable_bytes, signer.key).signature.hex()
log.info(f"order signature: {signature}")

order_dict = order_struct.data_dict()

# API payload to submit an order
payload = {
    "side": "BUY",
    "product_index": order_dict["productIndex"],
    "price": str(price),
    "size": str(size),
    "time_in_force": "GTC",
    "nonce": order_dict["nonce"],
    "signature": signature,
}

# NOTE: Should call deposit test tokens only once per day - only call this for testnet
# response = post_request("/deposit-test-token", {}, api_keys)
response = post_request(config.bsx_url, "/orders", payload, api_keys)
# any error different from "failed to verify order signature" should be considered as a successful order sign and submission

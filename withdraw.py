import logging
from eth_account import Account
import requests
from web3 import Web3
from common import MAINNET_CONFIG, TESTNET_CONFIG, X18_DECIMALS, post_request
from structs import Withdraw
import random


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

config = TESTNET_CONFIG

# This is the main wallet
account = Account.from_key(
    "0x22f2f8bd71ba7dc47e762cc70b7e5db5ecc45ea4a7babc5268782c58c79c346e"
)


# random nonce up to max(int64)
# Generate a random nonce
nonce = random.randint(0, 9223372036854775807)

# Fill in the amount here
amount = 2

withdraw_struct = Withdraw(
    sender=account.address,
    token=config.usdc_address,
    amount=amount * X18_DECIMALS,
    nonce=nonce,
)

withdraw_struct_bytes = Web3.keccak(
    withdraw_struct.signable_bytes(domain=config.domain)
)
withdraw_signature = Account._sign_hash(
    withdraw_struct_bytes, account.key
).signature.hex()

# API payload to register a signer wallet and retrieve the API keys
payload = {
    "sender": account.address,
    "token": config.usdc_address,
    "amount": str(amount),
    "nonce": nonce,
    "signature": withdraw_signature,
}

headers = {"accept": "application/json", "content-type": "application/json"}

withdraw_resp = post_request(config.bsx_url, "/transfers/withdraw", payload, api_keys=None)
import ipdb; ipdb.set_trace()
log.info(withdraw_resp.json())

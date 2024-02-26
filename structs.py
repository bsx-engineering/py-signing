from eip712_structs import (Address, EIP712Struct, String, Uint)

class SignKey(EIP712Struct):
    account = Address()

class Register(EIP712Struct):
    key = Address()
    message = String()
    nonce = Uint(64)

class Withdraw(EIP712Struct):
    sender = Address()
    token = Address()
    amount = Uint(128)
    nonce = Uint(64)

"""
Order: [
    { name: "sender", type: "address" },
    { name: "size", type: "uint128" },
    { name: "price", type: "uint128" },
    { name: "nonce", type: "uint64" },
    { name: "productIndex", type: "uint8" },
    { name: "orderSide", type: "uint8" },
],
"""
class Order(EIP712Struct):
    sender = Address()
    size = Uint(128)
    price = Uint(128)
    nonce = Uint(64)
    productIndex = Uint(8)
    orderSide = Uint(8)

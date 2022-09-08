from __future__ import annotations

from pycardano import Address
from pycardano import Network
from pycardano import VerificationKeyHash


def get_address_from_cbor(cbor_string: str) -> Address:
    cbor_bytes = bytes.fromhex(cbor_string)
    addr = Address.from_primitive(cbor_bytes)
    return addr


def get_staking_address(address: Address) -> str | None:
    # Check if address has staking part
    if not isinstance(address.staking_part, VerificationKeyHash):
        return None

    stake_address = Address(
        staking_part=address.staking_part,
        network=Network.MAINNET,
    ).encode()

    return stake_address


def resolve_wallet_address(address: Address) -> str:
    stake_address = get_staking_address(address)
    if stake_address is not None:
        return stake_address
    else:
        return address.encode()

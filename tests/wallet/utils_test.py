from __future__ import annotations

from pycardano import Address

from app.wallet.utils import get_address_from_cbor


def test_get_address_from_cbor():
    cbor_string = (
        '018ec8ad437a676544100b613cb4'
        '9f0065e48f297e68769cea32c3e9e'
        'fdc6dba1363fcbf676c311bc54eea7'
        'cf9643bd6e93401096cc3330346'
    )
    address = (
        'addr1qx8v3t2r0fnk23qspdsnedylqp'
        'j7fref0e58d882xtp7nm7udkapxcluha'
        'nkcvgmc48w5l8evsaad6f5qyykesenqdrqnnznmq'
    )
    addr = get_address_from_cbor(cbor_string=cbor_string)

    assert isinstance(addr, Address)
    assert addr.encode() == address

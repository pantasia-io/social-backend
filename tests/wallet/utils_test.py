from __future__ import annotations

import pytest
from pycardano import Address
from pycardano.exception import DeserializeException

from app.wallet.utils import get_address_from_cbor
from app.wallet.utils import get_staking_address
from app.wallet.utils import resolve_wallet_address


class TestGetAddressFromCbor:
    def test_good_cbor(self):
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

    def test_invalid_hex_string(self):
        bad_cbor_string = 'notahex'

        with pytest.raises(ValueError):
            get_address_from_cbor(bad_cbor_string)

    def test_bad_cbor(self):
        cbor_string = (
            '018ec8ad437a676544100b613cb4'
            '9f0065e48f297e68769cea32c3e9e'
            'fdc6dba1363fcbf676c311bc54eea7'
            'cf9643bd6e93401096cc33303'
        )

        # TODO:
        # Unclear which error will be raised
        # ValueError will be raised if Network part incorrect (MAINNET/TESTNET)
        # Getting Assertion Error otherwise if the hex length is incorrect
        # Not sure how to trigger DeserializeException, it's the only official
        # documented exception
        with pytest.raises((ValueError, AssertionError, DeserializeException)):
            get_address_from_cbor(cbor_string)


class TestGetStakingAddress:
    def test_good_address(self):
        address = (
            'addr1qx8v3t2r0fnk23qspdsnedylqp'
            'j7fref0e58d882xtp7nm7udkapxcluha'
            'nkcvgmc48w5l8evsaad6f5qyykesenqdrqnnznmq'
        )
        stake_address = (
            'stake1u8wxmwsnv07t7emvxydu2nh20nukgw'
            '7kay6qzztvcvesx3sxt80ze'
        )
        addr_obj = Address.from_primitive(address)
        result = get_staking_address(addr_obj)
        assert result == stake_address

    def test_enterprise_address(self):
        address = (
            'addr1vx7vlgvuupzvvls99penvatpm2c4j9lj'
            'scevzsnn3awk8ys6xynxk'
        )

        addr_obj = Address.from_primitive(address)
        result = get_staking_address(addr_obj)

        assert result is None

    def test_byron_address(self):
        address = (
            'Ae2tdPwUPEZFRbyhz3cpfC2CumGzNkFBN2L42rcU'
            'c2yjQpEkxDbkPodpMAi'
        )

        with pytest.raises(TypeError, match='NoneType'):
            Address.from_primitive(address)


@pytest.mark.parametrize(
    'address, wallet_key',
    [
        (
            (
                'addr1qx8v3t2r0fnk23qspdsnedylqp'
                'j7fref0e58d882xtp7nm7udkapxcluha'
                'nkcvgmc48w5l8evsaad6f5qyykesenqdrqnnznmq'
            ),
            (
                'stake1u8wxmwsnv07t7emvxydu2nh20nukgw'
                '7kay6qzztvcvesx3sxt80ze'
            ),
        ),
        (
            (
                'addr1vx7vlgvuupzvvls99penvatpm2c4j9lj'
                'scevzsnn3awk8ys6xynxk'
            ),
            (
                'addr1vx7vlgvuupzvvls99penvatpm2c4j9lj'
                'scevzsnn3awk8ys6xynxk'
            ),
        ),
    ],
)
def test_resolve_wallet_address(address, wallet_key):
    addr_obj = Address.from_primitive(address)
    result = resolve_wallet_address(addr_obj)
    assert result == wallet_key

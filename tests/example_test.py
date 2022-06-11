# Function based Test Case
from __future__ import annotations


def test_one_plus_one():
    assert 1 + 1 == 2


# Grouping similar Test Case into a Class
class TestArithmetic:
    def test_addition(self):
        assert 1 + 1 == 2

    def test_multiplication(self):
        assert 2 * 3 == 6

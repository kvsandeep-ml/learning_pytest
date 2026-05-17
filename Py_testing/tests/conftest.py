import pytest
import sys
sys.path.append(".")
from app import BankAccount, InsufficientFundsError, transfer


@pytest.fixture
def empty_account():
    """A fresh account with zero balance."""
    return BankAccount(owner="Alice")


@pytest.fixture
def funded_account():
    """An account pre-loaded with 1000.0."""
    account = BankAccount(owner="Bob", initial_balance=1000.0)
    return account


@pytest.fixture
def two_accounts():
    """A pair of accounts for transfer tests."""
    sender = BankAccount("Charlie", initial_balance=500.0)
    receiver = BankAccount("Diana", initial_balance=100.0)
    return sender, receiver

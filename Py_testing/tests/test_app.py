import pytest
import sys
sys.path.append(".")
from app import BankAccount, InsufficientFundsError, transfer

# ─────────────────────────────────────────────
# PARAMETRIZE — run same test with many inputs
# ─────────────────────────────────────────────

@pytest.mark.parametrize("amount, expected_balance", [
    (100,    100.0),
    (0.01,     0.01),
    (9999,  9999.0),
    (250.5,  250.5),
])
def test_deposit_valid_amounts(empty_account, amount, expected_balance):
    """Depositing various valid amounts should update balance correctly."""
    empty_account.deposit(amount)
    assert empty_account.balance == pytest.approx(expected_balance)

@pytest.mark.parametrize("withdraw_amount, expected_balance", [
    (100,   900.0),
    (1000, 0.0),
    (0.5,   999.5),
])
def test_withdraw_valid_amounts(funded_account, withdraw_amount, expected_balance):
    """Withdrawing valid amounts should reduce balance correctly."""
    funded_account.withdraw(withdraw_amount)
    assert funded_account.balance == pytest.approx(expected_balance)


@pytest.mark.parametrize("bad_amount", [0, -50])
def test_withdraw_invalid_amounts(funded_account, bad_amount):
    """Zero or negative withdrawals should raise ValueError."""
    with pytest.raises(ValueError):
        funded_account.withdraw(bad_amount)


# ─────────────────────────────────────────────
# REGULAR TESTS using fixtures
# ─────────────────────────────────────────────

def test_initial_balance_default(empty_account):
    assert empty_account.balance == 0.0


def test_initial_balance_custom():
    account = BankAccount("Eve", initial_balance=500)
    assert account.balance == 500


def test_negative_initial_balance_raises():
    with pytest.raises(ValueError, match="cannot be negative"):
        BankAccount("Frank", initial_balance=-100)


def test_withdraw_insufficient_funds(empty_account):
    with pytest.raises(InsufficientFundsError):
        empty_account.withdraw(1)


def test_transaction_count_after_operations(funded_account):
    funded_account.deposit(200)
    funded_account.withdraw(50)
    assert funded_account.get_transaction_count() == 2


def test_statement_no_transactions(empty_account):
    statement = empty_account.get_statement()
    assert "No transactions" in statement


def test_statement_with_transactions(funded_account):
    funded_account.deposit(200)
    funded_account.withdraw(100)
    statement = funded_account.get_statement()
    assert "+200.00" in statement
    assert "-100.00" in statement
    assert "Balance:" in statement


def test_transfer_updates_both_accounts(two_accounts):
    sender, receiver = two_accounts
    transfer(sender, receiver, 200)
    assert sender.balance == 300.0
    assert receiver.balance == 300.0


def test_transfer_insufficient_funds_leaves_accounts_unchanged(two_accounts):
    sender, receiver = two_accounts
    with pytest.raises(InsufficientFundsError):
        transfer(sender, receiver, 9999)
    # sender balance should be untouched since withdraw failed
    assert sender.balance == 500.0
    assert receiver.balance == 100.0
class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self.balance = initial_balance
        self.transactions: list[dict] = []

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount}. Available balance: {self.balance}"
            )
        self.balance -= amount
        self.transactions.append({"type": "withdrawal", "amount": amount})
        return self.balance

    def get_transaction_count(self) -> int:
        return len(self.transactions)

    def get_statement(self) -> str:
        if not self.transactions:
            return f"{self.owner}'s account: No transactions yet."
        lines = [f"{self.owner}'s statement:"]
        for t in self.transactions:
            sign = "+" if t["type"] == "deposit" else "-"
            lines.append(f"  {sign}{t['amount']:.2f}")
        lines.append(f"  Balance: {self.balance:.2f}")
        return "\n".join(lines)


def transfer(source: BankAccount, target: BankAccount, amount: float) -> None:
    """Transfer amount from source account to target account."""
    source.withdraw(amount)
    target.deposit(amount)
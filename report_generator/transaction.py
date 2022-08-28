from dataclasses import dataclass


@dataclass
class Transaction:
    """A debit or credit economic transaction.

    Attributes:
        id (int): The transaction id.
        month (str): The month of occurrence of this transaction.
        day (str): The day of month of this transaction.
        type (str): A categorical variable ("credit", "debit") signaling the transaction type.
        value (float): The economic value of the transaction.
    """
    id: int
    month: str
    day: str
    type: str
    value: float

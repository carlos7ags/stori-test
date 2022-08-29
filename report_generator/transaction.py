from dataclasses import dataclass
import datetime

@dataclass
class Transaction:
    """A debit or credit economic transaction.

    Attributes:
        id (int): The transaction id.
        date (datetime): The date of occurrence of this transaction.
        type (str): A categorical variable ("credit", "debit") signaling the transaction type.
        value (float): The economic value of the transaction.
    """
    id: int
    date: datetime
    type: str
    value: float

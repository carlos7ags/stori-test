from app.ReportGenerator.transaction import Transaction


def transaction_parser(transaction: str):
    txn = transaction.split(",")
    return Transaction(
        id=int(txn[0]),
        month=txn[1].split("/")[0],
        day=txn[1].split("/")[1],
        type="credit" if txn[2][0] == "+" else "debit",
        value=float(txn[2][1:]),
    )

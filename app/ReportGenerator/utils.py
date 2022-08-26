from typing import List, Dict
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


def get_average_value(transactions: List[Transaction]) -> float:
    return sum([txn.value for txn in transactions]) / len(transactions)


def get_total_balance(transactions: List[Transaction]) -> float:
    return sum([txn.value if "credit" else -txn.value for txn in transactions])


def get_transactions_summary(transactions: List[Transaction]) -> Dict:
    summary = dict()
    summary["balance"] = get_total_balance(transactions)
    periods = set([txn.month for txn in transactions])
    for period in periods:
        period_transactions = list(filter(lambda x: x.month == period, transactions))

        summary[period]["transactions_count"] = len(period_transactions)

        credit_transactions = list(filter(lambda x: x.type == "credit", period_transactions))
        summary[period]["credit_average"] = get_average_value(credit_transactions)

        debits_transactions = list(filter(lambda x: x.type == "debit", period_transactions))
        summary[period]["debit_average"] = get_average_value(debits_transactions)

    return summary


def transform_csv_object_to_transactions(csv_object: Any) -> List[Transaction]:
    data = csv_object['Body'].read().decode("utf-8").splitlines()
    records = csv.reader(data)
    next(records)
    return list(map(transaction_parser, records))

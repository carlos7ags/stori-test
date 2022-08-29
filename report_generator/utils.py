import csv
import os
from typing import List, Dict, Any
from datetime import datetime

from .transaction import Transaction


def transaction_parser(transaction: str):

    return Transaction(
        id=int(transaction[0]),
        date=datetime.strptime(transaction[1], "%m/%d"),
        type="credit" if transaction[2][0] == "+" else "debit",
        value=float(transaction[2][1:]),
    )


def get_average_value(transactions: List[Transaction]) -> float:
    return sum([txn.value for txn in transactions]) / len(transactions)


def get_total_balance(transactions: List[Transaction]) -> float:
    return sum([txn.value if txn.type == "credit" else -1 * txn.value for txn in transactions])


def get_transactions_summary(transactions: List[Transaction]) -> Dict:
    summary = dict()
    summary["balance"] = "${:0,.2f}".format(get_total_balance(transactions))
    summary["monthly_summary"] = []
    periods = sorted(list(set([txn.date.strftime("%B") for txn in transactions])), reverse=True)
    for period in periods:
        period_transactions = list(filter(lambda x: x.date.strftime("%B") == period, transactions))

        tmp_monthly_summary = dict()
        tmp_monthly_summary["period"] = period

        tmp_monthly_summary["transactions_count"] = len(period_transactions)

        credit_transactions = list(filter(lambda x: x.type == "credit", period_transactions))
        tmp_monthly_summary["credit_average"] = "${:0,.2f}".format(get_average_value(credit_transactions))

        debits_transactions = list(filter(lambda x: x.type == "debit", period_transactions))
        tmp_monthly_summary["debit_average"] = "${:0,.2f}".format(get_average_value(debits_transactions))

        summary["monthly_summary"].append(tmp_monthly_summary)

    return summary


def transform_csv_object_to_transactions(csv_object: Any) -> List[Transaction]:
    data = csv_object['Body'].read().decode("utf-8").splitlines()
    records = csv.reader(data)
    next(records)
    return list(map(transaction_parser, records))


def replace_template_literals(context: Dict, template_path: str) -> str:
    cwd = os.getcwd()

    with open(os.path.join(cwd, template_path), "r") as file:
        html_email_report = file.read()

    for tag, value in context.items():
        html_email_report = html_email_report.replace("{{ %s }}" % tag, str(value))

    return html_email_report


def get_transactions_html_report(context: Dict) -> str:
    body = ""
    for monthly_summary in context["monthly_summary"]:
        body += replace_template_literals(monthly_summary, "report_generator/templates/transactions_monthly_summary.html")

    return replace_template_literals({"balance": context["balance"], "monthly_summary": body},
                                     "report_generator/templates/transactions_summary_report.html")

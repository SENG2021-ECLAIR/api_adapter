"""
Calculate and create the stats of the users.
"""

from api_adapter.database import get_invoices
import datetime, xmltodict

def curr_month_stats(token):
    """
    Earnings for the month is returned.
    """

    invoices, msg = get_invoices(token)

    created_invoices = invoices["created"]

    month_earns = 0

    # find today's date
    today_date = datetime.datetime.now()

    for invoice in created_invoices:
        time_of_invoice = invoice["timestamp"]

        # parse datetime
        invoice_datetime = datetime.datetime.strptime(
            time_of_invoice, "%d/%m/%Y, %H:%M:%S"
        )
        if (invoice_datetime.month == today_date.month
            and invoice_datetime.year == today_date.year):
            # inv_dict = xmltodict.parse(invoice["invoices"]["content"])
            # monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
            # month_earns += float(monetary["cbc:PayableAmount"]["#text"])
            month_earns += 1
    
    for invoice in invoices["received"]:
        time_of_invoice = invoice["timestamp"]

        # parse datetime
        invoice_datetime = datetime.datetime.strptime(
            time_of_invoice, "%d/%m/%Y, %H:%M:%S"
        )
        if (invoice_datetime.month == today_date.month
            and invoice_datetime.year == today_date.year):
            # inv_dict = xmltodict.parse(invoice["invoices"]["content"])
            # monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
            # month_earns += float(monetary["cbc:PayableAmount"]["#text"])
            month_earns += 1

    list_prev_months = []

    for _ in range(0,5):
        list_prev_months.append(0)

    # find the date 5 months ago
    start_date = today_date - datetime.timedelta(5*30)

    curr_date = today_date

    i = 0


    while (curr_date != start_date):

        for invoice in invoices["created"]:
            time_of_invoice = invoice["timestamp"]

            # parse datetime
            invoice_datetime = datetime.datetime.strptime(
                time_of_invoice, "%d/%m/%Y, %H:%M:%S"
            )

            if (invoice_datetime.month == curr_date.month
                and invoice_datetime.year == curr_date.year):
                # inv_dict = xmltodict.parse(invoice["invoices"]["content"])
                # monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
                # list_stats[i] += float(monetary["cbc:PayableAmount"]["#text"])
                list_prev_months[i] += 1

        for invoice in invoices["received"]:
            time_of_invoice = invoice["timestamp"]

            # parse datetime
            invoice_datetime = datetime.datetime.strptime(
                time_of_invoice, "%d/%m/%Y, %H:%M:%S"
            )

            if (invoice_datetime.month == curr_date.month
                and invoice_datetime.year == curr_date.year):
                # inv_dict = xmltodict.parse(invoice["invoices"]["content"])
                # monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
                # list_stats[i] += float(monetary["cbc:PayableAmount"]["#text"])
                list_prev_months[i] += 1

        # loop back each date
        curr_date -= datetime.timedelta(30)
        i += 1

    return {
        "msg": msg,
        "month_earns": month_earns,
        "last_five_months": list_prev_months
    }

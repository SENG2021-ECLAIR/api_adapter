"""
Calculate and create the stats of the users.
"""

from api_adapter.database import get_invoices
import datetime, xmltodict

def last_thirty_days_stats(token):
    """
    Earnings for the last thirty days is returned.
    """

    invoices, msg = get_invoices(token)

    created_invoices = invoices["created"]

    list_stats = []

    for _ in range(0,30):
        list_stats.append(0)

    # find today's date
    today_date = datetime.datetime.now()

    # find the date 30 days ago
    start_date = today_date - datetime.timedelta(31)

    curr_date = today_date

    i = 0

    while curr_date != start_date:
        for invoice in created_invoices:
            time_of_invoice = invoice["invoices"]["timestamp"]

            # parse datetime
            invoice_datetime = datetime.datetime.strptime(
                time_of_invoice, "%d/%m/%Y, %H:%M:%S"
            )
            if invoice_datetime == curr_date:
                inv_dict = xmltodict.parse(invoice["invoices"]["content"])
                monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
                list_stats[i] += float(monetary["cbc:PayableAmount"]["#text"])

        # loop back each date
        curr_date -= datetime.timedelta(1)
        i += 1

    return {
        "msg": msg,
        "last_thirty_days": list_stats
    }

"""
Calculate and create the stats of the users.
"""

from api_adapter.database import get_invoices
import datetime, xmltodict

def curr_year_stats(token):
    """
    Earnings for the year is returned.
    """

    invoices, msg = get_invoices(token)

    created_invoices = invoices["created"]

    year_earns = 0

    # find today's date
    today_date = datetime.datetime.now()

    for invoice in created_invoices:
        time_of_invoice = invoice["invoices"]["timestamp"]

        # parse datetime
        invoice_datetime = datetime.datetime.strptime(
            time_of_invoice, "%d/%m/%Y, %H:%M:%S"
        )
        if invoice_datetime.year == today_date.year:
            inv_dict = xmltodict.parse(invoice["invoices"]["content"])
            monetary = inv_dict["Invoice"]["cac:LegalMonetaryTotal"]
            year_earns += float(monetary["cbc:PayableAmount"]["#text"])

    return {
        "msg": msg,
        "year_earns": year_earns
    }

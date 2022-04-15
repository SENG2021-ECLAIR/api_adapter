"""
Calculate and create the stats of the users.
"""

from api_adapter.database import get_invoices
import datetime, xmltodict

def num_created_stats(token):
    """
    How many invoices received is returned.
    """

    invoices, msg = get_invoices(token)

    received_invoices = invoices["received"]

    return {
        "msg": msg,
        "num_created_inv": len(received_invoices)
    }

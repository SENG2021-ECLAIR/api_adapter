"""
Calculate and create the stats of the users.
"""

from api_adapter.database import get_invoices
import datetime, xmltodict

def num_created_stats(token):
    """
    How many invoices created is returned.
    """

    invoices, msg = get_invoices(token)

    created_invoices = invoices["created"]

    return {
        "msg": msg,
        "num_created_inv": len(created_invoices)
    }

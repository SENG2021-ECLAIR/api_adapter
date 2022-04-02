"""
Functionality that is behind the "listing" endpoint. This:
    - gets all the invoices that the user has uploaded
"""

from api_adapter.database import get_invoices


def list_invoices(token: str) -> dict:
    """
    Gets a list of all invoices the user has uploaded
    """
    invoices, msg = get_invoices(token)
    return {"msg": msg, "invoices": invoices}

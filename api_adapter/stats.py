"""
Calculate and create the stats of the users.
"""

def last_thirty_days_stats(token):
    """
    Earnings for the last thirty days is returned.
    """

    invoices, msg = get_invoices(token)

    
"""
Functionality that is behind the "create" endpoint. This:
    - creates and validates the invoice via an API
    - stores the invoice via an API
"""

import requests

def create_invoice(invoice_details):
    return_val = requests.post(
        "seng-donut-frontend.azurewebsites.net/json/convert",
        json={
            "body"=invoice_details
        }
    )
    return {
        "status_code": return_val.status_code,
        "invoice": return_val.json()["invoice"]
    }

'''
Functionality for the send endpoint
- Takes a UBL file and sends it toanother user
- Generates a status report
'''

import requests

def send_invoice(input):
    post_val = requests.post("https://virtserver.swaggerhub.com/SE2Y22G24/e-invoice-sending/1.0.0/invoice/send/email",
        json = input)
    return {
        "status_code": post_val.status_code,
        "report_id": post_val.json()["report_id"]
    }
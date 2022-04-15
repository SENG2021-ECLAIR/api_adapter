"""
Functionality for the send endpoint
- Takes a UBL file and sends it toanother user
- Generates a status report
"""

import requests


def send_invoice(input):
    data1 = {
        "token": input["token"],
        "invoiceTitle": input["invoiceTitle"],
        "mailContent": input["mailContent"],
        "recipientEmail": input["recipientEmail"],
    }
    data2 = {"file": input["file"]}
    url = "https://honeycomb-prod.herokuapp.com/send"
    post_val = requests.post(url, data=data1, files=data2)
    return post_val

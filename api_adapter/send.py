'''
Functionality for the send endpoint
- Takes a UBL file and sends it toanother user
- Generates a status report
'''

import requests

    

def send_invoice():
    data1 = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL!!!",
        "mailContent": "Here is your UBL",
        "recipientEmail": "z5367576@ad.unsw.edu.au"
    }
    data2 = {
        "file": open("tests/test_data/test_valid_response.xml")
    }
    url = "https://honeycomb-prod.herokuapp.com/send"
    post_val = requests.post(url, data=data1, files=data2)
    return post_val

# def send_invoice_sms(input):
#     post_val = requests.post("https://virtserver.swaggerhub.com/SE2Y22G24/e-invoice-sending/1.0.0/invoice/send/email",
#         json = input)
#     return {
#         "status_code": post_val.status_code,
#         "report_id": post_val.json()["report_id"]
#     }
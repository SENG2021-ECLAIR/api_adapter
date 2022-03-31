'''
Functionality for the send endpoint
- Takes a UBL file and sends it toanother user
- Generates a status report
'''

import requests

def send_invoice(xml_data, email, subject, message, token):
    post_val = requests.post("https://virtserver.swaggerhub.com/SE2Y22G24/e-invoice-sending/1.0.0/invoice/send/email",
    json = {
        "xml_data": xml_data,
        "email": email,
        "subject": subject,
        "message": message,
        "token": token
    })
    return {
        "status_code": post_val.status_code,
        "report_id": post_val.json()["report_id"]
    }
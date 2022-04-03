import json
import xml.etree.ElementTree as ET

import pytest

from api_adapter.send import send_invoice

VALID = 200
INVALID_INPUT = 405

def test_successful_ubl():
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL!!!",
        "mailContent": "Here is your UBL",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": open("tests/test_data/test_valid_response.xml")
    }
    result = send_invoice(input)
    assert result.status_code == VALID

import json
import xml.etree.ElementTree as ET

import pytest

from api_adapter.send import send_invoice

VALID = 200
INVALID_INPUT = 405

# @pytest.fixture
# def valid_invoice():
#     with open("tests/test_data/test_valid_response.xml") as sample_invoice_file:
#         return sample_invoice_file


def test_successful_ubl(valid_invoice):



    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDdkNWYxN2I0NDViNDlkOGI2MTZjMCIsImVtYWlsIjoiZXRoYW5oYWZmZW5kZW5AZ21haWwuY29tIiwiaWF0IjoxNjQ4ODc1MTc1fQ.LYXRVSvge2TUU6rv_4y2RWLgiaHDIhW1Ttd-ZRSHlm4",
        "invoiceTitle": "UBL!!!",
        "mailContent": "Here is your UBL",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": open("tests/test_data/test_valid_response.xml")
    }

    result = send_invoice(input)
    assert result.status_code == VALID
from inspect import _void
import json
import xml.etree.ElementTree as ET

import pytest

from api_adapter.send import send_invoice

VALID = 200
ACCESS_ERROR = 403
INVALID_INPUT = 405

def test_successful_ubl():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == VALID

def test_access_error():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "this token isn't valid",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == ACCESS_ERROR

def test_missing_token():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == INVALID_INPUT

def test_missing_title():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == INVALID_INPUT

def test_missing_content():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == INVALID_INPUT

def test_missing_email():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == INVALID_INPUT

def test_missing_file():
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au"
    }
    result = send_invoice(input)
    assert result.status_code == INVALID_INPUT

def test_empty_token():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == ACCESS_ERROR

def test_empty_title():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == VALID

def test_empty_content():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == VALID

def test_empty_email():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "",
        "file": input_file
    }
    result = send_invoice(input)
    input_file.close()
    assert result.status_code == INVALID_INPUT

def test_empty_file():
    input = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNDkxMzgyMzYxM2UzYTBjNjU2ZmQ4NiIsImVtYWlsIjoic2VuZzIwMjFlY2xhaXJAZ21haWwuY29tIiwiaWF0IjoxNjQ4OTU2NTQxfQ.MMog2AH6wNo7RRW5M3oy_0WGA4Kl5oj7rv0p6CrpXVw",
        "invoiceTitle": "UBL Invoice",
        "mailContent": "Attached below is your UBL Invoice",
        "recipientEmail": "z5367576@ad.unsw.edu.au",
        "file": ""
    }
    result = send_invoice(input)
    assert result.status_code == INVALID_INPUT
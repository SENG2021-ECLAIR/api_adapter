import json
import xml.etree.ElementTree as ET

import pytest

from api_adapter.send import send_invoice

VALID = 200
INVALID_INPUT = 405

@pytest.fixture
def sample_invoice():
    with open("tests/test_data/test_invoice_input.json") as sample_invoice_file:
        return json.load(sample_invoice_file)


@pytest.fixture
def invalid_invoice():
    with open("tests/test_data/test_invalid_invoice_input.json") as sample_invoice_file:
        return json.load(sample_invoice_file)
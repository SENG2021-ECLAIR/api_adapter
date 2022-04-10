from inspect import _void
import json
import xml.etree.ElementTree as ET

import pytest

from api_adapter.render import get_render

VALID = 200
ACCESS_ERROR = 403
INVALID_INPUT = 405
UNAVALIABLE = 503

def test_successful_ubl():
    input_file = open("tests/test_data/test_valid_response.xml")
    input = {
        "file": input_file
    }
    result = get_render(input)
    input_file.close()
    assert result.status_code == VALID
import xmltodict

from api_adapter.render_json import conv_xml_format


def test_one():
    resp = conv_xml_format("tests/test_data/sample_response.xml")
    print(resp)
    resp = xmltodict.parse(resp)

    print("")
    print("")
    print("")
    # print(resp)
    # print(resp)
    xml_string = open("tests/test_data/sample_response.xml").read()
    print(xml_string)
    input_xml = xmltodict.parse(xml_string)

    assert resp["Invoice"]["cbc:ID"] == input_xml["Invoice"]["cbc:ID"]
    assert (
        resp["Invoice"]["cac:InvoiceLine"]["cac:Item"]["cac:ClassifiedTaxCategory"][
            "cac:TaxScheme"
        ]["cbc:ID"]["#text"]
        == input_xml["Invoice"]["cac:InvoiceLine"]["cac:Item"][
            "cac:ClassifiedTaxCategory"
        ]["cac:TaxScheme"]["cbc:ID"]
    )
    assert resp["Invoice"]["cbc:ID"] == "EBWASP1234"

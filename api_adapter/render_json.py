import re
import xmltodict
import json
from datetime import datetime

MISSING = "ERROR DATA MISSING"
INVALID = "ERROR INVALID DATA TYPE. EXPECTED: "

def conv_xml_to_dict(ubl_file_name):
    try:
        xml_string = open(ubl_file_name).read()
        return xmltodict.parse(xml_string)
    except FileNotFoundError:
        raise Exception('UBL cannot be found')

# Confirms data for a string is relevant and accurate
def try_string(input_string):
    try:
        if not input_string:
            raise TypeError
        elif type(input_string) != str:
            raise ValueError
        else:
            return input_string
    except TypeError:
        return MISSING
    except ValueError:
        return INVALID + "STRING"

def try_int(input_int):
    try:
        return int(input_int)
    except TypeError:
        return MISSING
    except ValueError:
        return INVALID + "INT"

# Confirms data for a float is relevant and accurate
def try_float(input_float):
    try:
        return float(input_float)
    except TypeError:
        return MISSING
    except ValueError:
        return INVALID + "FLOAT"

def try_currency(input_currency):
    try:
        return "{:.2f}".format(float(input_currency))
    except TypeError:
        return MISSING
    except ValueError:
        return INVALID + "FLOAT"

def try_date(input_date):
    try:
        if not input_date:
            raise TypeError
        return datetime.strptime(input_date, '%Y-%M-%d').date()
    except TypeError:
        return MISSING
    except SyntaxError:
        return INVALID + "DATE FORMATTED YYYY-MM-DD"

def build_address(street_name, city_name, postal_zone, country):
    return try_string(street_name) + ", " + try_string(city_name) + ", " + try_string(postal_zone) + ", " + try_string(country)

def return_currency_dict(address): 
    curr_dict = {
        'Value': try_currency(address['#text']),
        'Currency': try_string(address['@currencyID'])
    }
    return curr_dict

def return_code_dict(address):
    code_dict = {
        'Value': try_string(address['#text']),
        'listAgencyID': try_int(address['@listAgencyID']),
        'listID': try_string(address['@listID'])
    }
    return code_dict

def return_ID_dict(address):
    id_dict = {
        'Value': try_string(address['#text']),
        'schemeAgencyID': try_string(address['@schemeAgencyID']),
        'schemeID': try_string(address['@schemeID'])
    }
    return id_dict

def return_quantity(address):
    quan_dict = {
        'Value': try_float(address['#text']),
        'Unit Code': try_string(address['@unitCode']),
        'Unit Code List ID': try_string(address['@unitCode'])
    }
    return quan_dict

# Gets a float of UBLVersionID
def get_UBLVersionID(ubl_dict):
    return try_float(ubl_dict['Invoice']['cbc:UBLVersionID'])

# Gets a string of CustomizationID
def get_CustomizationID(ubl_dict):
    return try_string(ubl_dict['Invoice']['cbc:CustomizationID'])

# Gets a string of ProfileID
def get_ProfileID(ubl_dict):
    return try_string(ubl_dict['Invoice']['cbc:ProfileID'])

# Gets a string of ID
def get_ID(ubl_dict):
    return try_string(ubl_dict['Invoice']['cbc:ID'])

# Gets a date of IssueDate
def get_IssueDate(ubl_dict):
    return try_date(ubl_dict['Invoice']['cbc:IssueDate'])

# Gets a code dict of InvoiceTypeCode
def get_InvoiceTypeCode(ubl_dict):
    return return_code_dict(ubl_dict['Invoice']['cbc:InvoiceTypeCode'])

# Gets a code dict of DocumentCurrencyCode
def get_DocumentCurrencyCode(ubl_dict):
    return return_code_dict(ubl_dict['Invoice']['cbc:DocumentCurrencyCode'])

# Gets a string to BuyerReference
def get_BuyersReference(ubl_dict):
    return try_string(ubl_dict['Invoice']['cbc:BuyerReference'])

# Gets a string to ID within AdditionalDocumentReference
def get_AdditionalDocumentReferenceID(ubl_dict):
    return try_string(ubl_dict['Invoice']['cac:AdditionalDocumentReference']['cbc:ID'])

def get_SupplierRegistration(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']

def get_SupplierStreet(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']['cac:PostalAddress']['cbc:StreetName']

def get_SupplierCity(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']['cac:PostalAddress']['cbc:CityName']

def get_SupplierPost(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']['cac:PostalAddress']['cbc:PostalZone']

def get_SupplierCountry(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']['cac:PostalAddress']['cac:Country']['cbc:IdentificationCode']['#text']

def get_AccountingSupplierParty(ubl_dict):
    # Address shortcuts for the code
    party_sec = ubl_dict['Invoice']['cac:AccountingSupplierParty']['cac:Party']
    postaladress_sec = party_sec['cac:PostalAddress']
    partylegalentity_sec = party_sec['cac:PartyLegalEntity']

    accounting_supplier_party = {
        'Party ID': return_ID_dict(party_sec['cac:PartyIdentification']['cbc:ID']),
        'Party Name': try_string(party_sec['cac:PartyName']['cbc:Name']),
        'Postal Address': build_address(
            postaladress_sec['cbc:StreetName'],
            postaladress_sec['cbc:CityName'],
            postaladress_sec['cbc:PostalZone'],
            postaladress_sec['cac:Country']['cbc:IdentificationCode']['#text']
        ),
        'Country': return_code_dict(postaladress_sec['cac:Country']['cbc:IdentificationCode']),
        'PartyLegalEntity': {
            'Registration Name': try_string(partylegalentity_sec['cbc:RegistrationName']),
            'Company ID': return_ID_dict(partylegalentity_sec['cbc:CompanyID'])
        }
    }
    return accounting_supplier_party

def get_CustomerRegistration(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PartyLegalEntity']['cbc:RegistrationName']

def get_CustomerStreet(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PostalAddress']['cbc:StreetName']

def get_CustomerCity(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PostalAddress']['cbc:CityName']

def get_CustomerPost(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PostalAddress']['cbc:PostalZone']

def get_CustomerCountry(ubl_dict):
    return ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']['cac:PostalAddress']['cac:Country']['cbc:IdentificationCode']['#text']

def get_AccountingCustomerParty(ubl_dict):
    party_sec = ubl_dict['Invoice']['cac:AccountingCustomerParty']['cac:Party']
    postaladress_sec = party_sec['cac:PostalAddress']

    accounting_customer_party = {
        'Party Name': try_string(party_sec['cac:PartyName']['cbc:Name']),
        'Postal Address': build_address(
            postaladress_sec['cbc:StreetName'],
            postaladress_sec['cbc:CityName'],
            postaladress_sec['cbc:PostalZone'],
            postaladress_sec['cac:Country']['cbc:IdentificationCode']['#text']
        ),
        'Country': return_code_dict(postaladress_sec['cac:Country']['cbc:IdentificationCode']),
        'Party Legal Entity': {
            'Registration Name': try_string(party_sec['cac:PartyLegalEntity']['cbc:RegistrationName'])
        }
            
    }
    return accounting_customer_party

def get_PaymentMeans(ubl_dict):
    payment_means = {
        'Payment Means Code': return_code_dict(ubl_dict['Invoice']['cac:PaymentMeans']['cbc:PaymentMeansCode']),
        'Payment ID': ubl_dict['Invoice']['cac:PaymentMeans']['cbc:PaymentID']
    }
    return payment_means

# Returns a string to payment terms
def get_PaymentTerms(ubl_dict):
    return ubl_dict['Invoice']['cac:PaymentTerms']['cbc:Note']

def get_TaxSchemeID(ubl_dict):
    id_value = ubl_dict['Invoice']['cac:TaxTotal']['cac:TaxSubtotal']['cac:TaxCategory']['cac:TaxScheme']['cbc:ID']
    return return_ID_dict(id_value)['schemeID']

def get_TaxAmount(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:TaxTotal']['cbc:TaxAmount'])['Value']

def get_TaxableAmount(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:TaxTotal']['cac:TaxSubtotal']['cbc:TaxableAmount'])['Value']

def get_TaxTotal(ubl_dict):
    taxtotal_sec = ubl_dict['Invoice']['cac:TaxTotal']
    taxsubtotal_sec = taxtotal_sec['cac:TaxSubtotal']
    tax_total = {
        'Tax Amount': return_currency_dict(taxtotal_sec['cbc:TaxAmount']),

        'Tax Subtotal': {
            'Taxable Amount': return_currency_dict(taxsubtotal_sec['cbc:TaxableAmount']),
            'Tax Amount': return_currency_dict(taxsubtotal_sec['cbc:TaxAmount']),
            'Tax Category': {
                'Tax ID': return_ID_dict(taxsubtotal_sec['cac:TaxCategory']['cbc:ID']),
                'Tax Percentage': try_float(taxsubtotal_sec['cac:TaxCategory']['cbc:Percent']),
                'Tax Scheme': return_ID_dict(taxsubtotal_sec['cac:TaxCategory']['cac:TaxScheme']['cbc:ID'])
            }
        }
    }
    return tax_total

def get_PayableAmount(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:LegalMonetaryTotal']['cbc:PayableAmount'])['Value']
    

def get_TaxExclusiveAmount(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:LegalMonetaryTotal']['cbc:TaxExclusiveAmount'])['Value']

def get_TaxInclusiveAmount(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:LegalMonetaryTotal']['cbc:TaxInclusiveAmount'])['Value']

# Returns a dictionary containing
    # 'Line Extension Amount'   == currency
    # 'Tax Exclusive Amount'    == currency
    # 'Tax Inclusive Amount'    == currency
    # 'Payable Rounding Amount' == currency
    # 'Payable Amount'          == currency
def get_LegalMonetaryTotal(ubl_dict):
    legalmonetarytotal_sec = ubl_dict['Invoice']['cac:LegalMonetaryTotal']
    legal_monetary_total = {
        'Line Extension Amount': return_currency_dict(legalmonetarytotal_sec['cbc:LineExtensionAmount']),
        'Tax Exclusive Amount': return_currency_dict(legalmonetarytotal_sec['cbc:TaxExclusiveAmount']),
        'Tax Inclusive Amount': return_currency_dict(legalmonetarytotal_sec['cbc:TaxInclusiveAmount']),
        'Payable Rounding Amount': return_currency_dict(legalmonetarytotal_sec['cbc:PayableRoundingAmount']),
        'Payable Amount': return_currency_dict(legalmonetarytotal_sec['cbc:PayableAmount'])
    }
    return legal_monetary_total

def get_InvoiceName(ubl_dict):
    return ubl_dict['Invoice']['cac:InvoiceLine']['cac:Item']['cbc:Name']

def get_InvoiceQuantity(ubl_dict):
    return return_quantity(ubl_dict['Invoice']['cac:InvoiceLine']['cbc:InvoicedQuantity'])['Value']

def get_Currency(ubl_dict):
    return return_currency_dict(ubl_dict['Invoice']['cac:InvoiceLine']['cbc:LineExtensionAmount'])['Currency']

def get_InvoiceTaxSchemeID(ubl_dict):
    return return_ID_dict(ubl_dict['Invoice']['cac:InvoiceLine']['cac:Item']['cac:ClassifiedTaxCategory']['cac:TaxScheme']['cbc:ID'])['schemeID']

def get_InvoiceLine(ubl_dict):
    invoiceline_sec = ubl_dict['Invoice']['cac:InvoiceLine']
    classifiedtaxcategory_sec = invoiceline_sec['cac:Item']['cac:ClassifiedTaxCategory']
    price_sec = invoiceline_sec['cac:Price']

    invoice_line = {
        'ID': invoiceline_sec['cbc:ID'],
        'Invoiced Quality': return_quantity(invoiceline_sec['cbc:InvoicedQuantity']),
        'Line Extension Amount': return_currency_dict(invoiceline_sec['cbc:LineExtensionAmount']),
        'Item': {
            'Name': invoiceline_sec['cac:Item']['cbc:Name'],
            'Classified Tax Category': {
                'ID': return_ID_dict(classifiedtaxcategory_sec['cbc:ID']),
                'Percent': classifiedtaxcategory_sec['cbc:Percent'],
                'Tax Scheme': return_ID_dict(classifiedtaxcategory_sec['cac:TaxScheme']['cbc:ID'])
            }
        },
        'Price': {
            'Price Amount': return_currency_dict(price_sec['cbc:PriceAmount']),
            'Base Quantity': return_quantity(price_sec['cbc:BaseQuantity'])
        }
    }
    return invoice_line

def form_json(filename: str) -> json:
    ubl_dict = conv_xml_to_dict(filename)
    output = {
        'InvoiceID': get_ID(ubl_dict),
        'InvoiceTaxSchemeID': get_InvoiceTaxSchemeID(ubl_dict),
        'InvoiceName': get_InvoiceName(ubl_dict),
        'IssueDate': get_IssueDate(ubl_dict),
        'PayableAmount': get_PayableAmount(ubl_dict),
        'InvoiceQuantity': get_InvoiceQuantity(ubl_dict),
        'Currency': get_Currency(ubl_dict) ,
        'PaymentTerms': get_PaymentTerms(ubl_dict),
        'TaxAmount': get_TaxAmount(ubl_dict),
        'TaxableAmount': get_TaxableAmount(ubl_dict),
        'TaxExclusiveAmount': get_TaxExclusiveAmount(ubl_dict),
        'TaxInclusiveAmount': get_TaxInclusiveAmount(ubl_dict),
        'TaxSchemeID': get_TaxSchemeID(ubl_dict),
        'SupplierRegistration': get_SupplierRegistration(ubl_dict),
        'SupplierStreet': get_SupplierStreet(ubl_dict),
        'SupplierCity': get_SupplierCity(ubl_dict),
        'SupplierPost': get_SupplierPost(ubl_dict),
        'SupplierCountry': get_SupplierCountry(ubl_dict),
        'CustomerRegistration': get_CustomerRegistration(ubl_dict),
        'CustomerStreet': get_CustomerStreet(ubl_dict),
        'CustomerCity': get_CustomerCity(ubl_dict),
        'CustomerPost': get_CustomerPost(ubl_dict),
        'CustomerCountry': get_CustomerCountry(ubl_dict)
    }
    return json.dumps(output)


if __name__ == "__main__":
    ubl_dict = conv_xml_to_dict("ubl_example.xml")
    print(get_InvoiceTypeCode(ubl_dict))
    print(" ")
    print(get_AccountingCustomerParty(ubl_dict))
    print(" ")
    print(get_TaxTotal(ubl_dict))
    print (get_InvoiceLine(ubl_dict))

    print(" ")
    print(" ")
    print(form_json("ubl_example.xml"))

    # print("UBL Version ID: " + str(get_UBLVersionID(ubl_dict)))
    # print("Customization ID: " + get_CustomizationID(ubl_dict))
    # print("Profile ID: " + get_ProfileID(ubl_dict))
    # print("ID: " + get_ID(ubl_dict))
    # print("Issue Date: " + str(get_IssueDate(ubl_dict)))
    # print("Invoice Type Code: " + str(get_InvoiceTypeCode(ubl_dict)))
import os

import requests

from api_adapter.constants import RENDER_BASE_URL
from api_adapter.database import get_invoices
from api_adapter.render_json import conv_xml_format


def save_invoice_locally(invoice_contents):
    directory = "invoices/"
    filename = "invoice.xml"
    file_path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    file = open(file_path, "w")
    file.write(invoice_contents)
    file.close()
    return file_path


def get_render(token: str, invoice_id: int) -> dict:
    unformatted_invoice_contents = get_invoice_contents(token, invoice_id)
    invoice_contents = conv_xml_format(unformatted_invoice_contents)
    upload_url = f"{RENDER_BASE_URL}upload"

    file_path = save_invoice_locally(invoice_contents)
    files = {
        "file": ("invoice.xml", open(file_path, "rb"), "text/xml"),
    }
    headers = {
        "Content-Disposition": 'form-data; name="file"; filename="'
        + "invoice.xml"
        + '"',
        "Content-Type": "text/xml",
    }
    res = requests.post(upload_url, files=files, headers=headers)
    print(res.text)
    """if res.ok:
        download_url = (
            f"{RENDER_BASE_URL}download?file_id={res.json()['file_id']}&file_type=HTML"
        )
        response = requests.get(download_url)
        return {"msg": "RENDERED", "html": response.text}"""
    if res.ok:
        return {"msg": "RENDERED", "html": res.text}
    return {"msg": "Error rendering"}


def get_invoice_contents(token, id):
    invoices, msg = get_invoices(token)
    return invoices[id]["content"]

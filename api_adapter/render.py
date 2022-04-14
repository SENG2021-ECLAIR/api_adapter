import os

import requests

from api_adapter.constants import RENDER_BASE_URL
from api_adapter.database import get_invoices


def get_invoice_contents(token, id):
    invoices, msg = get_invoices(token)
    return invoices["created"][id]["content"] + invoices["received"][id]["content"]


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
    invoice_contents = get_invoice_contents(token, invoice_id)
    upload_url = f"{RENDER_BASE_URL}upload"

    file_path = save_invoice_locally(invoice_contents)
    files = {"file": open(file_path, "rb")}
    res = requests.post(upload_url, files=files)
    print(res.text)
    if res.ok:
        file_id = res.json()["file_ids"][0]
        print(file_id)
        download_url = f"{RENDER_BASE_URL}download?file_id={file_id}&file_type=HTML"
        response = requests.get(download_url)
        print(response.text)
        return {"msg": "Successfully rendered invoice as html", "html": response.text}
    return {"msg": "Error rendering invoice"}

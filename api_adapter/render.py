import os

import requests

from api_adapter.constants import RENDER_BASE_URL
from api_adapter.database import get_invoices


def get_render(input):
    data = {
        "file": input["file"]
    }
    upload_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
    post_val = requests.post(upload_url, files=data)
    print(post_val)

    assert post_val.status_code == 200
    if post_val.status_code == 200:
        download_url = f"{RENDER_BASE_URL}download?file_id={post_val.json()['file_id']}&file_type=HTML"
        response = requests.get(download_url)
        return {"msg": "Rendered", "html": response.text}
    return {"msg": "Error rendering"}



# def save_invoice_locally(invoice_contents):
#     directory = "invoices/"
#     filename = "invoice.xml"
#     file_path = os.path.join(directory, filename)
#     if not os.path.isdir(directory):
#         os.mkdir(directory)

#     file = open(file_path, "w")
#     file.write(invoice_contents)
#     file.close()
#     return file_path


# def get_render(token: str, invoice_id: int) -> dict:
#     invoice_contents = get_invoice_contents(token, invoice_id)
#     upload_url = f"{RENDER_BASE_URL}upload"

#     file_path = save_invoice_locally(invoice_contents)
#     files = {
#         "file": ("invoice.xml", open(file_path, "rb"), "text/xml"),
#     }
#     res = requests.post(upload_url, files=files)
#     print(res)
#     if res.ok:
#         download_url = (
#             f"{RENDER_BASE_URL}download?file_id={res.json()['file_id']}&file_type=HTML"
#         )
#         response = requests.get(download_url)
#         return {"msg": "RENDERED", "html": response.text}
#     return {"msg": "Error rendering"}


# def get_invoice_contents(token, id):
#     invoices, msg = get_invoices(token)
#     return invoices[id]["content"]

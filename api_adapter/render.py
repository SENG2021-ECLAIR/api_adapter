import os

import requests

from api_adapter.constants import RENDER_BASE_URL
from api_adapter.database import get_invoices
from api_adapter.render_json import conv_xml_format

# import zipfile


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
    file = {
        "file": ("invoice.xml", open(file_path, "rb"), "text/xml"),
    }

    res = requests.post(upload_url, files=file)
    print(f"\n\nRESPONSE:\n\n{res.json()['file_ids'][0]}\n\n")

    if res.ok:
        download_url = f"{RENDER_BASE_URL}download?file_id={res.json()['file_ids'][0]}&file_type=PDF"
        response = requests.get(download_url)

        # writing as zip file
        # https://edstem.org/au/courses/7693/discussion/807755?comment=1827786
        report_path = "zip_output4.zip"
        with open(report_path, "wb") as reportFile:
            reportFile.write(response.text.encode("utf-8"))

        return {"msg": "RENDERED", "content": response.text}

    return {"msg": "Error rendering"}


def get_invoice_contents(token, id):
    invoices, msg = get_invoices(token)

    for i in range(0, len(invoices["created"])):
        if invoices["created"][i]["invoice_id"] == id:
            return invoices["created"][i]["content"]
    for i in range(0, len(invoices["received"])):
        if invoices["received"][i]["invoice_id"] == id:
            return invoices["received"][i]["content"]
    return None


if __name__ == "__main__":
    return_value = get_render("79bc4516-face-4716-aa71-14f62a91f785", 323)
    # print(f"\n\RETURN VALUE:\n\n{return_value}\n\n")
    # zipObj = zipfile.ZipFile("zip_output1.zip", "w")
    # with zipfile.ZipFile("zip_output1.zip", "w") as myzip:
    #     myzip.write(return_value["PDF"])

    # f = open("zip_output.zip", "w")
    # f.write(return_value["PDF"])
    # f.close()

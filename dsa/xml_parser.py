import xml.etree.ElementTree as ET
import json
import re

def parse_sms_xml(xml_file):
    """
    Parse the XML file and convert SMS records into a list of dictionaries
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []
    transaction_id = 1

    for sms in root.findall("sms"):
        body = sms.attrib.get("body", "")
        readable_date = sms.attrib.get("readable_date", "")
        address = sms.attrib.get("address", "")

        # Extract amount using regular expressions
        amount_match = re.search(r'(\d[\d,]*) RWF', body)
        amount = amount_match.group(1).replace(",", "") if amount_match else "0"

        # Determine transactions types
        body_lower = body.lower()
        if "received" in body_lower:
            tx_type = "received"
        elif "payment" in body_lower:
            tx_type = "payment"
        elif "transferred" in body_lower:
            tx_type = "transferred"
        elif "bank deposit" in body_lower:
            tx_type = "bank deposit"
        else:
            tx_type = "Unkown"

        transaction = {
            "id": transaction_id,
            "address": address,
            "type": tx_type,
            "amount": amount,
            "date": readable_date,
            "raw_message": body
        }

        transactions.append(transaction)
        transaction_id += 1

    return transactions

def save_to_json(data, output_file):
    """
    Save list of transactions to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    xml_file = "../modified_sms_v2.xml"
    output_file = "transactions.json"

    transactions = parse_sms_xml(xml_file)
    save_to_json(transactions, output_file)

    print(f"** Parsed {len(transactions)} transactions successfully. ** ...")
    print("** Data save to transactions.json **")

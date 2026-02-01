from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import os

# Load transactions from JSON file
TRANSACTIONS_FILE = os.path.join(os.path.dirname(__file__), "../dsa/transactions.json")

def load_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)

transactions = load_transactions()

class TransactionHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def _parse_id(self, path):
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                return int(parts[1])
            except ValueError:
                return None
            
        return None
    
    # GET requests
    def do_GET(self):
        parsed_path = urlparse(self.path)
        tx_id = self._parse_id(parsed_path.path)

        if parsed_path.path == "/transactions":
            self._set_headers()
            self.wfile.write(json.dumps(transactions).encode())

        elif tx_id:
            tx = next((t for t in transactions if t["id"] == tx_id), None)
            if tx:
                self._set_headers()
                self.wfile.write(json.dumps(tx).encode())

            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    # POST requests
    def do_POST(self):
        if self.path != "/transactions":
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
            return
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            new_tx = json.loads(body)
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return
        
        new_id = max([t["id"] for t in transactions], default=0) + 1
        new_tx["id"] = new_id
        transactions.append(new_tx)
        save_transactions(transactions)

        self._set_headers(201)
        self.wfile.write(json.dumps(new_tx).encode())

    # PUT requests
    def do_PUT(self):
        tx_id = self._parse_id(self.path)
        if not tx_id:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            return
        
        tx = next((t for t in transactions if t["id"] == tx_id), None)
        if not tx:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            return
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            updated_data = json.loads(body)
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return
        
        tx.update(updated_data)
        save_transactions(transactions)

        self._set_headers()
        self.wfile.write(json.dumps(tx).encode())

    # DELETE requests
    def do_DELETE(self):
        tx_id = self._parse_id(self.path)
        if not tx_id:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
            return
        
        global transactions
        tx = next((t for t in transactions if t["id"] == tx_id), None)
        if not tx:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            return
        
        transactions = [t for t in transactions if t["id"] != tx_id]
        save_transactions(transactions)

        self._set_headers(204)
        self.wfile.write(b"")


def run(server_class=HTTPServer, handler_class=TransactionHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

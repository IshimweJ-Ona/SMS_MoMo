from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import os
import base64

# ============================================================
# AUTHENTICATION CONFIGURATION
# ============================================================
# Valid credentials for Basic Authentication
# In production, these should be stored securely (environment variables, database, etc.)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

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
    
    # ============================================================
    # BASIC AUTHENTICATION IMPLEMENTATION
    # ============================================================
    def _authenticate(self):
        """
        Validates Basic Authentication credentials.
        
        Basic Auth format: "Basic base64(username:password)"
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        auth_header = self.headers.get("Authorization")
        
        # Check if Authorization header exists
        if not auth_header:
            return False
        
        # Check if it's Basic Authentication
        if not auth_header.startswith("Basic "):
            return False
        
        try:
            # Extract and decode the base64 credentials
            # Format: "Basic base64_encoded_credentials"
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            
            # Split into username and password
            # Format: "username:password"
            username, password = decoded_credentials.split(":", 1)
            
            # Validate credentials
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                return True
            else:
                return False
                
        except (IndexError, ValueError, base64.binascii.Error):
            # Handle malformed Authorization header
            return False
    
    def _send_unauthorized(self):
        """
        Sends 401 Unauthorized response with WWW-Authenticate header.
        This prompts the client to provide authentication credentials.
        """
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_header("WWW-Authenticate", 'Basic realm="MoMo Transaction API"')
        self.end_headers()
        response = {
            "error": "Unauthorized",
            "message": "Invalid or missing authentication credentials. Please provide valid Basic Authentication."
        }
        self.wfile.write(json.dumps(response).encode())
    
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
        # ============================================================
        # AUTHENTICATION CHECK - All endpoints are protected
        # ============================================================
        if not self._authenticate():
            self._send_unauthorized()
            return
        
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
        # ============================================================
        # AUTHENTICATION CHECK - All endpoints are protected
        # ============================================================
        if not self._authenticate():
            self._send_unauthorized()
            return
        
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
        # ============================================================
        # AUTHENTICATION CHECK - All endpoints are protected
        # ============================================================
        if not self._authenticate():
            self._send_unauthorized()
            return
        
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
        # ============================================================
        # AUTHENTICATION CHECK - All endpoints are protected
        # ============================================================
        if not self._authenticate():
            self._send_unauthorized()
            return
        
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

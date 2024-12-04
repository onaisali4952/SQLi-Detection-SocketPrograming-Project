import socket
import threading
import sqlite3
from regularExpressions import is_sql_injection

# Server configuration
HOST = "127.0.0.1"  # Localhost
PORT = 9999         # Port

# SQLite Database setup
DB_FILE = "simple_db.db"


def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # UNSAFE query concatenation (for testing SQL Injection)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Executing query: {query}")  # Log query for debugging purposes
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user is not None


def fetch_employee_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_table")
    rows = cursor.fetchall()
    conn.close()
    return rows


def handle_client(client_socket, client_address):
    print(f"[INFO] Client connected: {client_address}")
    authenticated = False
    
    while True:
        try:
            if not authenticated:
                client_socket.send(b"Login (format: LOGIN <username> <password>):\n")
            else:
                client_socket.send(b"Enter command (VIEW_EMPLOYEE_DATA to browse, EXIT to disconnect):\n")
            
            client_input = client_socket.recv(1024).decode("utf-8").strip()
            
            if client_input.lower() == "exit":
                print(f"[INFO] Client disconnected: {client_address}")
                client_socket.send(b"Goodbye!\n")
                break

            if is_sql_injection(client_input):
                print(f"[WARNING] SQL Injection attempt detected from {client_address}. Disconnecting client...")
                client_socket.send(b"SQL Injection detected! Disconnecting...")
                with open("log_attackPrevented.log", "a") as file:
                    file.write(f"{client_input}\n")
                break
            
            if not authenticated:
                # Handle login
                if client_input.startswith("LOGIN"):
                    _, username, password = client_input.split(maxsplit=2)
                    if authenticate_user(username, password):
                        authenticated = True
                        client_socket.send(b"Login successful! You can now browse the database.\n")
                    else:
                        client_socket.send(b"Invalid credentials. Try again.\n")
                else:
                    client_socket.send(b"Please login first.\n")
            else:
                if client_input.upper() == "VIEW_EMPLOYEE_DATA":
                    data = fetch_employee_data()
                    response = "\n".join([f"{row[0]}: {row[1]} - {row[2]} (Created: {row[3]})" for row in data])
                    client_socket.send(f"Employee Table Contents:\n{response}\n".encode("utf-8"))
                else:
                    client_socket.send(b"Unknown command.\n")
        
        except Exception as e:
            print(f"[ERROR] Connection error with {client_address}: {e}")
            break
    
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Allow up to 5 simultaneous connections
    print(f"[INFO] Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
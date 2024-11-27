import socket
import threading

from regularExpressions import is_sql_injection

# Server configuration
HOST = "127.0.0.1"  # Localhost
PORT = 9999         # Port

# This function is made to handle the client connections that will be made with the server
def handle_client(client_socket, client_address):
    print(f"[INFO] Client connected: {client_address}")
    
    while True:
        try:
            # Receive data from the client
            client_socket.send(b"Enter your input (type 'exit' to disconnect):\n")
            client_input = client_socket.recv(1024).decode("utf-8").strip()
            
            # Disconnect on 'exit' command
            if client_input.lower() == "exit":
                print(f"[INFO] Client disconnected: {client_address}")
                client_socket.send(b"Goodbye!\n")
                break
            
            # Check for SQL injection
            if is_sql_injection(client_input):
                print(f"[WARNING] SQL Injection attempt detected from {client_address}. Disconnecting client...")
                client_socket.send(b"SQL Injection detected! Disconnecting...\n")
                # Log blocked input for further inspection (to evaluate false positives)
                with open("log_attackPrevented.log", "a") as file:
                    string_to_write = '\n'+client_input
                    file.write(string_to_write+'\n')
                break  # Disconnect the client
            else:
                
                response = f"Processed input: {client_input}\n"
                print(response)
                # Log allowed input for further inspection (to evaluate true negatives)
                with open("log_safeInput.log", "a") as file:
                    string_to_write = '\n'+client_input
                    file.write(string_to_write+'\n')
                client_socket.send(response.encode("utf-8"))
        except Exception as e:
            print(f"[ERROR] Connection error with {client_address}: {e}")
            break
    
    client_socket.close()

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Allow up to 5 simultaneous connections
    print(f"[INFO] Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, client_address = server.accept()
        # Handle each client in a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()

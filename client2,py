import socket

# Client configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, SERVER_PORT))
        print("[INFO] Connected to server")
        
        while True:
            # Receive welcome or response message
            server_message = client.recv(1024).decode("utf-8").strip()
            print(f"\nServer: {server_message}")

            # If an attempt at an SQL injection is detected, the client will be disconnected
            if server_message == "SQL Injection detected! Disconnecting...":
                break
            
            # Send user input
            user_input = input("Your Input: ")
            client.send(user_input.encode("utf-8"))
            
            if user_input.lower() == "exit":
                print("[INFO] Disconnecting...")
                break
            
            # Receive server response
            response = client.recv(1024).decode("utf-8").strip()
            print(f"Server: {response}")

if __name__ == "__main__":
    start_client()

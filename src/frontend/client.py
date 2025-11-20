import socket
import json
import os
import threading

SOCKET_PATH = "/tmp/scheduler_socket"

class SchedulerClient:
    def __init__(self, update_callback):
        self.server_sock = None
        self.conn = None
        self.running = False
        self.update_callback = update_callback

    def start_server(self):
        """Starts listening for the C backend to connect."""
        # Clean up old socket file if it exists
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        try:
            self.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.server_sock.bind(SOCKET_PATH)
            self.server_sock.listen(1)
            
            # Start a background thread to accept the connection
            thread = threading.Thread(target=self.accept_connection, daemon=True)
            thread.start()
            return True
        except Exception as e:
            print(f"Server Init Error: {e}")
            return False

    def accept_connection(self):
        """Waits for C backend to connect, then starts reading data."""
        try:
            # print("Waiting for C backend to connect...")
            self.conn, addr = self.server_sock.accept()
            # print("C Backend Connected!")
            self.running = True
            self.listen()
        except Exception as e:
            print(f"Accept Error: {e}")

    def listen(self):
        """Continuously reads JSON data from the connected C backend."""
        buffer = ""
        while self.running and self.conn:
            try:
                data = self.conn.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        try:
                            json_data = json.loads(line)
                            # Update UI on the main thread
                            self.update_callback(json_data)
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                print(f"Data Read Error: {e}")
                self.running = False
                break
        
        self.close()

    def close(self):
        self.running = False
        if self.conn:
            self.conn.close()
        if self.server_sock:
            self.server_sock.close()
        # Clean up the socket file
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
import socket
import json
import os
import threading

SOCKET_PATH = "/tmp/scheduler_socket"

class IPCServer:
    def __init__(self, on_data_received, on_disconnected):
        self.sock = None
        self.conn = None
        self.running = False
        self.on_data_received = on_data_received
        self.on_disconnected = on_disconnected # New Callback

    def start(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.bind(SOCKET_PATH)
            self.sock.listen(1)
            threading.Thread(target=self._accept_connection, daemon=True).start()
            return True
        except Exception as e:
            print(f"IPC Init Error: {e}")
            return False

    def _accept_connection(self):
        print("Waiting for C process...")
        try:
            self.conn, addr = self.sock.accept()
            print("C Process Connected!")
            self.running = True
            self._listen_loop()
        except Exception as e:
            print(f"Connection Error: {e}")

    def _listen_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.conn.recv(4096).decode('utf-8')
                if not data: 
                    break # Connection closed by C backend
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        try:
                            json_data = json.loads(line)
                            self.on_data_received(json_data)
                        except json.JSONDecodeError:
                            pass
            except:
                break
        
        # Connection lost/finished
        print("Simulation Finished (Connection Closed)")
        self.cleanup()
        self.on_disconnected() # Notify UI

    def cleanup(self):
        self.running = False
        if self.conn: 
            try: self.conn.close()
            except: pass
        if self.sock: 
            try: self.sock.close()
            except: pass
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
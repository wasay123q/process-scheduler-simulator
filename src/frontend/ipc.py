import socket
import json
import os
import threading

class IPCServer:
    def __init__(self, socket_path, on_data_received, on_disconnected):
        self.socket_path = socket_path
        self.sock = None
        self.conn = None
        self.running = False
        self.on_data_received = on_data_received
        self.on_disconnected = on_disconnected

    def start(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.bind(self.socket_path)
            self.sock.listen(1)
            threading.Thread(target=self._accept_connection, daemon=True).start()
            return True
        except Exception:
            return False

    def _accept_connection(self):
        try:
            self.conn, addr = self.sock.accept()
            self.running = True
            self._listen_loop()
        except: pass

    def _listen_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.conn.recv(4096).decode('utf-8')
                if not data: break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        try:
                            self.on_data_received(json.loads(line))
                        except: pass
            except: break
        
        self.cleanup()
        self.on_disconnected()

    def cleanup(self):
        self.running = False
        if self.conn: 
            try: self.conn.close()
            except: pass
        if self.sock: 
            try: self.sock.close()
            except: pass
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
import socket
from threading import Thread

class ProxyServer(Thread):

    def __init__(self, host, port):
        super(ProxyServer, self).__init__()
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connection((host, port))

    def run(self):
        while True:
            data = self.server.recv(port)
            if data:
                self.game.sendall(data)

class GameProxy(Thread):
    def __init__(self, host, port):
        super(GameProxy, self).__init__()
        self.server = None
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        self.game, addr = sock.accept()
    
    def run(self):
        while True:
            data = self.game.recv(port)
            if data:
                self.server.sendall(data)

class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
    
    def run(self):
        while True:
            print("[Proxy({})] setting up".format(self.port))
            self.g2p = GameProxy(self.from_host, self.port)
            self.p2s = ProxyServer(self.to_host, self.port)
            print("[proxy({})] connection established".format(self.port))
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            self.g2p.start()
            self.p2s.start()

master_server = Proxy('0.0.0.0', 'ip', port)
master_server.start()







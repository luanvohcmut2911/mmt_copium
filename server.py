import socket
import threading
import json
class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connections = {}
    self.peerHost = {}
  
  def clientHandle(self, clientSocket, clientAddress):
    while True:
      clientMessage = clientSocket.recv(1024).decode('utf-8')
      print(f"Client send to server: {clientMessage}")
      if(clientMessage.split(" ")[0] == "peerHost:"):
        peerServerHostName = clientMessage.split(' ')[1]
        self.peerHost[clientAddress[1]] = peerServerHostName
        print(f"Current peerHost: {self.peerHost}")
      elif (clientMessage == "get peer host"):
        clientSocket.sendall(json.dumps(self.peerHost).encode('utf-8'))
  def run(self):
    self.serverSocket.bind((self.host, self.port))
    self.serverSocket.listen(5)
    print(f"Server starts running on {self.host}/{self.port}")
    while True:
      try:
        clientSocket, clientAddress = self.serverSocket.accept()
        print(f"{clientAddress} is connect to server")
        self.connections[clientAddress[1]] = clientSocket
        clientHandler = threading.Thread(daemon = True, target=self.clientHandle, args=(clientSocket, clientAddress))
        clientHandler.start()
      except Exception as e:
        print(f'Error in connection {e}')
        
  def close(self):
    for key in self.connections:
      self.connections[key].close()
    self.serverSocket.close()
    
    
    
if __name__ == '__main__':
  try:
    host = '127.0.0.1'
    port = 8080
    server = Server(host, port)
    server.run()  
  except KeyboardInterrupt:
    server.close()
    
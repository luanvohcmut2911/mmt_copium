import socket
import threading

class ServerInClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
  def clientHandle(self, clientSocket, clientAddress):
    clientMessage = clientSocket.recv(1024).decode('utf-8')
    print(f"Client send to server: {clientMessage}") 
    
  def run(self):
    self.serverSocket.bind((self.host, self.port))
    self.serverSocket.listen(5)
    print(f"Peer server starts running on {self.host}/{self.port}")
    while True:
      try:
        clientSocket, clientAddress = self.serverSocket.accept()
        self.connections[clientAddress[1]] = clientSocket
        clientHandler = threading.Thread(daemon = True, target=self.clientHandle, args=(clientSocket, clientAddress))
        clientHandler.start()
      except Exception as e:
        print(f'Error in connection {e}')
        
  def close(self):
    for key in self.connections:
      self.connections[key].close()
    self.serverSocket.close()   
    
class ClientInClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port


class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
  def broadcast(self):
    serverMessage = self.clientSocket.recv(1024).decode('utf-8')
    print(f"Server return to message: {serverMessage}")
    
  def sendCommand(self, command):
    print(command)
    self.clientSocket.send(command.encode('utf-8'))
  
  def connect(self):
    try:
      self.clientSocket. connect((self.host, self.port))
      self.sendCommand(f'peerHost: {host}/{self.clientSocket.getsockname()[1] % 100}')
      
      broadCastHandler = threading.Thread(daemon = True,target = self.broadcast)
      broadCastHandler.start()
      
      # if success, start server in client
      serverInClient = ServerInClient(self.host, self.clientSocket.getsockname()[1] % 100)
      serverInClientHandler = threading.Thread(target=serverInClient.run)
      serverInClientHandler.start()
      # print(self.clientSocket.getsockname())

    except Exception as e:
      print(f"Error in client: {e}")
      
  def close(self):
    self.clientSocket.close()
      
  
if __name__ == '__main__':
  try:
    # host and port of server
    host = '127.0.0.1'
    port = 8080
    client = Client(host, port)
    client.connect()
    while True:
      inputCommand = input("Enter your command:")
      if(inputCommand == "get list"):
        client.sendCommand(f'get peer host')
  except KeyboardInterrupt:
    client.close()
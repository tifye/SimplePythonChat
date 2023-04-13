import socket

class ChatClient(object):

    def __init__(self):
        self.bConnected = False
        self.sock = None

        self.pollFreq = 200

    def disconnect(self):
        """Disconnects from server and
        sets the state of the program to 'disconnected'
        """
        if self.bConnected:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

        self.bConnected = False
   
    def tryToConnect(self, ipPort):
        """Attempts to connect to Server
        
        Returns a Boolean on wether was successfull or not
        """
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock.settimeout(0.1)

        try:
            self.sock.connect(ipPort)
            self.bConnected = True
            self.sock.setblocking(False)
            return True
        except socket.timeout:
            del self.sock
            self.sock = None
            return False


    # attempt to send the message (in the text field g_app.textIn) to the server
    def sendMessage(self, message):
        try:
            print(message)
            self.sock.sendall(message)
            return True
        except socket.error:
            self.disconnect()
            return False

    # poll messages
    def pollMessages(self):
        if self.bConnected:
            try:
                data = self.sock.recv(2048)
                if not data:
                    raise socket.error
                else:
                    return data
            except socket.error:
                return None



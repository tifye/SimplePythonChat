import tkinter as tk
from GUIclient import Application
from ChatClient import ChatClient
import json

# TODO #

# Validate address format before calling tryConnect

########

class Controller(object):

    def __init__(self):
        self.chatClient = ChatClient()

        # launch the gui
        self._root = tk.Tk()
        self.view = Application(self, master=self._root)
        
        # make sure everything is set to the status 'disconnected' at the beginning
        self.disconnect()

        # schedule the next call to pollMessages
        self._root.after(self.chatClient.pollFreq, self.pollMessages)

        # if attempt to close the window, handle it in the on-closing method
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.view.mainloop()

    def clearButtonClick(self):
        """Clear chat field"""
        self.view.msgText.configure(state=tk.NORMAL)
        self.view.msgText.delete(1.0, tk.END)
        self.view.msgText.see(tk.END)
        self.view.msgText.configure(state=tk.DISABLED)

    def sendButtonClick(self):
        """forward to the sendMessage method"""
        self.sendMessage()

    def sendMessage(self, message="meep", event = None):
        # forward to the sendMessage method
        # If connected to anything
        if self.chatClient.bConnected:
            # If message was not successfully sent
            if not self.chatClient.sendMessage(bytearray(message, "utf-8")):
                self.printToMessages("Failed to send message. You have been disconned from the server")
                self.disconnect()
            else:
                # Clear sendMessage field
                self.view.textIn.config(state = tk.NORMAL)
                self.view.textIn.delete(0, tk.END)
        else:
            self.printToMessages("You are not connected to any server.")

    def connectButtonClick(self):
        """forward to the connect handler"""
        self.connectHandler()

    def connectHandler(self, event = None):
        """connectHandler toggles the status between connected/disconnected"""
        if self.chatClient.bConnected:
            self.disconnect()
        else:
            ipPortStr = self.view.ipPort.get()        
            ipPort = self.tupleAddrFormat(ipPortStr)

            print(ipPort)

            if self.chatClient.tryToConnect(ipPort):
                self.view.connectButton['text'] = 'disconnect'
            else:
                self.view.connectButton['text'] = 'connect'


    def disconnect(self):
        """Discoonect and Update UI"""
        self.chatClient.disconnect()

        self.view.connectButton['text'] = 'connect'

    def printToMessages(self, message):
        """A utility method to print to the message field"""    
        self.view.msgText.configure(state=tk.NORMAL)
        self.view.msgText.insert(tk.END, message + '\n')
        # scroll to the end, so the new message is visible at the bottom
        self.view.msgText.see(tk.END)
        self.view.msgText.configure(state=tk.DISABLED)

    def on_closing(self):
        """When closing, quit application responsibly"""
        if self.chatClient.bConnected:
            if self.view.askokcancel("Quit", 
                    "You are still connected. If you quit you will be"
                    + " disconnected."):
                self.myQuit()
        else:
            self.myQuit()
           
    def myQuit(self):
        """Quit application responibly"""
        self.chatClient.disconnect()
        self._root.destroy()
    
    def tupleAddrFormat(self, string):
        """Taken as <ip>:<port>"""
        t = tuple(str(string).split(":"))
        return (t[0], int(t[1]))

    def myAddrFormat(self, addr):
        """Convert address to string of format <ip>:<port>"""
        return '{}:{}'.format(addr[0], addr[1])

    def pollMessages(self):
        # reschedule the next polling event
        self._root.after(self.chatClient.pollFreq, self.pollMessages)

        message = self.chatClient.pollMessages()
        if message is not None:
            self.printToMessages(message.decode("utf-8"))

    def left(self):
        message = {
            "type": 4,
            "command": "left"
        }
        jsonString = json.dumps(message)
        self.sendMessage(jsonString)
        pass

    def right(self):
        message = {
            "type": 4,
            "command": "right"
        }
        message = json.dumps(message)
        self.sendMessage(message)
        pass

    def forward(self):
        message = {
            "type": 4,
            "command": "forward"
        }
        message = json.dumps(message)
        self.sendMessage(message)
        pass

    def backward(self):
        message = {
            "type": 4,
            "command": "backward"
        }
        message = json.dumps(message)
        self.sendMessage(message)
        pass



if __name__ == '__main__':
    controller = Controller()
import tkinter as tk
from ChatServerView import View
from ChatServer import ChatServer


class ChatServerController(object):

    def __init__(self):
        self.chatServer = ChatServer()
        self.chatServer._messenger.messageDelegate = self
        self.chatServer.delegate = self

        # Launch the GUI
        self._root = tk.Tk()
        self.view = View(self, master=self._root)

        # If attempt to close the window, handle it in the on-closing method
        self._root.protocol("WM_DELETE_WINDOW", self.onClosing)     

        self.view.mainloop()

    def broadcastButtonClicked(self):
        self.broadcastMessage()

    def broadcastMessage(self, event=None):
        message = self.view.broadcastEntry.get()
        if message:
            self.chatServer.broadcastMessage(message)

            self.view.broadcastEntry.config(state=tk.NORMAL)
            self.view.broadcastEntry.delete(0, tk.END)

    #----Connection Stuff-----------------------------------------
    def disconnectServer(self):
        """Disconnect Server"""
        self.chatServer.disconnect()
        self.view.connectButton['text'] = 'Go up'

    def disconnectAllClients(self):
        """Disconnect all client"""
        for client in self.chatServer.getClientSocket():
            self.chatServer.disconnectClient(client)

    def disconnectClient(self):
        """Diconnect client sleceted in list of clients"""
        selected = self.view.clientsListField.curselection()
        if len(selected) > 0:
            index = selected[0]
            self.chatServer.disconnectClientAtIndex(index)

    def connectButtonClicked(self):
        self.connectHandler()

    def connectHandler(self, event=None):
        """Handle trying to start up the server"""
        if self.chatServer.running:
            self.disconnectServer()
            #self.printToMessages("Server shut down.")
        else:
            # Get portnumber from textfield
            portString = self.view.portEntry.get()
            try: 
                # Try converting to integer
                port = int(portString)
                if port > 65535: raise ValueError
            except ValueError:
                # Present error in ui
                self.printWarning("Invalid port number")
            else:
                # Try connecting
                if self.chatServer.connect(port):
                    # Schedule the call to pollMessage
                    self._root.after(self.chatServer.pollFreq, self.pollMessages)

                    self.view.connectButton['text'] = 'Go down'
                    #self.printToMessages("Running server on: {}".format(self.chatServer.getIpPort()))
                else:
                    self.view.connectButton['text'] = 'Go up'
                    self.printWarning("")
            
    
    def messageClientButtonClicked(self):
        self.messageClient()

    def messageClient(self, event=None):
        message = self.view.messageEntry.get()
        selectedClient = self.view.clientsListField.curselection()
        if message and len(selectedClient) > 0:
            index = selectedClient[0]
            self.chatServer.sendMessageToClientAtIndex(index, message)

            self.view.messageEntry.config(state=tk.NORMAL)
            self.view.messageEntry.delete(0, tk.END)
            

    #----Connection Stuff------------------------------------------
    def pollMessages(self):
        if self.chatServer.running:
            self._root.after(self.chatServer.pollFreq, self.pollMessages)
            self.chatServer.pollMessages()

    #----Extra Stuff---------------------------------------------------
    def printWarning(self, errorMsg):
        self.printToMessages("!!-{}-!!".format(errorMsg))

    def message(self, message):
        self.printToMessages(message)

    def clientConnected(self, clientID):
        self.view.clientsListField.insert(tk.END, clientID)

    def clientDisconnectedAtIndex(self, index):
        self.view.clientsListField.delete(index)

    def printToMessages(self, message):
        """Print to message field"""
        self.view.messagesField.configure(state=tk.NORMAL)
        self.view.messagesField.insert(tk.END, message + '\n')
        # Scroll to the end, so the new message is visible at the bottom
        self.view.messagesField.see(tk.END)
        self.view.messagesField.configure(state=tk.DISABLED)

    def clearButtonClicked(self):
        """Clear messages field of all text"""
        self.view.messagesField.configure(state=tk.NORMAL)
        self.view.messagesField.delete(1.0, tk.END)
        self.view.messagesField.see(tk.END)
        self.view.messagesField.configure(state=tk.DISABLED)

    def onClosing(self):
        """When closing, quit application responsibly"""
        if self.chatServer.running:
            if self.view.askokcancel("Quit", "Server is still running, if you quit it will be shit down"):
                self.quit()
        else:
            self.quit()

    def quit(self):
        """Quit application responsibly"""
        self.chatServer.disconnect()
        self._root.destroy()

controller = ChatServerController()
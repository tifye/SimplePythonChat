import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt

class Application(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)

        self.controller = controller

        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(tk.END, 'localhost:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', self.controller.connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,
            command = self.controller.connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = self.controller.clearButtonClick)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', self.controller.sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = self.controller.sendButtonClick)
        self.sendButton.pack(side="left")
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

        # -------------------------------------------------------------------
        # row 3: sending messages
        # -------------------------------------------------------------------
        self.groupControls = tk.LabelFrame(bd=0)
        self.groupControls.pack(side="top")
        #
        self.left = tk.Button(self.groupControls, text="<", command=self.controller.left)
        self.left.pack(side="left")
        #
        self.right = tk.Button(self.groupControls, text=">", command=self.controller.right)
        self.right.pack(side="left")
        #
        self.forward = tk.Button(self.groupControls, text="^", command=self.controller.forward)
        self.forward.pack(side="left")
        #
        self.backward = tk.Button(self.groupControls, text="v", command=self.controller.backward)
        self.backward.pack(side="left")


    def askokcancel(self, title, message):
        return tkmsgbox.askokcancel(title, message)



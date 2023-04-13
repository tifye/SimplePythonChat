import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
from enum import IntEnum


class Colors(IntEnum):
    bg1 = 0
    bg2 = 1
    fg1 = 2
    fg2 = 3


class View(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)

        self.controller = controller

        master.resizable(0, 0)

        self.colors = ["#1a1a2e", "#16213e", "#fddb3a", "#e94560"]
        # self.colors = ["#364f6b", "#3fc1c9", "#f5f5f5", "#fc5185"]
        # self.colors = ["#222831", "#393e46", "#00adb5", "#eeeeee"]
        # self.colors = ["#000000", "#6a097d", "#c060a1", "#f1d4d4"]

        self.pack()
        self.create_widgets()
        self.color_widgets()
        master['bg'] = self.colors[0]

    def create_widgets(self):
        # =======#--------------------------------------------------
        # left Group
        # =======#--------------------------------------------------
        self.leftGroup = tk.LabelFrame(bd=0, relief="flat")
        self.leftGroup.pack(side="left")
        # -                                               -#
        # --------------------------------------------------
        # row 1: IP-Port input | Go Up/Down btn | Clear messages btn
        # --------------------------------------------------
        self.connectionGroup = tk.LabelFrame(self.leftGroup, bd=1, text="Connection", relief="ridge")
        self.connectionGroup.pack(side="top")
        # -
        self.portLabel = tk.Label(self.connectionGroup, text='IP:port', padx=10)
        self.portLabel.pack(side="left")
        # -
        self.portEntry = tk.Entry(self.connectionGroup, width=20)
        self.portEntry.insert(tk.END, '60003')
        self.portEntry.bind('<Return>', self.controller.connectHandler)
        self.portEntry.pack(side="left")
        # -
        self.paddingLabel1 = tk.Label(self.connectionGroup, padx=5)
        self.paddingLabel1.pack(side="left")
        # -
        self.connectButton = tk.Button(self.connectionGroup, text="Go up",
                                       command=self.controller.connectButtonClicked, width=10)
        self.connectButton.pack(side="left")
        # -
        self.paddingLabel2 = tk.Label(self.connectionGroup, padx=1)
        self.paddingLabel2.pack(side="left")
        # -
        self.clearMessagesButton = tk.Button(self.connectionGroup, text='Clear messages',
                                             command=self.controller.clearButtonClicked)
        self.clearMessagesButton.pack(side="left")
        # -
        self.paddingLabel3 = tk.Label(self.connectionGroup, padx=5)
        self.paddingLabel3.pack(side="left")
        # -
        # -
        # --------------------------------------------------
        # row 2: ScrolledText field
        # --------------------------------------------------
        self.messageFieldGroup = tk.LabelFrame(self.leftGroup, bd=5, relief="flat")
        self.messageFieldGroup.pack(side="top")
        # -
        self.messagesField = tksctxt.ScrolledText(self.messageFieldGroup, height=30, width=70)
        self.messagesField.pack(side="top")
        # -
        # -
        # =======#--------------------------------------------------
        # right Group
        # =======#--------------------------------------------------
        self.rightGroup = tk.LabelFrame(bd=0, relief="flat", width=45)
        self.rightGroup.pack(side="right", fill="both", expand=True)
        # -                                               -#
        # --------------------------------------------------
        # row 3: Broadcast input + button
        # --------------------------------------------------
        self.broadcastGroup = tk.LabelFrame(self.rightGroup, bd=0, relief="flat")
        self.broadcastGroup.pack(side="top", pady=10)
        # -
        self.broadcastInputLabel = tk.Label(self.broadcastGroup, text="Broadcast message", padx=4)
        self.broadcastInputLabel.pack(side="left")
        # -
        self.broadcastEntry = tk.Entry(self.broadcastGroup, width=50)
        self.broadcastEntry.bind('<Return>', self.controller.broadcastMessage)
        self.broadcastEntry.pack(side="left")
        # -
        self.paddingLabel4 = tk.Label(self.broadcastGroup, padx=5)
        self.paddingLabel4.pack(side="left")
        # -
        self.broadcastButton = tk.Button(self.broadcastGroup, text="Send to all",
                                         command=self.controller.broadcastButtonClicked)
        self.broadcastButton.pack(side="right")
        # -
        # -
        # --------------------------------------------------
        # row 4: Connected clients field | Disconnect all/ Disconnect selected
        # --------------------------------------------------
        self.clientsGroup = tk.LabelFrame(self.rightGroup, bd=1, relief="ridge", text="Connected Clients")
        self.clientsGroup.pack(side="top", fill="both", expand=True)
        # -
        # self.clientsListField = tksctxt.ScrolledText(self.clientsGroup, height=22, width=60, relief="flat")
        self.clientsListField = tk.Listbox(self.clientsGroup, bd=0, height=18, width=30, relief="flat",
                                           selectborderwidth=0, highlightthickness=0,
                                           highlightcolor=self.colors[Colors.fg1])
        self.clientsListField.pack(side="bottom", fill="both", expand=True)
        # -
        self.paddingLabel6 = tk.Label(self.clientsGroup, padx=5, text="-^.-_-^¨*-,_- ")
        self.paddingLabel6.pack(side="left")
        # -
        self.disconnectClientButton = tk.Button(self.clientsGroup,
                                                text="Disconnect selected",
                                                command=self.controller.disconnectClient)
        self.disconnectClientButton.pack(side="left")
        # -
        self.clientFieldLabel = tk.Label(self.clientsGroup, text="-^.-_-^¨*-,_-*~,-_-^¨*-,_-*~- ", padx=5)
        self.clientFieldLabel.pack(side="left")
        # -
        self.disconnectAllButton = tk.Button(self.clientsGroup,
                                             text="Disconnect all",
                                             command=self.controller.disconnectAllClients)
        self.disconnectAllButton.pack(side="left")
        # -
        self.paddingLabel7 = tk.Label(self.clientsGroup, padx=5, text="-^.-_-^¨*-")
        self.paddingLabel7.pack(side="left")
        # -
        # -
        # --------------------------------------------------
        # row 5: Individual message input + button
        # --------------------------------------------------
        self.messageGroup = tk.LabelFrame(self.rightGroup, bd=0, relief="flat")
        self.messageGroup.pack(side="bottom")
        # -
        self.messageInputLabel = tk.Label(self.messageGroup, text="Individual message", padx=4)
        self.messageInputLabel.pack(side="left")
        # -
        self.messageEntry = tk.Entry(self.messageGroup, width=48)
        self.messageEntry.bind('<Return>', self.controller.messageClient)
        self.messageEntry.pack(side="left")
        # -
        self.paddingLabel5 = tk.Label(self.messageGroup, padx=5)
        self.paddingLabel5.pack(side="left")
        # -
        self.messageButton = tk.Button(self.messageGroup, text="Send to selected",
                                       command=self.controller.messageClientButtonClicked)
        self.messageButton.pack(side="right")

    def color_widgets(self):
        backgroundList1 = [
            # --Row 1--
            self.leftGroup,
            self.connectionGroup,
            self.portLabel,
            self.paddingLabel1,
            self.paddingLabel2,
            self.paddingLabel3,
            # --Row 2--
            # --Row 3--
            self.rightGroup,
            self.broadcastGroup,
            self.broadcastInputLabel,
            self.paddingLabel4,
            # --Row 4--
            self.clientsGroup,
            self.clientFieldLabel,
            self.disconnectClientButton,
            self.disconnectAllButton,
            self.clientsListField,
            self.paddingLabel6,
            self.paddingLabel7,
            # --Row 5--
            self.messageGroup,
            self.messageInputLabel,
            self.paddingLabel5
        ]

        backgroundList2 = [
            # --Row 1--
            self.connectButton,
            self.clearMessagesButton,
            self.portEntry,
            # --Row 2--
            self.messageFieldGroup,
            self.messagesField,
            # --Row 3--
            self.broadcastEntry,
            self.broadcastButton,
            # --Row 4--

            # --Row 5--
            self.messageEntry,
            self.messageButton
        ]

        foregroundList1 = [
            # --Row 1--
            # --Row 2--
            self.messagesField,
            # --Row 3--
            # --Row 4--
            self.clientsListField
            # --Row 5--
        ]

        foregroundList2 = [
            # --Row 1--
            self.connectionGroup,
            self.portEntry,
            self.connectButton,
            self.clearMessagesButton,
            self.portLabel,
            # --Row 2--
            # --Row 3--
            self.broadcastInputLabel,
            self.broadcastEntry,
            self.broadcastButton,
            # --Row 4--
            self.clientFieldLabel,
            self.disconnectClientButton,
            self.disconnectAllButton,
            self.clientsGroup,
            self.paddingLabel6,
            self.paddingLabel7,
            # --Row 5--
            self.messageEntry,
            self.messageButton,
            self.messageInputLabel
        ]

        self.clientsListField['highlightcolor'] = self.colors[Colors.fg1]

        for obj in backgroundList1:
            obj['bg'] = self.colors[Colors.bg1]

        for obj in backgroundList2:
            obj['bg'] = self.colors[Colors.bg2]

        for obj in foregroundList1:
            obj['fg'] = self.colors[Colors.fg1]

        for obj in foregroundList2:
            obj['fg'] = self.colors[Colors.fg2]

    @staticmethod
    def askokcancel(title, message):
        return tkmsgbox.askokcancel(title, message)

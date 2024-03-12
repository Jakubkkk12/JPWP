import tkinter as tk

from python_guis.main_gui import MainGUI

APPNAME = 'appname'
VERSION = '0.0.1'
WINDOW_ICON_PATH = 'resources/APP_ICON_512.png'

class LoginGUI:
    def __init__(self):
        self.root = tk.Tk()
        # ######## WINDOW PARAMETERS ######## #
        # title
        self.root.title(APPNAME + ' ' + VERSION + ' Login')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        # size parameters
        width = 1000
        height = 800
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # background color
        self.root.configure(bg='grey')

        # ######## FUNCTIONS ######## #

        lblUsername = tk.Label(self.root, text='Username:', bg='grey')
        lblUsername.place(x=400, y=220, width=200, height=30)

        self.usernameEntry = tk.Entry(self.root)
        self.usernameEntry.place(x=400, y=250, width=200, height=30)

        lblPassword = tk.Label(self.root, text='Password:', bg='grey')
        lblPassword.place(x=400, y=280, width=200, height=30)

        self.entryPassword = tk.Entry(self.root, show='*')
        self.entryPassword.place(x=400, y=310, width=200, height=30)

        lblSSHPassword = tk.Label(self.root, text='SSH password (optional):', bg='grey')
        lblSSHPassword.place(x=400, y=340, width=200, height=30)

        self.entrySSHPassword = tk.Entry(self.root, show='*')
        self.entrySSHPassword.place(x=400, y=370, width=200, height=30)

        btnLogin = tk.Button(self.root, text='Login', command=self.validate_credentials)
        btnLogin.place(x=400, y=410, width=200, height=30)
        btnLogin.configure(highlightcolor='black')

        btnQuit = tk.Button(self.root, text='Quit', command=self.root.destroy)
        btnQuit.place(x=890, y=750, width=100, height=30)

        self.root.mainloop()

    def validate_credentials(self):
        username = self.usernameEntry.get()
        password = self.entryPassword.get()
        sshPassword = self.entrySSHPassword.get()
        self.root.destroy()
        MainGUI()
         # if correct:
         #    run maingui
         # else error
import tkinter as tk
from gui_resources import config
from PIL import Image, ImageTk

APPNAME = config.APPNAME
VERSION = config.VERSION
BG_COLOR = config.BG_COLOR

WINDOW_ICON_PATH = 'gui_resources/APP_ICON_512.png'
LOGIN_ICON_PATH = 'gui_resources/LOGIN_512.png'


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
        width = 400
        height = 400
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # background color
        self.root.configure(bg=BG_COLOR)

        # ######## FUNCTIONS ######## #

        lblUsername = tk.Label(self.root, text='Username:', bg=BG_COLOR)
        lblUsername.place(x=100, y=50, width=200, height=30)

        self.usernameEntry = tk.Entry(self.root)
        self.usernameEntry.place(x=100, y=80, width=200, height=30)

        lblPassword = tk.Label(self.root, text='Password:', bg=BG_COLOR)
        lblPassword.place(x=100, y=110, width=200, height=30)

        self.entryPassword = tk.Entry(self.root, show='*')
        self.entryPassword.place(x=100, y=140, width=200, height=30)

        lblSSHPassword = tk.Label(self.root, text='SSH password (optional):', bg=BG_COLOR)
        lblSSHPassword.place(x=100, y=170, width=200, height=30)

        self.entrySSHPassword = tk.Entry(self.root, show='*')
        self.entrySSHPassword.place(x=100, y=200, width=200, height=30)

        LOGIN_ICON = Image.open(LOGIN_ICON_PATH)
        LOGIN_ICON = LOGIN_ICON.resize((24, 24))
        tk_icon = ImageTk.PhotoImage(LOGIN_ICON)
        btnLogin = tk.Button(self.root, text='Login', image=tk_icon, compound=tk.RIGHT,
                             command=self.validate_credentials)
        btnLogin.place(x=100, y=240, width=200, height=30)

        btnQuit = tk.Button(self.root, text='Quit', command=self.root.destroy)
        btnQuit.place(x=150, y=310, width=100, height=30)

        self.root.mainloop()

    def validate_credentials(self):
        username = self.usernameEntry.get()
        password = self.entryPassword.get()
        sshPassword = self.entrySSHPassword.get()
        self.root.destroy()

        from main_gui import MainGUI
        MainGUI()

         # if correct:
         #    run maingui
         # else error


if __name__ == '__main__':
    LoginGUI()
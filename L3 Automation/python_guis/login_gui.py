import tkinter as tk
from gui_resources import config
from PIL import Image, ImageTk

APPNAME = config.APPNAME
VERSION = config.VERSION
BG_COLOR = config.BG_COLOR

WINDOW_ICON_PATH = config.WINDOW_ICON_PATH
LOGIN_ICON_PATH = config.LOGIN_ICON_PATH


class LoginGUI:
    def __init__(self):
        self.root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        self.root.title(APPNAME + ' ' + VERSION + ' Login')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        # size parameters
        width = 300
        height = 220
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)

        self.root.minsize(width, height)

        # background color
        self.root.configure(bg=BG_COLOR)

        top_margin = tk.Frame(self.root, bg=BG_COLOR, height=10)
        top_margin.pack()

        lblUsername = tk.Label(self.root, text='Username:', bg=BG_COLOR)
        lblUsername.pack()

        self.usernameEntry = tk.Entry(self.root)
        self.usernameEntry.pack(fill='x', padx=50)

        lblPassword = tk.Label(self.root, text='Password:', bg=BG_COLOR)
        lblPassword.pack()

        self.entryPassword = tk.Entry(self.root, show='*')
        self.entryPassword.pack(fill='x', padx=50)

        LOGIN_ICON = Image.open(LOGIN_ICON_PATH)
        LOGIN_ICON = LOGIN_ICON.resize((24, 24))
        tk_icon = ImageTk.PhotoImage(LOGIN_ICON)
        btnLogin = tk.Button(self.root, text='Login', image=tk_icon, compound=tk.RIGHT,
                             command=self.validate_credentials)
        btnLogin.pack(pady=5)

        btnCancel = tk.Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.pack(pady=5)

        self.root.mainloop()

    def validate_credentials(self):
        username = self.usernameEntry.get()
        password = self.entryPassword.get()
        self.root.destroy()

        # import has to be there to avoid circular imports
        from main_gui import MainGUI
        MainGUI()

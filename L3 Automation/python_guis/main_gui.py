import tkinter as tk
import ssh_password_gui
from gui_resources import config
from login_gui import LoginGUI
from PIL import Image, ImageTk

APPNAME = config.APPNAME
VERSION = config.VERSION
BG_COLOR = config.BG_COLOR
WINDOW_ICON_PATH = 'gui_resources/APP_ICON_512.png'
QUIT_ICON_PATH = 'gui_resources/QUIT_512.png'


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        # title
        self.root.title(APPNAME + ' ' + VERSION)

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        # setting window size
        width = 800
        height = 800
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.root.configure(bg=BG_COLOR)

        # Header labels in 'ALL' section
        lblHostnameHeader = tk.Label(self.root, text='Hostname')
        lblStateHeader = tk.Label(self.root, text='State')
        lblRIPHeader = tk.Label(self.root, text='RIP')
        lblOSPFHeader = tk.Label(self.root, text='OSPF')
        lblBGPHeader = tk.Label(self.root, text='BGP')

        headerLabels = [lblHostnameHeader, lblStateHeader, lblRIPHeader, lblOSPFHeader, lblBGPHeader]
        x = 5  # starting point for headers
        for header in headerLabels:
            header.place(x=x, y=70, width=80, height=30)
            header.configure(bg=BG_COLOR, bd=2, relief='solid')
            x = x + 80

        self.lstbxRouters = tk.Listbox(self.root)
        self.lstbxRouters["borderwidth"] = "1px"
        self.lstbxRouters["fg"] = "#333333"
        self.lstbxRouters["justify"] = "center"
        self.lstbxRouters.place(x=5, y=100, width=680, height=650)
        self.lstbxRouters.configure(bg=BG_COLOR)

        # Sample data:
        routers = {
            "R1": {'ip': '10.1.1.11'},
            "R2": {'ip': '10.1.1.22'}
        }
        # Loading data to listbox, change padx parameter to move
        for router in routers:
            item_frame = tk.Frame(self.lstbxRouters)
            item_frame.pack(fill='x')

            lblHostname = tk.Label(item_frame, text=router)
            lblHostname.pack(side='left', padx=20)
            lblIP = tk.Label(item_frame, text=routers[router]['ip'])
            lblIP.pack(side='left', padx=20)

            button = tk.Button(item_frame, text='Download config')
            button.pack(side='right')

        # Buttons
        btnAll = tk.Button(self.root, text='All', command=self.btnAll_command)
        btnRIP = tk.Button(self.root, text='RIP', command=self.btnRIP_command)
        btnOSPF = tk.Button(self.root, text='OSPF', command=self.btnOSPF_command)
        btnBGP = tk.Button(self.root, text='BGP', command=self.btnBGP_command)

        buttons = [btnAll, btnRIP, btnOSPF, btnBGP]
        x = 5  # starting point
        for button in buttons:
            button.place(x=x, y=5, width=70, height=30)
            x = x + 70

        btnAddRouter = tk.Button(self.root, text='Add Router', command=self.btnAddRouter_command)
        btnAddRouter.place(x=695, y=100, width=100, height=30)

        btnSSHPassword = tk.Button(self.root, text='SSH Password', command=ssh_password_gui.SSHPasswordGUI)
        btnSSHPassword.place(x=695, y=5, width=100, height=30)

        btnLogOut = tk.Button(self.root, text='Log Out', command=self.btnLogOut_command)
        btnLogOut.place(x=725, y=735, width=70, height=30)

        QUIT_ICON = Image.open(QUIT_ICON_PATH)
        QUIT_ICON = QUIT_ICON.resize((24, 24))
        quit_icon = ImageTk.PhotoImage(QUIT_ICON)
        btnQuit = tk.Button(self.root, text='Quit', image=quit_icon, compound=tk.RIGHT, command=self.root.destroy)
        btnQuit.place(x=725, y=765, width=70, height=30)

        self.root.mainloop()

    def btnLogOut_command(self) -> None:
        self.root.destroy()
        LoginGUI()
        return None

    def btnAddRouter_command(self):
        return

    def btnAll_command(self):
        return

    def btnRIP_command(self):
        self.lstbxRouters.delete(0, tk.END)

    def btnBGP_command(self):
        return

    def btnOSPF_command(self):
        return


if __name__ == "__main__":
    MainGUI()

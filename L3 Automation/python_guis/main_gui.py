import tkinter as tk
import ssh_password_gui
from resources import config

APPNAME = 'appname'
VERSION = '0.0.1'
WINDOW_ICON_PATH = 'resources/APP_ICON_512.png'
COLOR = config.COLOR

class MainGUI:
    def __init__(self):
        root = tk.Tk()
        # title
        root.title(APPNAME + ' ' + VERSION)

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        #setting window size
        width=800
        height=800
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        root.configure(bg='grey')

        lblHostnameHeader = tk.Label(root, text='Hostname')
        lblHostnameHeader.place(x=5, y=70, width=60, height=30) # min=60
        lblHostnameHeader.configure(bg='grey', bd=2, relief='solid')

        lblStateHeader = tk.Label(root, text='State')
        lblStateHeader.place(x=65, y=70, width=50, height=30)
        lblStateHeader.configure(bg='grey', bd=2, relief='solid')

        lblRIPHeader = tk.Label(root, text='RIP')
        lblRIPHeader.place(x=115, y=70, width=50, height=30)
        lblRIPHeader.configure(bg='grey', bd=2, relief='solid')

        lblOSPFHeader = tk.Label(root, text='OSPF')
        lblOSPFHeader.place(x=165, y=70, width=50, height=30)
        lblOSPFHeader.configure(bg='grey', bd=2, relief='solid')

        self.lstbxRouters = tk.Listbox(root)
        self.lstbxRouters["borderwidth"] = "1px"
        self.lstbxRouters["fg"] = "#333333"
        self.lstbxRouters["justify"] = "center"
        self.lstbxRouters.place(x=5,y=100,width=680,height=650)
        self.lstbxRouters.configure(bg='grey')

        # Sample data:
        routers = {
            "R1": "123",
            "R2": "123131313"
        }
        # Loading data to listbox
        for router in routers:
            item_frame = tk.Frame(self.lstbxRouters)
            item_frame.pack(fill='x')
            label = tk.Label(item_frame, text=router)
            label.pack(side='left', padx=5)
            button = tk.Button(item_frame, text='Action')
            button.pack(side='right')

        # Buttons
        btnAll=tk.Button(root)
        btnAll["bg"] = "#f0f0f0"
        btnAll["fg"] = "#000000"
        btnAll["justify"] = "center"
        btnAll["text"] = "All"
        btnAll.place(x=5,y=5,width=70,height=30)
        btnAll["command"] = self.btnAll_command

        btnRIP=tk.Button(root)
        btnRIP["bg"] = "#f0f0f0"
        btnRIP["fg"] = "#000000"
        btnRIP["justify"] = "center"
        btnRIP["text"] = "RIP"
        btnRIP.place(x=75,y=5,width=70,height=30)
        btnRIP["command"] = self.btnRIP_command

        btnOSPF=tk.Button(root)
        btnOSPF["bg"] = "#f0f0f0"
        btnOSPF["fg"] = "#000000"
        btnOSPF["justify"] = "center"
        btnOSPF["text"] = "OSPF"
        btnOSPF.place(x=145,y=5,width=70,height=30)
        btnOSPF["command"] = self.btnOSPF_command

        btnBGP=tk.Button(root)
        btnBGP["bg"] = "#f0f0f0"
        btnBGP["fg"] = "#000000"
        btnBGP["justify"] = "center"
        btnBGP["text"] = "BGP"
        btnBGP.place(x=215,y=5,width=70,height=30)
        btnBGP["command"] = self.btnBGP_command

        btnAddRouter=tk.Button(root)
        btnAddRouter["bg"] = "#f0f0f0"
        btnAddRouter["fg"] = "#000000"
        btnAddRouter["justify"] = "center"
        btnAddRouter["text"] = "Add Router"
        btnAddRouter.place(x=695,y=100,width=100,height=30)
        btnAddRouter["command"] = self.btnAddRouter_command

        btnSSHPassword=tk.Button(root)
        btnSSHPassword["bg"] = "#f0f0f0"
        btnSSHPassword["fg"] = "#000000"
        btnSSHPassword["justify"] = "center"
        btnSSHPassword["text"] = "SSH Password"
        btnSSHPassword.place(x=695, y=5, width=100, height=30)
        btnSSHPassword["command"] = ssh_password_gui.SSHPasswordGUI

        btnLogOut=tk.Button(root)
        btnLogOut["bg"] = "#f0f0f0"
        btnLogOut["fg"] = "#000000"
        btnLogOut["justify"] = "center"
        btnLogOut["text"] = "Log out"
        btnLogOut.place(x=725,y=735,width=70,height=30)
        btnLogOut["command"] = self.btnLogOut_command

        btnQuit=tk.Button(root)
        btnQuit["bg"] = "#f0f0f0"
        btnQuit["fg"] = "#000000"
        btnQuit["justify"] = "center"
        btnQuit["text"] = "Quit"
        btnQuit.place(x=725,y=765,width=70,height=30)
        btnQuit["command"] = root.destroy

        root.mainloop()

    def btnSSHPassword_command(self):
        return
    def btnLogOut_command(self):
        return
    def btnAddRouter_command(self):
        return
    def btnAll_command(self):
        return
    def btnRIP_command(self):
        return
    def btnBGP_command(self):
        return
    def btnOSPF_command(self):
        return

if __name__ == "__main__":
    MainGUI()

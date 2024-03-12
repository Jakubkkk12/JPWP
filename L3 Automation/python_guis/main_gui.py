import tkinter as tk
from tkinter import ttk

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

        # Sample data:
        routers = [
            ('1', 'R1', '10.1.1.11'),
            ('2', 'R2', '10.1.1.22')
             ]
        columns = ('No', 'Hostname', 'IP')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.place(x=5, y=100, width=650, height=500)

        for router in routers:
            self.tree.insert('', tk.END, values=router)

        self.tree.heading('No', text='No',)
        self.tree.column('No', width=30)

        self.tree.heading('Hostname', text='Hostname')
        self.tree.column('Hostname', width=80)

        self.tree.heading('IP', text='IP')
        self.tree.column('IP', width=50)

        self.tree.bind('<Button-3>', self.show_content_menu)

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

        self.menu = tk.Menu(self.root)
        self.menu.add_command(label='test', command=self.do_test)

        self.root.mainloop()

    def show_content_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.menu.post(event.x_root, event.y_root)

    def do_test(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_text = self.tree.item(selected_item)['values']
            print(f'do something: {item_text}')

    def btnLogOut_command(self) -> None:
        self.root.destroy()
        LoginGUI()
        return None

    def btnAddRouter_command(self):
        return

    def btnAll_command(self):
        return

    def btnRIP_command(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    def btnBGP_command(self):
        return

    def btnOSPF_command(self):
        return


if __name__ == "__main__":
    MainGUI()

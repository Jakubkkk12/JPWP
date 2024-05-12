import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import get_info_router
from resources.devices.Router import Router
from resources.ssh.SSHInformation import SSHInformation
from resources.user.User import User


class AddRouterGUI:
    def __init__(self, main_gui, user: User):
        self.main_gui = main_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' Add router')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 400
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(300, 300)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Components
        lblHostname = tk.Label(root, text='Hostname:')
        lblHostname.grid(row=0, column=0)
        entryHostname = tk.Entry(root)
        entryHostname.grid(row=0, column=1)

        lblIPAddress = tk.Label(root, text='IP Address:')
        lblIPAddress.grid(row=1, column=0)

        addressFrame = tk.Frame(root)
        entryIPAddress = tk.Entry(addressFrame, width=10)
        entryIPAddress.pack(side='left')
        lblDot1 = tk.Label(addressFrame, text='.')
        lblDot1.pack(side='left')
        entryIPAddress2 = tk.Entry(addressFrame, width=10)
        entryIPAddress2.pack(side='left')
        lblDot2 = tk.Label(addressFrame, text='.')
        lblDot2.pack(side='left')
        entryIPAddress3 = tk.Entry(addressFrame, width=10)
        entryIPAddress3.pack(side='left')
        lblDot3 = tk.Label(addressFrame, text='.')
        lblDot3.pack(side='left')
        entryIPAddress4 = tk.Entry(addressFrame, width=10)
        entryIPAddress4.pack(side='left')

        addressFrame.grid(row=1, column=1)

        lblEnablePassword = tk.Label(root, text='Enable Password:')
        lblEnablePassword.grid(row=2, column=0)
        entryEnablePassword = tk.Entry(root, show='*')
        entryEnablePassword.grid(row=2, column=1)

        lblSSHPort = tk.Label(root, text='Port:')
        lblSSHPort.grid(row=3, column=0)
        entrySSHPort = tk.Entry(root, width=10)
        entrySSHPort.grid(row=3, column=1)
        entrySSHPort.insert(0, '22')

        lblType = tk.Label(root, text='Type:')
        lblType.grid(row=4, column=0)
        varOption = tk.StringVar()
        options = ['cisco_ios']  # 'mikrotik', 'juniper', 'huawei', 'other']
        optionType = tk.OptionMenu(root, varOption, *options)
        optionType.grid(row=4, column=1)

        def get_address() -> str:
            return (entryIPAddress.get() + '.' + entryIPAddress2.get() + '.' + entryIPAddress3.get() + '.' +
                    entryIPAddress4.get())

        def clean_entries():
            entryHostname.delete(0, tk.END)
            entryIPAddress.delete(0, tk.END)
            entryIPAddress2.delete(0, tk.END)
            entryIPAddress3.delete(0, tk.END)
            entryIPAddress4.delete(0, tk.END)
            entryEnablePassword.delete(0, tk.END)
            entrySSHPort.delete(0, tk.END)

        def validate_router() -> bool:
            hostname = entryHostname.get()
            if main_gui.router_exists(hostname):
                messagebox.showerror('Error', 'Router with this hostname already exists', parent=root)
                return False

            ip = get_address()
            try:
                ip = ipaddress.ip_address(ip)
            except ValueError:
                messagebox.showerror('Error', 'Invalid IP address', parent=root)
                return False

            ssh_password = entryEnablePassword.get()
            # check if ssh_password is correct

            ssh_port = entrySSHPort.get()
            if not ssh_port.isdigit() or not 0 < int(ssh_port) < 65536:
                messagebox.showerror('Error', 'Invalid port number', parent=root)
                return False

            type = varOption.get()
            if type not in options:
                messagebox.showerror('Error', 'Invalid type', parent=root)
                return False

            return True

        def add_router():
            if validate_router():
                router = Router(name=entryHostname.get(),
                                ssh_information=SSHInformation(ip_addresses={get_address(): get_address()}),
                                type=varOption.get(),
                                enable_password=entryEnablePassword.get())
                main_gui.project.devices[router.name] = router
                threading.Thread(target=get_info_router,
                                 args=(main_gui, router, user)).start()

                messagebox.showinfo('Success', 'Router added successfully', parent=root)
                clean_entries()

        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_router, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=5, column=1)

        root.mainloop()

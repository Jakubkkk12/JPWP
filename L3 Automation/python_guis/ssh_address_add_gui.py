import tkinter as tk
from tkinter import messagebox

from resources.devices.Router import Router
from python_guis.gui_resources import config
import ipaddress

from resources.ssh.SSHInformation import SSHInformation


class SSHAddressAddGUI:
    def __init__(self, router: Router, ssh_connections_gui):
        self.hostname = router.name
        self.ssh_connections_gui = ssh_connections_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' SSH Connections Add Address')

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

        lblAddress = tk.Label(root, text='Address:')

        NetworkFrame = tk.Frame(root)
        entryIPNetworkFirst = tk.Entry(NetworkFrame, width=10)
        entryIPNetworkFirst.pack(side='left')
        labelDot1 = tk.Label(NetworkFrame, text='.')
        labelDot1.pack(side='left')

        entryIPNetworkSecond = tk.Entry(NetworkFrame, width=10)
        entryIPNetworkSecond.pack(side='left')
        labelDot2 = tk.Label(NetworkFrame, text='.')
        labelDot2.pack(side='left')

        entryIPNetworkThird = tk.Entry(NetworkFrame, width=10)
        entryIPNetworkThird.pack(side='left')
        labelDot3 = tk.Label(NetworkFrame, text='.')
        labelDot3.pack(side='left')

        entryIPNetworkFourth = tk.Entry(NetworkFrame, width=10)
        entryIPNetworkFourth.pack(side='left')

        lblPort = tk.Label(root, text='Port:')
        entryPort = tk.Entry(root, width=5)

        lblAddress.pack()
        NetworkFrame.pack()
        lblPort.pack()
        entryPort.pack()

        def get_network() -> str:
            ip = (entryIPNetworkFirst.get() + '.' + entryIPNetworkSecond.get() + '.' + entryIPNetworkThird.get() + '.' +
                  entryIPNetworkFourth.get())
            try:
                ipaddress.ip_address(ip)
                return ip
            except ValueError:
                messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                clean_entries()

        def clean_entries() -> None:
            ip_entries = [entryIPNetworkFirst, entryIPNetworkSecond, entryIPNetworkThird,
                          entryIPNetworkFourth]
            for entry in ip_entries:
                entry.delete(0, 'end')
            entryPort.delete(0, 'end')

        def validate_network() -> bool:
            ip_entries = [entryIPNetworkFirst, entryIPNetworkSecond, entryIPNetworkThird, entryIPNetworkFourth]
            network = ''
            for entry in ip_entries:
                value = entry.get()
                network += value + '.'
            network = network.rstrip('.')
            try:
                ipaddress.ip_address(network)
            except ValueError:
                messagebox.showerror('Error', 'Incorrect Network', parent=root)
                clean_entries()
                return False

            port = entryPort.get()
            if not port.isdigit() or not 0 <= int(port) <= 65535:
                messagebox.showerror('Error', 'Incorrect Port', parent=root)
                entryPort.delete(0, 'end')
                return False
            return True

        def apply_network():
            if validate_network():
                network = get_network()
                port = entryPort.get()
                messagebox.showinfo('Address added', 'Address added', parent=root)
                clean_entries()

                router.ssh_information.ip_addresses[network] = network
                self.ssh_connections_gui.insert_address(network, port)

        btnApply = tk.Button(root, text='Apply', command=apply_network)
        btnApply.pack(pady=5)
        btnQuit = tk.Button(root, text='Quit', command=root.destroy)
        btnQuit.pack()

        root.mainloop()

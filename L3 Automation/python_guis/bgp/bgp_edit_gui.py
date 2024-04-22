import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from resources.connect_frontend_with_backend.frontend_backend_functions import update_bgp
from resources.devices.Router import Router
from python_guis.gui_resources import config
from resources.user.User import User


# todo punkt 16
class BGPEditGUI:
    def __init__(self, main_gui, router: Router, user: User):
        root = tk.Toplevel()
        main_gui = main_gui

        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' ' + ' Edit RIP ')
        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 400
        height = 400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(400, 400)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Components
        lblRouterID = tk.Label(root, text='Router ID')
        lblRouterID.grid(column=0, row=1)

        router_id_frame = tk.Frame(root)
        id_entry1 = tk.Entry(router_id_frame, width=5)
        id_entry1.insert(0, router.bgp.router_id.split('.')[0])
        id_entry1.pack(side=tk.LEFT)
        id_dot1 = tk.Label(router_id_frame, text='.')
        id_dot1.pack(side=tk.LEFT)
        id_entry2 = tk.Entry(router_id_frame, width=5)
        id_entry2.insert(0, router.bgp.router_id.split('.')[1])
        id_entry2.pack(side=tk.LEFT)
        id_dot2 = tk.Label(router_id_frame, text='.')
        id_dot2.pack(side=tk.LEFT)
        id_entry3 = tk.Entry(router_id_frame, width=5)
        id_entry3.insert(0, router.bgp.router_id.split('.')[2])
        id_entry3.pack(side=tk.LEFT)
        id_dot3 = tk.Label(router_id_frame, text='.')
        id_dot3.pack(side=tk.LEFT)
        id_entry4 = tk.Entry(router_id_frame, width=5)
        id_entry4.insert(0, router.bgp.router_id.split('.')[3])
        id_entry4.pack(side=tk.LEFT)
        router_id_frame.grid(column=1, row=1)

        lblDefaultInformationOriginate = tk.Label(root, text='Default Information Originate')
        lblDefaultInformationOriginate.grid(column=0, row=2)
        varDefaultInformationOriginate = tk.BooleanVar(root)
        chckbtnDefaultInformation = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        if router.bgp.default_information_originate is True:
            chckbtnDefaultInformation.select()
            varDefaultInformationOriginate.set(True)
        chckbtnDefaultInformation.grid(column=1, row=2)

        lblDefaultMetric = tk.Label(root, text='Default Metric of Redistributed Routes')
        lblDefaultMetric.grid(column=0, row=3)
        entryDefaultMetric = tk.Entry(root)
        entryDefaultMetric.insert(0, str(router.bgp.default_metric_of_redistributed_routes))
        entryDefaultMetric.grid(column=1, row=3)

        lblKeepAlive = tk.Label(root, text='Keep Alive Timer')
        lblKeepAlive.grid(column=0, row=4)
        entryKeepAlive = tk.Entry(root)
        entryKeepAlive.insert(0, str(router.bgp.timers.keep_alive))
        entryKeepAlive.grid(column=1, row=4)

        lblHoldTime = tk.Label(root, text='Hold Time Timer')
        lblHoldTime.grid(column=0, row=5)
        entryHoldTime = tk.Entry(root)
        entryHoldTime.insert(0, str(router.bgp.timers.hold_time))
        entryHoldTime.grid(column=1, row=5)

        def validate_changes():
            id_entries = [id_entry1, id_entry2, id_entry3, id_entry4]
            id = ''
            for entry in id_entries:
                value = entry.get()
                id += value + '.'
            id = id.rstrip('.')
            try:
                ipaddress.ip_address(id)
            except ValueError:
                messagebox.showerror('Error', 'Router ID must be a valid IP address', parent=root)
                return False
            if not entryDefaultMetric.get().isdigit() or not (0 <= int(entryDefaultMetric.get()) <= 255):
                messagebox.showerror('Error', 'Default Metric must be an integer between 0 and 255', parent=root)
                entryDefaultMetric.delete(0, tk.END)
                return False
            if not entryKeepAlive.get().isdigit() or not (0 <= int(entryKeepAlive.get()) <= 65535):
                messagebox.showerror('Error', 'Keep Alive Timer must be an integer between 0 and 65535', parent=root)
                entryKeepAlive.delete(0, tk.END)
                return False
            if not entryHoldTime.get().isdigit() or not (0 <= int(entryHoldTime.get()) <= 65535):
                messagebox.showerror('Error', 'Hold Time Timer must be an integer between 0 and 65535', parent=root)
                entryHoldTime.delete(0, tk.END)
                return False
            return True

        def get_id_address() -> str:
            return f'{id_entry1.get()}.{id_entry2.get()}.{id_entry3.get()}.{id_entry4.get()}'

        def apply_changes():
            if validate_changes():
                threading.Thread(target=update_bgp,
                                 args=(main_gui, router, user, get_id_address(), varDefaultInformationOriginate.get(),
                                       int(entryDefaultMetric.get()), int(entryKeepAlive.get()),
                                       int(entryHoldTime.get()))).start()
                root.destroy()

        btnFrame = tk.Frame(root)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_changes)
        btnApply.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy)
        btnCancel.pack()
        btnFrame.grid(column=0, row=6, columnspan=2)

        root.mainloop()

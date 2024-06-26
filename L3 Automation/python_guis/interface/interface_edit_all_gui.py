import threading
import tkinter as tk
from tkinter import messagebox

from resources.connect_frontend_with_backend.frontend_backend_functions import update_interface_basic
from resources.devices.Router import Router
from python_guis.gui_resources import config
from resources.user.User import User


class EditInterfaceGUI:
    def __init__(self, main_gui, interfaces_details_gui, router: Router, user: User, int_name: str, iid: int):
        root = tk.Toplevel()
        self.interfaces_details_gui = interfaces_details_gui

        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' ' + ' Edit Interface ' + int_name)
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
        lblIPAddress = tk.Label(root, text='IP Address:', pady=10)
        lblIPAddress.grid(column=0, row=0)

        entryIPAddressFrame = tk.Frame(root)

        entryIPAddressFirst = tk.Entry(entryIPAddressFrame, width=10)
        entryIPAddressFirst.pack(side='left')
        labelDot1 = tk.Label(entryIPAddressFrame, text='.')
        labelDot1.pack(side='left')

        entryIPAddressSecond = tk.Entry(entryIPAddressFrame, width=10)
        entryIPAddressSecond.pack(side='left')
        labelDot2 = tk.Label(entryIPAddressFrame, text='.')
        labelDot2.pack(side='left')

        entryIPAddressThird = tk.Entry(entryIPAddressFrame, width=10)
        entryIPAddressThird.pack(side='left')
        labelDot3 = tk.Label(entryIPAddressFrame, text='.')
        labelDot3.pack(side='left')

        entryIPAddressFourth = tk.Entry(entryIPAddressFrame, width=10)
        entryIPAddressFourth.pack(side='left')

        def get_ip_address() -> str:
            new_ip = (entryIPAddressFirst.get() + '.' + entryIPAddressSecond.get() + '.' + entryIPAddressThird.get() +
                      '.' + entryIPAddressFourth.get())
            return new_ip

        def get_mask() -> int:
            return int(entryMask.get())

        def get_mtu() -> int:
            return int(entryMTU.get())

        def get_description() -> str:
            return entryDescription.get()

        def refill_with_current_ip() -> None:
            if router.interfaces[int_name].ip_address != 'unassigned':
                ip_entries = [entryIPAddressFirst, entryIPAddressSecond, entryIPAddressThird, entryIPAddressFourth]

                currentIP = router.interfaces[int_name].ip_address
                octets = currentIP.split('.')
                i = 0
                for entry in ip_entries:
                    entry.insert(0, octets[i])
                    i += 1
            return None

        refill_with_current_ip()
        entryIPAddressFrame.grid(column=1, row=0)

        lblMask = tk.Label(root, text='Mask:')
        lblMask.grid(column=0, row=1)
        entryMask = tk.Entry(root)
        entryMask.insert(0, str(router.interfaces[int_name].subnet))
        entryMask.grid(column=1, row=1)

        lblDuplex = tk.Label(root, text='Duplex:')
        lblDuplex.grid(column=0, row=2)
        duplexOptions = ['Full', 'Half', 'Auto']
        duplexVariable = tk.StringVar(root)
        duplexVariable.set(router.interfaces[int_name].statistics.information.duplex)
        duplexOptions.remove((duplexVariable.get().capitalize()))
        optionMenuDuplex = tk.OptionMenu(root, duplexVariable, *duplexOptions)
        optionMenuDuplex.grid(column=1, row=2)

        def get_speed_options() -> list[str]:
            if router.type == 'cisco_ios':
                if 'GigabitEthernet' in int_name:
                    return ['1000Mbps', '100Mbps', '10Mbps']
                if 'FastEthernet' in int_name:
                    return ['100Mbps', '10Mbps']
                if 'Serial' in int_name:
                    return ['None']
            # todo: add other types

        if 'Serial' not in int_name:
            lblSpeed = tk.Label(root, text='Speed:')
            lblSpeed.grid(column=0, row=3)
            speedOptions = get_speed_options()
            speedVariable = tk.StringVar(root)
            speedVariable.set(router.interfaces[int_name].statistics.information.speed)
            optionMenuSpeed = tk.OptionMenu(root, speedVariable, *speedOptions)
            optionMenuSpeed.grid(column=1, row=3)

        lblMTU = tk.Label(root, text='MTU (bytes):')
        lblMTU.grid(column=0, row=4)
        entryMTU = tk.Entry(root)
        entryMTU.insert(0, str(router.interfaces[int_name].statistics.information.mtu))
        entryMTU.grid(column=1, row=4)

        lblDescription = tk.Label(root, text='Description:')
        lblDescription.grid(column=0, row=5)
        entryDescription = tk.Entry(root)
        if router.interfaces[int_name].description is not None:
            entryDescription.insert(0, router.interfaces[int_name].description)
        entryDescription.grid(column=1, row=5)

        def validate_changes() -> bool:
            ip_entries = [entryIPAddressFirst, entryIPAddressSecond, entryIPAddressThird, entryIPAddressFourth]

            for entry in ip_entries:
                value = entry.get()
                if not value.isdigit() or not (0 <= int(value) <= 255):
                    messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                    for entry in ip_entries:
                        entry.delete(0, 'end')
                    return False
            try:
                if int(entryIPAddressFirst.get()) == 0:
                    messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                    for entry in ip_entries:
                        entry.delete(0, 'end')
                    return False
            except ValueError:
                return False

            mask_value = entryMask.get()
            if not mask_value.isdigit() or not (0 <= int(mask_value) <= 32):
                messagebox.showerror('Error', 'Incorrect Mask Value', parent=root)
                entryMask.delete(0, 'end')
                return False

            mtu_value = entryMTU.get()
            if not mtu_value.isdigit() or not (1500 <= int(mtu_value) <= 10240):
                messagebox.showerror('Error', 'Incorrect MTU Size (1500 - 10240)', parent=root)
                entryMTU.delete(0, 'end')
                return False

            return True

        def apply_changes():
            if validate_changes():
                if 'Serial' in int_name:
                    threading.Thread(target=update_interface_basic,
                                     args=(main_gui, interfaces_details_gui, router, user, router.interfaces[int_name],
                                           get_description(), get_ip_address(), get_mask(), 'None', 'None'
                                           , get_mtu())).start()
                else:
                    threading.Thread(target=update_interface_basic,
                                     args=(main_gui, interfaces_details_gui, router, user, router.interfaces[int_name],
                                           get_description(), get_ip_address(), get_mask(), duplexVariable.get(),
                                           speedVariable.get(), get_mtu())).start()

                root.destroy()

        btnFrame = tk.Frame(root, pady=10)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_changes, width=30)
        btnApply.pack()

        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=30)
        btnCancel.pack()
        btnFrame.grid(column=0, row=6, columnspan=2, sticky='s')

        root.mainloop()

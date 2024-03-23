import tkinter as tk
from tkinter import messagebox

from resources.devices.Router import Router
from gui_resources import config


class EditInterfaceOSPFGUI:
    def __init__(self, router: Router, int_name: str, iid: int, ospf_interfaces_details_gui):
        root = tk.Toplevel()
        self.ospf_interfaces_details_gui = ospf_interfaces_details_gui

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
        lblNetworkType = tk.Label(root, text='Network type')
        lblNetworkType.grid(column=0, row=0)
        networkTypeOption = ['broadcast', 'point-to-point', 'non-broadcast']
        typeVariable = tk.StringVar(root)
        typeVariable.set(router.interfaces[int_name].ospf.network_type)
        optionMenuType = tk.OptionMenu(root, typeVariable, *networkTypeOption)
        optionMenuType.grid(column=1, row=0)

        lblCost = tk.Label(root, text='Cost:')
        lblCost.grid(column=0, row=1)
        entryCost = tk.Entry(root)
        entryCost.insert(0, str(router.interfaces[int_name].ospf.cost))
        entryCost.grid(column=1, row=1)

        lblPassiveInterface = tk.Label(root, text='Passive interface:')
        lblPassiveInterface.grid(column=0, row=2)
        chckbtnVar = tk.BooleanVar(root)
        chckbtnPassiveInterface = tk.Checkbutton(root, variable=chckbtnVar)
        if router.interfaces[int_name].ospf.passive_interface is True:
            chckbtnPassiveInterface.select()
            chckbtnVar = True
        else:
            chckbtnPassiveInterface.deselect()
            chckbtnVar = False
        chckbtnPassiveInterface.grid(column=1, row=2)

        lblPriority = tk.Label(root, text='Priority:')
        lblPriority.grid(column=0, row=3)
        entryPriority = tk.Entry(root)
        entryPriority.insert(0, str(router.interfaces[int_name].ospf.priority))
        entryPriority.grid(column=1, row=3)

        lblHelloTimer = tk.Label(root, text='Hello timer:')
        lblHelloTimer.grid(column=0, row=4)
        entryHelloTimer = tk.Entry(root)
        entryHelloTimer.insert(0, str(router.interfaces[int_name].ospf.timers.hello_timer))
        entryHelloTimer.grid(column=1, row=4)

        lblDeadTimer = tk.Label(root, text='Dead timer:')
        lblDeadTimer.grid(column=0, row=5)
        entryDeadTimer = tk.Entry(root)
        entryDeadTimer.insert(0, str(router.interfaces[int_name].ospf.timers.dead_timer))
        entryDeadTimer.grid(column=1, row=5)

        lblWaitTimer = tk.Label(root, text='Wait timer:')
        lblWaitTimer.grid(column=0, row=6)
        entryWaitTimer = tk.Entry(root)
        entryWaitTimer.insert(0, str(router.interfaces[int_name].ospf.timers.wait_timer))
        entryWaitTimer.grid(column=1, row=6)

        lblRetransmitTimer = tk.Label(root, text='Retransmit timer:')
        lblRetransmitTimer.grid(column=0, row=7)
        entryRetransmitTimer = tk.Entry(root)
        entryRetransmitTimer.insert(0, str(router.interfaces[int_name].ospf.timers.retransmit_timer))
        entryRetransmitTimer.grid(column=1, row=7)

        def get_network_type() -> str:
            return typeVariable.get()

        def get_cost() -> int:
            return int(entryCost.get())

        def get_passive_interface() -> bool:
            return chckbtnVar

        def get_priority() -> int:
            return int(entryPriority.get())

        def get_hello_timer() -> int:
            return int(entryHelloTimer.get())

        def get_dead_timer() -> int:
            return int(entryDeadTimer.get())

        def get_wait_timer() -> int:
            return int(entryWaitTimer.get())

        def get_retransmit_timer() -> int:
            return int(entryRetransmitTimer.get())

        def validate_changes() -> bool:
            if not entryCost.get().isdigit() or not (0 <= int(entryCost.get())):
                messagebox.showerror('Error', 'Incorrect cost size', parent=root)
                entryCost.delete(0, 'end')
                return False
            if not entryPriority.get().isdigit() or not (0 <= int(entryPriority.get())):
                messagebox.showerror('Error', 'Incorrect priority size', parent=root)
                entryPriority.delete(0, 'end')
                return False
            if not entryHelloTimer.get().isdigit() or not (0 <= int(entryHelloTimer.get())):
                messagebox.showerror('Error', 'Incorrect hello timer', parent=root)
                entryHelloTimer.delete(0, 'end')
                return False
            if not entryDeadTimer.get().isdigit() or not (0 <= int(entryDeadTimer.get())):
                messagebox.showerror('Error', 'Incorrect dead timer', parent=root)
                entryDeadTimer.delete(0, 'end')
                return False
            if not entryWaitTimer.get().isdigit() or not (0 <= int(entryWaitTimer.get())):
                messagebox.showerror('Error', 'Incorrect wait timer', parent=root)
                entryWaitTimer.delete('Error', 'Incorrect wait timer')
                return False
            if not entryRetransmitTimer.get().isdigit() or not (0 <= int(entryRetransmitTimer.get())):
                messagebox.showerror('Error', 'Incorrect retransmit timer', parent=root)
                entryRetransmitTimer.delete(0, 'end')
                return False
            return True

        def apply_changes() -> None:
            if validate_changes():
                router.interfaces[int_name].ospf.network_type = get_network_type()
                router.interfaces[int_name].ospf.cost = get_cost()
                router.interfaces[int_name].ospf.passive_interface = get_passive_interface()
                router.interfaces[int_name].ospf.priority = get_priority()
                router.interfaces[int_name].ospf.timers.hello_timer = get_hello_timer()
                router.interfaces[int_name].ospf.timers.dead_timer = get_dead_timer()
                router.interfaces[int_name].ospf.timers.wait_timer = get_wait_timer()
                router.interfaces[int_name].ospf.timers.retransmit_timer = get_retransmit_timer()

            self.ospf_interfaces_details_gui.update_interface_details(iid, int_name, get_network_type(), get_cost(),
                                                                      get_passive_interface(), get_priority(),
                                                                      get_hello_timer(), get_dead_timer(),
                                                                      get_wait_timer(), get_retransmit_timer())
            root.destroy()

        btnFrame = tk.Frame(root, pady=10)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_changes, width=30)
        btnApply.pack()

        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=30)
        btnCancel.pack()
        btnFrame.grid(column=0, row=8, columnspan=2, sticky='s')

        root.mainloop()

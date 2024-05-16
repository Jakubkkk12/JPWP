import threading
import tkinter as tk
import tkinter.messagebox
from python_guis.gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import get_info_router

WINDOW_ICON_PATH = config.WINDOW_ICON_PATH
BG_COLOR = config.BG_COLOR


class EnablePasswordGUI:
    def __init__(self, main_gui, devices):
        self.main_gui = main_gui
        self.devices = devices
        self.root = tk.Toplevel()
        self.root.title('Enable password')

        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        width = 300
        height = 300
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        hostnames = []
        self.chckbtns = []
        self.vars = []
        for name, device in devices.items():
            hostnames.append(device.name)
        i, j = 0, 0
        for hostname in hostnames:
            lblHostname = tk.Label(self.root, text=hostname)
            lblHostname.grid(row=i, column=j)
            lblHostname.widgetName = f"lblHostname{i+1}"

            varHostname = tk.BooleanVar()
            chckbtnHostname = tk.Checkbutton(self.root, variable=varHostname)
            chckbtnHostname.grid(row=i, column=j+1)
            chckbtnHostname.widgetName = hostname
            self.chckbtns.append(chckbtnHostname)
            self.vars.append(varHostname)
            i += 1

        lblEnablePassword = tk.Label(self.root, text='Enable password:')
        lblEnablePassword.grid(row=i, column=0, columnspan=2, sticky='w')
        self.entryEnablePassword = tk.Entry(self.root, show='*')
        self.entryEnablePassword.grid(row=i, column=1, columnspan=2, sticky='e', padx=5)
        i += 1

        lblConfirmEnable = tk.Label(self.root, text='Confirm enable password:')
        lblConfirmEnable.grid(row=i, column=0, columnspan=2, sticky='w')
        self.entryConfirmEnable = tk.Entry(self.root, show='*')
        self.entryConfirmEnable.grid(row=i, column=1, columnspan=2, sticky='e', padx=5)
        i += 1

        btnApply = tk.Button(self.root, text='Apply', command=self.validate)
        btnApply.grid(row=i, column=0, columnspan=2)
        i += 1

        btnCancel = tk.Button(self.root, text='Cancel', command=self.root.destroy)
        btnCancel.grid(row=i, column=0, columnspan=2)

        self.root.mainloop()

    def validate(self) -> None:
        enable_pass = self.entryEnablePassword.get()
        enable_confirm_pass = self.entryConfirmEnable.get()

        if enable_pass != enable_confirm_pass:
            self.entryEnablePassword.delete(0, 'end')
            self.entryConfirmEnable.delete(0, 'end')
            tk.messagebox.showerror(title='Wrong credentials', message='Passwords must be the same.', parent=self.root)

        else:
            who_to_enable = [chckbtn.widgetName for chckbtn, var in zip(self.chckbtns, self.vars) if var.get()]

            for device in self.devices.values():
                if device.name in who_to_enable:
                    device.enable_password = enable_pass
                    threading.Thread(target=get_info_router,
                                     args=(self.main_gui, self.main_gui.project.devices[device.name],
                                           self.main_gui.project.current_user)).start()

            self.root.destroy()
            return None

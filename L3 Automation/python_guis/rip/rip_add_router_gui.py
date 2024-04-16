import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.routing_protocols.rip.RIPInformation import RIPInformation


class RIPAddRouterGUI:
    def __init__(self, main_gui):
        self.main_gui = main_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' RIP Add router')

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
        devices = main_gui.get_devices()
        ripOptions = []
        for k, router in devices.items():
            if router.rip is None:
                ripOptions.append(router.name)
        if len(ripOptions) == 0:
            messagebox.showerror('Error', 'All routers have RIP configured', parent=root)
            root.destroy()
            return
        lblHostname = tk.Label(root, text='Hostname:')
        lblHostname.grid(row=0, column=0)

        varHostname = tk.StringVar(root)
        optionMenuHostname = tk.OptionMenu(root, varHostname, *ripOptions)
        optionMenuHostname.grid(row=0, column=1)

        lblAutoSummary = tk.Label(root, text='Auto Summary')
        lblAutoSummary.grid(column=0, row=1)
        varAutoSummary = tk.BooleanVar(root)
        chckbtnAutoSummary = tk.Checkbutton(root, variable=varAutoSummary)
        chckbtnAutoSummary.grid(column=1, row=1)

        lblDefaultInformationOriginate = tk.Label(root, text='Default Information Originate')
        lblDefaultInformationOriginate.grid(column=0, row=2)
        varDefaultInformationOriginate = tk.BooleanVar(root)
        chckbtnDefaultInformation = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        chckbtnDefaultInformation.grid(column=1, row=2)

        lblDefaultMetric = tk.Label(root, text='Default Metric')
        lblDefaultMetric.grid(column=0, row=3)
        entryDefaultMetric = tk.Entry(root)
        entryDefaultMetric.grid(column=1, row=3)

        lblDistance = tk.Label(root, text='Distance')
        lblDistance.grid(column=0, row=4)
        entryDistance = tk.Entry(root)
        entryDistance.grid(column=1, row=4)

        lblMaximumPaths = tk.Label(root, text='Maximum Paths')
        lblMaximumPaths.grid(column=0, row=5)
        entryMaximumPaths = tk.Entry(root)
        entryMaximumPaths.grid(column=1, row=5)

        lblVersion = tk.Label(root, text='Version')
        lblVersion.grid(column=0, row=6)
        versionOptions = ['1', '2']
        varVersion = tk.StringVar(root)
        optionMenuVersion = tk.OptionMenu(root, varVersion, *versionOptions)
        optionMenuVersion.grid(column=1, row=6)

        def validate_router() -> bool:
            if not entryDefaultMetric.get().isdigit() or not (0 <= int(entryDefaultMetric.get()) <= 15):
                messagebox.showerror('Error', 'Default metric must be a an integer between 0 and 15', parent=root)
                entryDefaultMetric.delete(0, tk.END)
                return False
            if not entryDistance.get().isdigit() or not (0 <= int(entryDistance.get()) <= 255):
                messagebox.showerror('Error', 'Distance must be a an integer between 0 and 255', parent=root)
                entryDistance.delete(0, tk.END)
                return False
            if not entryMaximumPaths.get().isdigit() or not (1 <= int(entryMaximumPaths.get()) <= 16):
                messagebox.showerror('Error', 'Maximum paths must be a an integer between 1 and 16', parent=root)
                entryMaximumPaths.delete(0, tk.END)
                return False
            if varVersion.get() not in ['1', '2']:
                messagebox.showerror('Error', 'Version must be 1 or 2', parent=root)
                return False
            return True

        def add_router():
            if validate_router():
                router = main_gui.get_router(varHostname.get())
                rip = RIPInformation(auto_summary=varAutoSummary.get(),
                                     default_information_originate=varDefaultInformationOriginate.get(),
                                     default_metric_of_redistributed_routes=int(entryDefaultMetric.get()),
                                     distance=int(entryDistance.get()),
                                     maximum_paths=int(entryMaximumPaths.get()),
                                     version=int(varVersion.get()))
                router.rip = rip

                main_gui.add_router_rip(router)
                messagebox.showinfo('Success', 'Router updated successfully', parent=root)

                root.destroy()

        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_router, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=7, column=1)

        root.mainloop()

import threading
import tkinter as tk
from tkinter import messagebox

from resources.connect_frontend_with_backend.frontend_backend_functions import update_rip
from resources.devices.Router import Router
from python_guis.gui_resources import config
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.user.User import User


class RIPEditGUI:
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
        lblAutoSummary = tk.Label(root, text='Auto Summary')
        lblAutoSummary.grid(column=0, row=0)
        varAutoSummary = tk.BooleanVar(root)
        chckbtnAutoSummary = tk.Checkbutton(root, variable=varAutoSummary)
        if router.rip.auto_summary is True:
            chckbtnAutoSummary.select()
            varAutoSummary.set(True)
        chckbtnAutoSummary.grid(column=1, row=0)

        lblDefaultInformationOriginate = tk.Label(root, text='Default Information Originate')
        lblDefaultInformationOriginate.grid(column=0, row=1)
        varDefaultInformationOriginate = tk.BooleanVar(root)
        chckbtnDefaultInformation = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        if router.rip.default_information_originate is True:
            chckbtnDefaultInformation.select()
            varDefaultInformationOriginate.set(True)
        chckbtnDefaultInformation.grid(column=1, row=1)

        lblDefaultMetric = tk.Label(root, text='Default Metric')
        lblDefaultMetric.grid(column=0, row=2)
        entryDefaultMetric = tk.Entry(root)
        entryDefaultMetric.insert(0, str(router.rip.default_metric_of_redistributed_routes))
        entryDefaultMetric.grid(column=1, row=2)

        lblDistance = tk.Label(root, text='Distance')
        lblDistance.grid(column=0, row=3)
        entryDistance = tk.Entry(root)
        entryDistance.insert(0, str(router.rip.distance))
        entryDistance.grid(column=1, row=3)

        lblMaximumPaths = tk.Label(root, text='Maximum Paths')
        lblMaximumPaths.grid(column=0, row=4)
        entryMaximumPaths = tk.Entry(root)
        entryMaximumPaths.insert(0, str(router.rip.maximum_paths))
        entryMaximumPaths.grid(column=1, row=4)

        lblVersion = tk.Label(root, text='Version')
        lblVersion.grid(column=0, row=5)
        versionOptions = ['1', '2']
        versionVariable = tk.StringVar(root)
        versionVariable.set(str(router.rip.version))
        optionMenuVersion = tk.OptionMenu(root, versionVariable, *versionOptions)
        optionMenuVersion.grid(column=1, row=5)

        def validate_changes():
            if not entryDefaultMetric.get().isdigit() or not (0 <= int(entryDefaultMetric.get()) <= 15):
                messagebox.showerror('Error', 'Default Metric must be an integer between 0 and 15', parent=root)
                entryDefaultMetric.delete(0, tk.END)
                return False
            if not entryDistance.get().isdigit() or not (0 <= int(entryDistance.get()) <= 255):
                messagebox.showerror('Error', 'Distance must be an integer between 0 and 255', parent=root)
                entryDistance.delete(0, tk.END)
                return False
            if not entryMaximumPaths.get().isdigit() or not (1 <= int(entryMaximumPaths.get()) <= 16):
                messagebox.showerror('Error', 'Maximum Paths must be an integer between 1 and 16', parent=root)
                entryMaximumPaths.delete(0, tk.END)
                return False
            return True

        def apply_changes():
            if validate_changes():
                threading.Thread(target=update_rip,
                                 args=(main_gui, router, user, varAutoSummary.get(),
                                       varDefaultInformationOriginate.get(), int(entryDefaultMetric.get()),
                                       int(entryDistance.get()), int(entryMaximumPaths.get()),
                                       int(versionVariable.get()))).start()

                root.destroy()

        btnFrame = tk.Frame(root)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_changes)
        btnApply.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy)
        btnCancel.pack()
        btnFrame.grid(column=0, row=6, columnspan=2)

        root.mainloop()

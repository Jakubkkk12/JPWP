import tkinter as tk
from tkinter import ttk

from python_guis.gui_resources import config
from resources.devices.Router import Router


class InterfaceErrorsGUI:
    def __init__(self, router: Router, int_name: str):
        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' ' + int_name + ' Interfaces Errors')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 600
        height = 150
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(300, 300)

        # Frame containing treeview and scrollbars
        treeFrame = tk.Frame(root)
        treeFrame.configure(bg=config.BG_COLOR)
        treeFrame.pack(fill='both', expand=True)

        verticalScrollbar = ttk.Scrollbar(treeFrame, orient='vertical')
        verticalScrollbar.pack(side='right', fill='y')

        horizontalScrollbar = ttk.Scrollbar(treeFrame, orient='horizontal')
        horizontalScrollbar.pack(side='bottom', fill='x')

        treeColumns = ('input errors',
                       'output errors',
                       'output buffer failures',
                       'runts',
                       'giants',
                       'crc',
                       'frame',
                       'throttles',
                       'overrun',
                       'ignored')
        tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        tree.pack(side='top', expand=True, fill='both')
        tree.configure(yscrollcommand=verticalScrollbar.set)
        tree.configure(xscrollcommand=horizontalScrollbar.set)

        verticalScrollbar.config(command=tree.yview)
        horizontalScrollbar.config(command=tree.xview)

        # Button is a child of root, not treeFrame
        btnQuit = tk.Button(root, text='Quit', command=root.destroy)
        btnQuit.pack(side='bottom')

        # Data insert
        interface = router.interfaces.get(int_name)
        values = (interface.statistics.errors.input_errors,
                  interface.statistics.errors.output_errors,
                  interface.statistics.errors.output_buffer_failures,
                  interface.statistics.errors.runts,
                  interface.statistics.errors.giants,
                  interface.statistics.errors.crc,
                  interface.statistics.errors.frame,
                  interface.statistics.errors.throttles,
                  interface.statistics.errors.overrun,
                  interface.statistics.errors.ignored)
        tree.insert('', tk.END, values=values)

        for heading in treeColumns:
            tree.heading(heading, text=heading, anchor='w')
            tree.column(heading, width=100, stretch=False)

        root.mainloop()

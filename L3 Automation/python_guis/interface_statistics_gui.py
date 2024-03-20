import tkinter as tk
from tkinter import ttk

from gui_resources import config
from resources.devices.Router import Router
from resources.interfaces.InterfaceOSPFInformation import InterfaceOSPFInformation
from resources.interfaces.InterfaceStatistics import InterfaceStatistics, ErrorsStatistics, InformationStatistics
from resources.interfaces.RouterInterface import RouterInterface
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.ospf.OSPFTimers import OSPFTimers
from resources.ssh.SSHInformation import SSHInformation


class InterfaceStatisticsGUI:
    def __init__(self, router: Router, int_name: str):
        interface = router.interfaces.get(int_name)

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' ' + interface.name + ' Interfaces Details')

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

        treeColumns = ('collision',
                       'late collision',
                       'broadcast',
                       'packets input',
                       'packets output',
                       'duplex',
                       'speed',
                       'layer 1 status',
                       'layer 2 status',
                       'mtu',
                       'encapsulation')
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

        values = (interface.statistics.information.collision,
                  interface.statistics.information.late_collision,
                  interface.statistics.information.broadcast,
                  interface.statistics.information.packets_input,
                  interface.statistics.information.packets_output,
                  interface.statistics.information.duplex,
                  interface.statistics.information.speed,
                  interface.statistics.information.layer1_status,
                  interface.statistics.information.layer2_status,
                  interface.statistics.information.mtu,
                  interface.statistics.information.encapsulation)
        tree.insert('', tk.END, values=values)

        for heading in treeColumns:
            tree.heading(heading, text=heading, anchor='w')
            tree.column(heading, width=100)

        root.mainloop()

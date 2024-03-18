import tkinter as tk
import tkinter.ttk
from gui_resources import config
from PIL import Image, ImageTk
from resources.devices import Router

APPNAME = config.APPNAME
VERSION = config.VERSION
BG_COLOR = config.BG_COLOR
WINDOW_ICON_PATH = 'gui_resources/APP_ICON_512.png'
QUIT_ICON_PATH = 'gui_resources/QUIT_512.png'


class InterfacesDetails:
    def __init__(self, hostname):

        root = tk.Tk()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(APPNAME + ' ' + VERSION + ' Interfaces Details')

        # size parameters
        width = 300
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(300, 300)

        tree = tk.ttk.Treeview(root)
        tree.pack(expand=True, fill='both')

        verticalScrollbar = tk.Scrollbar(root, orient='vertical')
        verticalScrollbar.pack(side='right', fill='y', expand=False)
        horizontalScrollbar = tk.Scrollbar(root, orient='horizontal')
        horizontalScrollbar.pack(side='bottom', fill='x', expand=False)

        QUIT_ICON = Image.open(QUIT_ICON_PATH)
        QUIT_ICON = QUIT_ICON.resize((24, 24))
        quit_icon = ImageTk.PhotoImage(QUIT_ICON)
        btnQuit = tk.Button(root, text='Quit')
        btnQuit.pack(side='bottom')




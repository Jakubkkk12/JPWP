import tkinter as tk
import tkinter.messagebox
from python_guis.gui_resources import config

WINDOW_ICON_PATH = config.WINDOW_ICON_PATH
BG_COLOR = config.BG_COLOR


class EnablePasswordGUI:
    def __init__(self):
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

        self.root.configure(bg=BG_COLOR)

        lblEnterEnable = tk.Label(self.root, text='Enter Enable Password')
        lblEnterEnable.place(x=80, y=30, width=140, height=30)
        lblEnterEnable.configure(bg=BG_COLOR)

        self.entryEnablePassword = tk.Entry(self.root, show='*')
        self.entryEnablePassword.place(x=80, y=60, width=140, height=30)

        lblConfirmEnable = tk.Label(self.root, text='Confirm Enable Password')
        lblConfirmEnable.place(x=80, y=90, width=140, height=30)
        lblConfirmEnable.configure(bg=BG_COLOR)

        self.entryConfirmEnable = tk.Entry(self.root, show='*')
        self.entryConfirmEnable.place(x=80, y=120, width=140, height=30)

        btnApply = tk.Button(self.root, text='Apply', command=self.validate)
        btnApply.place(x=100, y=160, width=100, height=30)

        btnQuit = tk.Button(self.root, text='Cancel', command=self.root.destroy)
        btnQuit.place(x=100, y=200, width=100, height=30)

        self.root.mainloop()

    def validate(self) -> None:
        ssh_pass = self.entryEnablePassword.get()
        ssh_confirm_pass = self.entryConfirmEnable.get()

        if ssh_pass != ssh_confirm_pass:
            self.entryEnablePassword.delete(0, 'end')
            self.entryConfirmEnable.delete(0, 'end')
            tk.messagebox.showerror(title='Wrong credentials', message='Passwords must be the same.', parent=self.root)

        else:
            # router.sshpass = ssh_pass
            self.root.destroy()
            return None


if __name__ == '__main__':
    EnablePasswordGUI()
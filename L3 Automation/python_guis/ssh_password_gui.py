import tkinter as tk
import tkinter.messagebox
from gui_resources import config

WINDOW_ICON_PATH = 'gui_resources/APP_ICON_512.png'
BG_COLOR = config.BG_COLOR


class SSHPasswordGUI:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title('SSH Password')

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

        lblEnterSSH = tk.Label(self.root, text='Enter SSH Password')
        lblEnterSSH.place(x=80, y=30, width=140, height=30)
        lblEnterSSH.configure(bg=BG_COLOR)

        self.entrySSHPassword = tk.Entry(self.root, show='*')
        self.entrySSHPassword.place(x=80, y=60, width=140, height=30)

        lblConfirmSSH = tk.Label(self.root, text='Confirm SSH Password')
        lblConfirmSSH.place(x=80, y=90, width=140, height=30)
        lblConfirmSSH.configure(bg=BG_COLOR)

        self.entryConfirmSSH = tk.Entry(self.root, show='*')
        self.entryConfirmSSH.place(x=80, y=120, width=140, height=30)

        btnApply = tk.Button(self.root, text='Apply', command=self.validate_ssh)
        btnApply.place(x=100, y=160, width=100, height=30)

        btnQuit = tk.Button(self.root, text='Cancel', command=self.root.destroy)
        btnQuit.place(x=100, y=200, width=100, height=30)

        self.root.mainloop()

    def validate_ssh(self) -> None:
        ssh_pass = self.entrySSHPassword.get()
        ssh_confirm_pass = self.entryConfirmSSH.get()

        if ssh_pass != ssh_confirm_pass:
            self.entrySSHPassword.delete(0, 'end')
            self.entryConfirmSSH.delete(0, 'end')
            tk.messagebox.showerror(title='Wrong credentials', message='Passwords must be the same.', parent=self.root)

        else:
            # router.sshpass = ssh_pass
            self.root.destroy()
            return None


# if __name__ == '__main__':
#     SSHPasswordGUI()

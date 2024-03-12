import tkinter as tk
import tkinter.messagebox

WINDOW_ICON_PATH = 'resources/APP_ICON_512.png'


class SSHPasswordGUI:
    def __init__(self):
        root = tk.Toplevel()
        root.title('SSH Password')

        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        width = 300
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        root.configure(bg='grey')

        lblEnterSSH = tk.Label(root, text='Enter SSH Password')
        lblEnterSSH.place(x=80, y=30, width=140, height=30)
        lblEnterSSH.configure(bg='grey')

        self.entrySSHPassword = tk.Entry(root, show='*')
        self.entrySSHPassword.place(x=80, y=60, width=140, height=30)

        lblConfirmSSH = tk.Label(root, text='Confirm SSH Password')
        lblConfirmSSH.place(x=80, y=90, width=140, height=30)
        lblConfirmSSH.configure(bg='grey')

        self.entryConfirmSSH = tk.Entry(root, show='*')
        self.entryConfirmSSH.place(x=80, y=120, width=140, height=30)

        btnApply = tk.Button(root, text='Apply', command=self.validate_ssh)
        btnApply.place(x=100, y=160, width=100, height=30)

        btnQuit = tk.Button(root, text='Cancel', command=root.destroy)
        btnQuit.place(x=100, y=200, width=100, height=30)

        root.mainloop()

    def validate_ssh(self):
        ssh_pass = self.entrySSHPassword.get()
        ssh_confirm_pass = self.entryConfirmSSH.get()
        if ssh_pass != ssh_confirm_pass:
            self.entrySSHPassword.delete(0, 'end')
            self.entryConfirmSSH.delete(0, 'end')
            tk.messagebox.showerror(title='Wrong credentials',
                                         message='Passwords must be the same.')
        else:
            # router.sshpass = ssh_pass
            return


# if __name__ == '__main__':
#     SSHPasswordGUI()

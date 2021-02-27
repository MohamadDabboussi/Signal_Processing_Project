from tkinter import *
root = Tk()


def B1Click():
    L2 = Label(root, text="L2", width="15", height="10")
    L2.grid(row=0, column=1)


L1 = Label(root, text="L1", width=15, height=10)
L1.grid(row=0, column=0)
B1 = Button(root, text="B1", padx=20, pady=10, command=B1Click)
B1.grid(row=3, column=2)
E1 = Entry(root, width=20)
E1.grid(row=1, column=2)

root.mainloop()

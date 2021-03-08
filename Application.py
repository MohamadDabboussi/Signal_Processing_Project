from tkinter import *
from ttk import *

root = Tk()
root.geometry("400x40")
root.configure(background='green')
root.tk_setPalette('black')

name = Entry(root, width=50)
e.pack()
e.insert(0, "Enter the filter name:")


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


##################################

root.title('Projet traitement numerique')
root.iconbitmap(path.ico)

# make multiple window
frame1
frame2
frame3
frame4

frames_list = []

status = Label(root, text="step 1 of " + str(len(frames_list)),
               bd=1, relief=SUNKEN, anchor=E)

myLabel = Label(image=my_img)
myLabel.grid(row=0, column=0, columnspan=3)


def forward(frame_number):
    global frame
    global button_forward
    global button_back

    my_Label.grid_forget()
    my_Label = Label(image=frames_list[frame_number-1])
    button_forward = Button(root, text="next", command=Lambda: forward(frame_number+1))
    button_back = Button(root, text="back", command=Lambda: forward(frame_number-1))

    if(frame_number == 5):
        button_forward = Button(root, text="next", state=DISABLED)
    myLabel.grid(row=0, column=0, columnspan=3)
    button_back = Button(root, text="back", command=back)
    button_forward.grid(row=1, column=2)
    status = Label(root, text="step "+str(frame_number)+" of " + str(len(frames_list)),
                   bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)


def back(frame_number):
    global frame
    global button_forward
    global button_back
    my_Label = Label(image=frames_list[frame_number-1])
    button_forward = Button(root, text="next", command=Lambda: forward(frame_number+1))
    button_back = Button(root, text="back", command=Lambda: forward(frame_number-1))

    if(frame_number == 0):
        button_back = Button(root, text="back", state=DISABLED)

    myLabel.grid(row=0, column=0, columnspan=3)
    button_back = Button(root, text="back", command=back)
    button_forward.grid(row=1, column=2)
    status = Label(root, text="step "+str(frame_number)+" of " + str(len(frames_list)),
                   bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)


button_back = Button(root, text="back", command=back, state=DISABLED)
button_exit = Button(root, text="Exit", command=root.quit)
button_forward = Button(root, text="next", command=Lambda: forward(2))

button_back.grid(row=1, column=0)
button_exit.grid(row=1, columm=1)
button_forward.grid(row=1, column=2, pady=10)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)
######################################

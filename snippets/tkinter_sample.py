from tkinter import *

def printData(firstName, lastName):
    print(firstName)
    print(lastName)
    root.destroy()

def get_input():

    firstName = entry1.get()
    lastName = entry2.get()
    printData(firstName, lastName)


root = Tk()
#Label 1
label1 = Label(root,text = 'First Name')
label1.pack()
label1.config(justify = CENTER)

entry1 = Entry(root, width = 30)
entry1.pack()

label3 = Label(root, text="Last Name")
label3.pack()
label1.config(justify = CENTER)

entry2 = Entry(root, width = 30)
entry2.pack()

button1 = Button(root, text = 'submit')
button1.pack()
button1.config(command = get_input)

root.mainloop()



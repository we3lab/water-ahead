from tkinter import *


def callback():
    print("Called the callback!")


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("Hi there, everyone!")


root = Tk()

# Create the menu.
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=callback)

# # Create a toolbar.
# toolbar = Frame(root)
#
# b = Button(toolbar, text="New", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)
#
# b = Button(toolbar, text="Open", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)
#
# toolbar.pack(side=TOP, fill=X)

# Define a Status Bar class.


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

status = StatusBar(root)
status.pack(side=BOTTOM, fill=X)

app = App(root)



root.mainloop()

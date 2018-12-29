from tkinter import *
from tkinter import ttk
import tkinter.simpledialog
import tkinter.messagebox
import os

def menu_option_selected():
    print('Called the callback!')

class Notebook(Frame):
    """Notebook Widget"""

    def __init__(self, parent, activerelief=RAISED, inactiverelief=RIDGE, xpad=4, ypad=6, activefg='black',
                 inactivefg='black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)

        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
        # Make various argument available to the rest of the class
        self.activefg = activefg
        self.inactivefg = inactivefg
        self.deletedTabs = []
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief
        self.kwargs = kw
        self.tabVars = {}  # This dictionary holds the label and frame instances of each tab
        self.tabs = 0  # Keep track of the number of tabs
        self.noteBookFrame = Frame(parent)  # Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)  # Create a frame to put the "tabs" in
        self.noteBook = Frame(self.noteBookFrame, relief=RAISED, bd=2,
                              **kw)  # Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)  # self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row=0, sticky=W)
        self.noteBook.grid(row=1, column=0, columnspan=27)

    def change_tab(self, IDNum):
        """Internal Function"""

        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if i not in self.deletedTabs:  # Make sure tab hasn't been deleted
                if i != IDNum:  # Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()  # Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0][
                        'relief'] = self.inactiverelief  # Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0][
                        'fg'] = self.inactivefg  # Set the fg of the tab, showing it is selected, default is black
                else:  # When on the tab that is currently selected...
                    self.tabVars[i][1].grid()  # Re-grid the frame that corresponds to the tab
                    self.tabVars[IDNum][0][
                        'relief'] = self.activerelief  # Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0][
                        'fg'] = self.activefg  # Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width=2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """

        temp = self.tabs  # Temp is used so that the value of self.tabs will not throw off the argument sent by the label's event binding
        self.tabVars[self.tabs] = [Label(self.BFrame, relief=RIDGE, **kw)]  # Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event: self.change_tab(temp))  # Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side=LEFT, ipady=self.ypad,
                                        ipadx=self.xpad)  # Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(
            Frame(self.noteBook, **self.kwargs))  # Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row=0, column=0)  # Grid the frame ontop of any other already existing frames
        self.change_tab(0)  # Set focus to the first tab
        self.tabs += 1  # Update the tab count
        return self.tabVars[temp][1]  # Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                b[0].destroy()  # Destroy the tab's frame, along with all child widgets
                self.tabs -= 1  # Subtract one from the tab count
                self.deletedTabs.append(
                    self.iteratedTabs)  # Apend the NumID of the given tab to the list of deleted tabs
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count

    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                self.change_tab(
                    self.iteratedTabs)  # send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count


def demo():
    def adjustCanvas(someVariable=None):
        fontLabel["font"] = ("arial", var.get())

    root = Tk()

    # Create the menu.
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=menu_option_selected)
    filemenu.add_command(label="Open", command=menu_option_selected)
    filemenu.add_command(label="Save", command=menu_option_selected)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=menu_option_selected)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=menu_option_selected)

    root.title("Water AHEAD")
    note = Notebook(root, width=530, height=400, activefg='black', inactivefg='gray')  # Create a Note book Instance
    note.grid()
    tab1 = note.add_tab(text='General Properties')  # Create an overview tab.
    tab2 = note.add_tab(text='Geography')  # Create a tab to ask about the system geography (i.e., where is it located  or will you be using nationwide averages?)
    tab3 = note.add_tab(text='Baseline Treatment Process')  # Create a tab with the text "Tab Three"
    tab4 = note.add_tab(text='New Treatment Process')  # Create a tab with the text "Tab Four"
    tab5 = note.add_tab(text='Results')  # Create a tab with the text "Tab Five"
    Label(tab1, text='System Parameters',font=('Arial', 10, 'bold')).grid(row=0, column=1)  # Use each created tab as a parent, etc etc...
    Label(tab1, text='System Type:', font=('Arial', 10)).grid(row=1, column=0, sticky=E)
    Label(tab1, text='System Size:', font=('Arial', 10)).grid(row=2, column=0, sticky=E)

    system_type = StringVar(root)
    system_type_choices = ['Drinking Water System', 'Municipal Wastewater System', 'Industrial Wastewater System']
    system_type.set('Drinking Water System')
    system_type_popup_menu = OptionMenu(tab1, system_type, *system_type_choices).grid(row=1, column=1)

    def change_dropdown(*args):
        selected_system_type = system_type.get()
        print(selected_system_type)

    system_type.trace('w', change_dropdown)

    def callback(P):
        # if P in ['0', '1', '2', '3,' '4', '5', '6', '7', '8', '9', '.']:
        if str.isalpha(P):
        # if str.isfloat(P) or P == '' or P == '.':
            return False
        else:
            return True

    vcmd = (tab1.register(callback))

    system_size_input = Entry(tab1, validate='all', validatecommand=(vcmd, '%P')).grid(row=2, column=1)
    print(system_size_input)
    Label(tab1, text=f'm\N{SUPERSCRIPT THREE}/d', font=('Arial', 10)).grid(row=2, column=2, sticky=W)

    Label(tab1, text='Economic Parameters', font=('Arial', 10, 'bold')).grid(row=3, column=1)

    Label(tab1, text='Year for Inflation Adjustment:', font=('Arial', 10)).grid(row=4, column=0, sticky=E)
    year_for_inflation = StringVar(root)
    year_for_inflation_choices = range(2000, 2019)
    year_for_inflation.set(2015)
    year_for_inflation_popup_menu = OptionMenu(tab1, year_for_inflation, *year_for_inflation_choices).grid(row=4, column=1)

    Label(tab1, text='Value of a Statistical Life:', font=('Arial', 10)).grid(row=5, column=0, sticky=E)
    vsl = DoubleVar(root)
    vsl.set(8.6)
    scale = Scale(tab1, from_=0.1, to=20, resolution=0.1, font=('Arial', 10), orient='horizontal', variable=vsl).grid(row=5, column=1)
    Label(tab1, text='$M (in $2015USD)', font=('Arial', 10)).grid(row=5, column=2, sticky=W)

    Label(tab1, text='Social Cost of Carbon:', font=('Arial', 10)).grid(row=6, column=0, sticky=E)
    scc = IntVar(root)
    scc.set(40)
    scale = Scale(tab1, from_=0, to=250, font=('Arial', 10), orient='horizontal', variable=scc).grid(row=6, column=1)
    Label(tab1, text=f'$/short ton CO\N{SUBSCRIPT TWO} (in $2015 USD)', font=('Arial', 10)).grid(row=6, column=2, sticky=W)

    Label(tab2,
          text='Electricity Generation and Chemical Manufacturing Geography',
          font=("Arial", 10, 'bold')).grid(row=0, column=0, columnspan=2)

    Label(tab2, text='Grid State:', font=('Arial', 10)).grid(row=1, column=0, sticky=E)
    grid_state = StringVar(root)
    grid_state_choices = ['US Average', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA',
                          'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                          'VA', 'WA', 'WV', 'WI', 'WY']
    grid_state.set('US Average')
    grid_state_popup_menu = OptionMenu(tab2, grid_state, *grid_state_choices).grid(row=1, column=1, sticky=W)

    Label(tab2, text='Chemical Manufacturing State:', font=('Arial', 10)).grid(row=2, column=0, sticky=E)
    chem_state = StringVar(root)
    chem_state_choices = ['US Average', 'Off-Shore', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL',
                          'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                          'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                          'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    chem_state.set('US Average')
    chem_state_popup_menu = OptionMenu(tab2, chem_state, *chem_state_choices).grid(row=2, column=1, sticky=W)

    Button(tab3, text='Destroy Tab Four!', command=lambda: note.destroy_tab(tab4)).grid()
    Label(tab3,
          text="Destroying a tab will remove it,\nand competely destoy all child widgets.\nOnce you destroy a tab, you have to recreate it\ncompletely in order to get it back.",
          font=("Comic Sans MS", 12, "italic")).grid()
    Label(tab4, text='Tab 4').grid()
    Button(tab5, text='Tab One', command=lambda: note.focus_on(tab1)).grid(pady=3)
    Button(tab5, text='EXIT', width=23, command=root.destroy).grid()
    note.focus_on(tab1)
    root.mainloop()

if __name__ == "__main__":
    demo()

# class App:
#
#     def __init__(self, master):
#
#         frame = Frame(master)
#         frame.pack()
#
#         self.button = Button(
#             frame, text="QUIT", fg="red", command=frame.quit
#             )
#         self.button.pack(side=LEFT)
#
#         self.hi_there = Button(frame, text="Hello", command=self.say_hi)
#         self.hi_there.pack(side=LEFT)
#
#     def say_hi(self):
#         print("Hi there, everyone!")

# class MyDialog:
#
#     def __init__(self, parent):
#
#         top = self.top = Toplevel(parent)
#
#         Label(top, text='Value').pack()
#
#         self.e = Entry(top)
#         self.e.pack(padx=5)
#
#         b = Button(top, text='OK', command=self.ok)
#         b.pack(pady=5)
#
#     def ok(self):
#
#         print("Value is", self.e.get())
#
#         self.top.destroy()
#
#
# class Dialog(Toplevel):
#
#     def __init__(self, parent, title=None):
#
#         Toplevel.__init__(self, parent)
#         self.transient(parent)
#
#         if title:
#             self.title(title)
#
#         self.parent = parent
#
#         self.result = None
#         body = Frame(self)
#         self.initial_focus = self.body(body)
#         body.pack(padx=5, pady=5)
#
#         self.buttonbox()
#
#         self.grab_set()
#
#         if not self.initial_focus:
#             self.initial_focus = self
#
#         self.protocol('WM_DELETE_WINDOW', self.cancel)
#
#         self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
#                                   parent.winfo_rooty() + 50))
#
#         self.initial_focus.focus_set()
#
#         self.wait_window(self)
#
#     # construction hooks
#
#     def body(self,master):
#         # Create dialog body.  Return widget that should have initial focus.  This method should be overriden.
#         pass
#
#     def buttonbox(self):
#         # Add standard button box.  Override if you don't want the standard buttons.
#
#         box = Frame(self)
#
#         w = Button(box, text='OK', width=10, command=self.ok, default=ACTIVE)
#         w.pack(side=LEFT, padx=5, pady=5)
#         w = Button(box, text='Cancel', width=10, command=self.cancel)
#         w.pack(side=LEFT, padx=5, pady=5)
#
#         self.bind('<Return>', self.ok)
#         self.bind('<Escape>', self.cancel)
#
#         box.pack()
#
#     # standard button semantics
#
#     def ok(self, event=None):
#
#         if not self.validate():
#             self.initial_focus.focus_set()
#             return
#
#         self.withdraw()
#         self.update_idletasks()
#
#         self.apply()
#
#         self.cancel()
#
#     def cancel(self, event=None):
#
#         # Put focus back to the parent window.
#         self.parent.focus_set()
#         self.destroy()
#
#     # command hooks
#
#     def validate(self):
#
#         return 1 #override
#
#     def apply(self):
#
#         pass #override
#
#
# class MyDialog(tkinter.simpledialog.Dialog):
#
#     def body(self, master):
#
#         Label(master, text='Number 1:').grid(row=0, sticky=W)
#         Label(master, text='Number 2:').grid(row=1, sticky=W)
#
#         self.e1 = Entry(master)
#         self.e2 = Entry(master)
#
#         self.e1.grid(row=0, column=1)
#         self.e2.grid(row=1, column=1)
#
#         self.cb = Checkbutton(master, text='Hardcopy')
#         self.cb.grid(row=2, columnspan=2, sticky=W)
#
#         return self.e1  # initial focus
#
#     def validate(self):
#         try:
#             first = int(self.e1.get())
#             second = int(self.e2.get())
#             result = first + second
#             self.result_string = f'The sum of your numbers is {result}.'
#             return 1
#         except ValueError:
#             tkinter.messagebox.showwarning(
#                 'Bad input',
#                 'Illegal values, please try again'
#             )
#             return 0
#
#     def apply(self):
#         tkinter.messagebox.showinfo(
#             'Result',
#             self.result_string
#         )
#
#         return
#
# root = Tk()
#
# d = MyDialog(root)
# #print(d.result_string)
#
# # root.wait_window(d.top)
#
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
#
#
# class StatusBar(Frame):
#
#     def __init__(self, master):
#         Frame.__init__(self, master)
#         self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
#         self.label.pack(fill=X)
#
#     def set(self, format, *args):
#         self.label.config(text=format % args)
#         self.label.update_idletasks()
#
#     def clear(self):
#         self.label.config(text="")
#         self.label.update_idletasks()
#
# status = StatusBar(root)
# status.pack(side=BOTTOM, fill=X)
#
# app = App(root)
#
#
#
# root.mainloop()

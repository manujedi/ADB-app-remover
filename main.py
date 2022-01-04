import os
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

def listapps():
    stream = os.popen('adb shell pm list packages')
    output = stream.read()
    applist = []
    for line in output.splitlines():
        applist.append(line[8:])
    applist.sort()
    return applist


# Create the root window
root = Tk()
root.title('App Uninstaller')
root.geometry('1000x800')
filterstring = ""
 
listbox = Listbox(root, selectmode=EXTENDED)
 
def fillBox(applist):
    global filterstring
    listbox.delete(0,END)
    newList = [s for s in applist if filterstring in s]
    for item in newList:
        listbox.insert(END, item)

fillBox(listapps())


#buttons
def update():
    global filterstring
    filterstring = ""
    vw = listbox.yview()
    fillBox(listapps())
    listbox.yview_moveto(vw[0])

def remApp():
    for i in listbox.curselection():
        app = listbox.get(i)
        print("removing " + app + "...")
        val = os.system('adb shell pm uninstall -k --user 0 ' + app)
    fillBox(listapps())

def filter():
    global filterstring 
    filterstring = simpledialog.askstring(title="Search", prompt="Input a substring to search for")
    fillBox(listapps())
 
btn1 = Button(root, text='Remove', command=remApp)
btn2 = Button(root, text='Update', command=update)
btn3 = Button(root, text='Filter', command=filter)

listbox.pack(fill='both', expand=True)
btn1.pack(ipadx=10,ipady=10, expand=True, fill='both', side='left')
btn2.pack(ipadx=10,ipady=10, expand=True, fill='both',side='left')
btn3.pack(ipadx=10,ipady=10, expand=True, fill='both',side='left')
 
root.mainloop()
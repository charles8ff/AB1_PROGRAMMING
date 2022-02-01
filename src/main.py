import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from ttkbootstrap.constants import *
import os.path
import sqlite3
import ttkbootstrap as ttkth
from turtle import heading
import datetime

#-------- Functions for the DataBase
#---- Creates the DataBase
def myDB():
    if not os.path.exists("prizes"):
        varConnect=sqlite3.connect('./prizes')
        varCursor=varConnect.cursor()
        varCursor.execute("""
            CREATE TABLE prizes(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(20),
                DATE DATE,
                AMOUNT INT(30)
                )
            """)
        messagebox.showinfo("DB","DataBase built successfully")
    else:
        messagebox.showwarning("Warning!","DB already exists")

#---- Shows a window with the DataBase  
def showDB():
    varConnect=sqlite3.connect("prizes")
    varCursor=varConnect.cursor()
    varCursor.execute("SELECT * FROM prizes")
    prizes=varCursor.fetchall()
    varCursor.close()
    varConnect.close()
    
    NewWindow = Toplevel(root)
    list=ttk.Treeview(NewWindow, columns=("1","2","3","4"),padding=(10))
    list.heading("1", text="ID")
    list.heading("2", text="Name")
    list.heading("3", text="Date")
    list.heading("4", text="Amount")
    list.column("#0", stretch=NO, minwidth=0, width=0)
    list.column("1", anchor="center") # The following 4 lines center the items in the columns
    list.column("2", anchor="center")
    list.column("3", anchor="center")
    list.column("4", anchor="center")
    for prize in prizes:
        list.insert('', 'end', values=prize) # Inserts each element of the database into the window
    list.pack()
    Button(NewWindow, text="Ok", command=NewWindow.destroy).pack()
    
#---- Correctly closes the app
def exitApp():
    if messagebox.askquestion("Exit","Do you want to exit the app?")=="yes":
        root.destroy()
        
#---- Clear input fields
def clearFields():
    targetID.set("")
    targetName.set("")
    targetDate.set("")
    targetAmount.set("")  

#---- Open the licence of this program
def openLicencse():
    webbrowser.open_new("https://github.com/charles8ff/AB1_PROGRAMMING/blob/main/LICENSE")

#---- Checks the data and creates a new entry into the Database
def create():
    isAnAmount=targetAmount.get()
    splitDate=targetDate.get()
    isADate=True # Variable used to check, will be marked false if the following code does not succeed
    
    try:
        day, month, year = splitDate.split('-') # Date format is DD-MM-YYYY
    except ValueError:
        isADate = False
        
    if isADate:
        try:
            datetime.datetime(int(year), int(month), int(day)) # Checks for a valid date
        except ValueError:
            isADate = False
    else:
        pass
    
    myTuple=()
    if isAnAmount.isnumeric() and isADate is True: # Checks for the date and for the amount to be valid
        myTuple=(targetName.get(),
                 targetDate.get(),
                 targetAmount.get()
                )
        myConnect=sqlite3.connect("prizes")
        myCursor=myConnect.cursor()
        myCursor.execute("""INSERT INTO prizes
                VALUES(NULL,?,?,? )""", myTuple) # Inserts into DB
        myConnect.commit()
        messagebox.showinfo("DB", "Successfully inserted data.")
    else:
        messagebox.showwarning("DB", "Incorrect data.")

#---- Reads an entry selected by ID    
def read():
    if targetID.get().isalpha():
        messagebox.showwarning("DB", "Incorrect ID format.")
    else:
        myConnect=sqlite3.connect("prizes")
        myCursor=myConnect.cursor()
        myCursor.execute("SELECT * FROM prizes WHERE ID="+targetID.get())

        targetPlayer=myCursor.fetchall()
        if targetPlayer == []:
            messagebox.showwarning("DB", "This entry does not exist")
        else:
            targetID.set(targetPlayer[0][0])
            targetName.set(targetPlayer[0][1])
            targetDate.set(targetPlayer[0][2])  
            targetAmount.set(targetPlayer[0][3])    

        myConnect.commit()

#---- Deletes the selected entry from the Database
def deleteEntries():
    if targetID.get().isdigit():
        myConnect=sqlite3.connect("prizes")
        myCursor=myConnect.cursor()
        myCursor.execute("SELECT * FROM prizes WHERE ID="+targetID.get())

        targetPlayer=myCursor.fetchall()
        if targetPlayer != []: # checks if the entry exists
            targetID.set(targetPlayer[0][0])
            myCursor.execute("""DELETE FROM prizes WHERE ID=?""", targetID.get())
            myConnect.commit()
            myCursor.close()
            myConnect.close()
            messagebox.showinfo("DB", "Successfully deleted entry")
        else:
            messagebox.showwarning("DB", "This entry does not exist")
    else:
        messagebox.showwarning("DB", "Please select an ID")
    
#-------- Window functions
#---- General settings
root = ttkth.Window(themename="solar") # adds theme
root.resizable(False, False)
topMenu=Menu(root)
root.config(menu=topMenu,width=500, height=500,padx=10,pady=20)

#---- Top Menu Content
dbMenu = Menu(topMenu, tearoff=0)
dbMenu.add_command(label="Create DB", command=myDB)
dbMenu.add_command(label="Connect DB", command=showDB)
dbMenu.add_command(label="Exit", command=exitApp) 

deleteMenu = Menu(topMenu, tearoff=0)
deleteMenu.add_command(label="Clear fields", command=clearFields)

helpMenu = Menu(topMenu, tearoff=0)
helpMenu.add_command(label="License", command=openLicencse)

#---- Top Menu Buttons                                 
topMenu.add_cascade(label= "DB", menu=dbMenu)
topMenu.add_cascade(label= "Clear fields", menu=deleteMenu)
topMenu.add_cascade(label= "Help", menu=helpMenu)

#---- Fields to add entries
upperFrame =Frame(root)
upperFrame.pack()

targetID=StringVar()
targetName=StringVar()
targetDate=StringVar()
targetAmount=StringVar()

myFrameID =Entry(upperFrame, textvariable=targetID)
myFrameID.grid(row=0, column=1, padx=10, pady= 10)

myFrameName =Entry(upperFrame, textvariable=targetName)
myFrameName.grid(row=1, column=1, padx=10, pady= 10)

myFrameAmount =Entry(upperFrame, textvariable=targetDate)
myFrameAmount.grid(row=2, column=1, padx=10, pady= 10)

myFrameAmount =Entry(upperFrame, textvariable=targetAmount)
myFrameAmount.grid(row=3, column=1, padx=10, pady= 10)

#---- Labels to the inputs

labelID=Label(upperFrame, text="Id:")
labelID.grid(row=0, column=0, sticky="e", padx=10, pady=10)

labelName=Label(upperFrame, text="Name of prize:")
labelName.grid(row=1, column=0, sticky="e", padx=10, pady=10)

labelDate=Label(upperFrame, text="Date:")
labelDate.grid(row=2, column=0, sticky="e", padx=10, pady=10)

labelAmount=Label(upperFrame, text="Amount:")
labelAmount.grid(row=3, column=0, sticky="e", padx=10, pady=10)

#--- Lower Menu

lowerFrame=Frame(root)
lowerFrame.pack()

createButton=Button(lowerFrame, text="Add prize", command=create)
createButton.grid(row=1, column=0, sticky="e", padx=10, pady=10)

readButton=Button(lowerFrame, text="Read entry", command=read)
readButton.grid(row=1, column=1, sticky="e", padx=10, pady=10)

deleteButton=Button(lowerFrame, text="Delete entry", command=deleteEntries)
deleteButton.grid(row=1, column=3, sticky="e", padx=10, pady=10)

#--- Main Loop of events
root.mainloop()
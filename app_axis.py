#import inspect
#import json
#import sys
import tracemalloc
#from datetime import datetime
from tkinter import *

#from docutils.nodes import label
#from numpy.matrixlib.defmatrix import matrix
import bCAPClient.bcapclient as bcapclient

#from scipy.stats import randint
#from sympy import false

from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
def print_error(message:str):
    showerror("Error", message)
    raise Exception(message)

class App(Tk):
    def __init__(self):
        super().__init__()
        self.configure(background='white')

        self.j1 = DoubleVar(value= 380.0)
        self.j2 = DoubleVar(value= -12.04)
        self.j3 = DoubleVar(value= 200.36)
        self.j4 = DoubleVar(value= 173.86)
        self.j5 = DoubleVar(value= -0.30)
        self.j6 = DoubleVar(value= 111.72)
    
        self.title("PF4EA")
        self.geometry("1000x1200")
        self.page = Page1(self)

    def move(self):

        ### set IP Address , Port number and Timeout of connected RC8
        host = "192.168.0.1"
        port = 5007
        timeout = 2000

        ### Connection processing of tcp communication
        m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
        print("Open Connection")

        ### start b_cap Service
        m_bcapclient.service_start("")
        print("Send SERVICE_START packet")

        ### set Parameter
        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")

        ### Connect to RC8 (RC8(VRC)provider)
        hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
        print("Connect RC8")
        ### get Robot Object Handl
        HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
        print("AddRobot")

        ### TakeArm
        Command = "TakeArm"
        Param = [0,0]
        m_bcapclient.robot_execute(HRobot,Command,Param)
        print("TakeArm")

        ### Set Parameters
        #Interpolation
        Comp=1

        try:        
            Pose ="@P P("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
            m_bcapclient.robot_move(HRobot,Comp,Pose,"")
            print("Complete Move P,@P P[1]")
        except:
            print("no buono")



        ###Give Arm
        Command = "GiveArm"
        Param = None
        m_bcapclient.robot_execute(HRobot,Command,Param)
        print("GiveArm")

        #Disconnect
        if(HRobot != 0):
            m_bcapclient.robot_release(HRobot)
            print("Release Robot Object")
        #End If
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Release Controller")
        #End If
        m_bcapclient.service_stop()
        print("B-CAP service Stop")


  

class Page1(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(pady=5)

        
        self.label_j1 = Label(self, text='X', font=('calibre', 10, 'bold'))
        self.entry_j1 = Entry(self, textvariable=parent.j1, font=('calibre', 10, 'normal'))
        
        self.label_j2 = Label(self, text='Y', font=('calibre', 10, 'bold'))
        self.entry_j2 = Entry(self, textvariable=parent.j2, font=('calibre', 10, 'normal'))
        
        self.label_j3 = Label(self, text='Z', font=('calibre', 10, 'bold'))
        self.entry_j3 = Entry(self, textvariable=parent.j3, font=('calibre', 10, 'normal'))
        
        self.label_j4 = Label(self, text='Rx', font=('calibre', 10, 'bold'))
        self.entry_j4 = Entry(self, textvariable=parent.j4, font=('calibre', 10, 'normal'))
          
        self.label_j5 = Label(self, text='Ry', font=('calibre', 10, 'bold'))
        self.entry_j5 = Entry(self, textvariable=parent.j5, font=('calibre', 10, 'normal'))
        
        self.label_j6 = Label(self, text='Rz', font=('calibre', 10, 'bold'))
        self.entry_j6 = Entry(self, textvariable=parent.j6, font=('calibre', 10, 'normal'))

        self.label_j1.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_j1.grid(row=0, column=1,sticky='w', padx=5, pady=5)

        self.label_j2.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_j2.grid(row=1, column=1,sticky='w', padx=5, pady=5)       
        
        self.label_j3.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_j3.grid(row=2, column=1,sticky='w', padx=5, pady=5)       
        
        self.label_j4.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.entry_j4.grid(row=3, column=1,sticky='w', padx=5, pady=5)        
        
        self.label_j5.grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.entry_j5.grid(row=4, column=1,sticky='w', padx=5, pady=5)        
        
        self.label_j6.grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.entry_j6.grid(row=5, column=1,sticky='w', padx=5, pady=5)        
        # Main action buttons
        self.button_1 = Button(self, text='Move', command=parent.move)

        self.button_1.grid(row=7, column=0, columnspan=2,pady=10)


app = App()
app.mainloop()
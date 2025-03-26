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

        self.j1 = DoubleVar(value= 318.0)
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
        Comp = 2

        try:        
            #Pose ="P(177.483268825558, -44.478627592948996, 254.99815172770593, -179.98842099994923, 0, 179.99584205147127, 261.0)"
            Pose ="P("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+", 261.0)"
            m_bcapclient.robot_move(HRobot,2,Pose,"")
            """
            Q1 = "@0 P(124.8479084757812, 96.71132432510223, 254.93505849932905, 179.98326477675423, -0.021660598353600596, 179.9971873030206, 261.0)"
            m_bcapclient.robot_move(HRobot,2,Q1,"")
            Q2 = "@0 P(201.62729889242553, 96.71465770886049, 254.9352502844515, 179.98348831787996, -0.021534861588810798, 179.99838567272027, 261.0)"
            m_bcapclient.robot_move(HRobot,2,Q2,"")
            Q3 = "@0 P(222.45008156262494, -28.895388040937206, 254.9197279214668, 179.9806000045344, -0.029053337503689936, 179.98516581416754, 261.0)"
            m_bcapclient.robot_move(HRobot,2,Q3,"")
            Q4 = "@0 P(217.31049652044388, -130.24508774032034, 254.89685566528902, 179.9716479887839, -0.03128951339508686, 179.98066547808395, 261.0)"
            m_bcapclient.robot_move(HRobot,2,Q4,"")
            Q5 = "@0 P(133.63413919141982, -131.393237172843, 254.87885013312, 179.9599341526348, -0.027773416827480392, 179.97129867455095, 261.0)"
            m_bcapclient.robot_move(HRobot,2,Q5,"")
            print("Complete Move P,@P P[1]")
            """
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
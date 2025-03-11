import bCAPClient.bcapclient as bcapclient

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

switch_bcap_to_orin(client, hRobot, caoRobot)
    # Open hand to release object. HandMoveA (open in mm, speed)
    ctrl.Execute(RobotAction.HAND_MOVE_A.value, [30, 25])
    switch_orin_to_bcap(client, hRobot, caoRobot)

### Set Parameters
#Interpolation
Comp=1

#Pose = "@P J(-3.84, -18.78, 123.81, 15.5, 50.15, 70.55)"
#Pose = "@P J(1.63, 50.89, 30, 7.85, 18.82, 70.55)"
#Pose = "@P P(174.41, 10.84, 166.05)"
#Pose = "@P J(5.84, -18.78, 123.81, 15.5, 50.15, 70.55)"
#m_bcapclient.robot_move(HRobot,Comp,Pose,"")
#print("Complete Move P,@P P[1]")

#Pose = "@P J(1.63, 50.89, 30, 7.85, 18.82, 70.55)"
#m_bcapclient.robot_move(HRobot,Comp,Pose,"")
#print("Complete Move P,@P P[1]")

Pose = "@P P(380.7966685850664, -12.04779397418564, 200.36141513361235, 108.03845050651411, 9.54516553939122, 97.65194420131768)"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[1]")



#VARIABILI

var = m_bcapclient.robot_getvariable(HRobot,"@CURRENT_POSITION")
value = m_bcapclient.variable_getvalue(var)

print("Variables: " + str(var))
print("Value: " + str(value))

var = m_bcapclient.robot_getvariable(HRobot,"@CURRENT_ANGLE")
value = m_bcapclient.variable_getvalue(var)

print("Variables: " + str(var))
print("Value: " + str(value))

#PoseData
'''
Pose = "@P P1"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[1]")
Pose = "@P P2"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[2]")
Pose = "@P P3"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[3]")
'''
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

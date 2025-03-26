#import tracemalloc
from tkinter import *
from win32com.client import Dispatch

import bCAPClient.bcapclient as bcapclient


from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog

import threading

import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model2 import KeyPointClassifier
#from model import PointHistoryClassifier
import speech_recognition as sr
import re
from page import Page1


def move_arm_to_position(Position):

    host = "192.168.0.1"
    port = 5007
    timeout = 2000

    m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
    #print("Open Connection")

    m_bcapclient.service_start("")
    #print("Send SERVICE_START packet")

    Name = ""
    Provider="CaoProv.DENSO.VRC"
    Machine = ("localhost")
    Option = ("")

    hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
    #print("Connect RC8")
    HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
    #print("AddRobot")

    Command = "TakeArm"
    Param = [0,0]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    #print("TakeArm")

    Comp=1
    m_bcapclient.robot_move(HRobot,Comp,Position,"")
    #print("Complete Move")


    Command = "GiveArm"
    Param = None
    m_bcapclient.robot_execute(HRobot,Command,Param)
    #print("GiveArm")
    
    if(HRobot != 0):
        m_bcapclient.robot_release(HRobot)
        #print("Release Robot Object")
    
    if(hCtrl != 0):
        m_bcapclient.controller_disconnect(hCtrl)
        #print("Release Controller")
    
    m_bcapclient.service_stop()
    #print("B-CAP service Stop")

def move_hand(input_value):
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

    eng = Dispatch("CAO.CaoEngine")
    ctrl = eng.Workspaces(0).AddController(
        "", "CaoProv.DENSO.RC8", "", "Server=" + "192.168.0.1"
    )

    caoRobot = ctrl.AddRobot("robot0", "")

    m_bcapclient.robot_execute(HRobot, "GiveArm")
    m_bcapclient.robot_execute(HRobot, "TakeArm", [0, 0])
    caoRobot.Execute("Motor", [1, 0])

    ##(open in mm, speed)

    ctrl.Execute("HandMoveA", [input_value, 25])

    caoRobot.Execute("GiveArm")
    m_bcapclient.robot_execute(HRobot, "TakeArm", [0, 0])
    m_bcapclient.robot_execute(HRobot, "Motor", [1, 0])


class App(Tk):
    def __init__(self):
        super().__init__()
        self.configure(background='white')

        self.passiBase = [10, 5, 4, 11, 7, 11]

        self.minimi = [-150, -60, 20, -165, -85, -165]
        self.massimi = [150, 90, 140, 165, 125, 165]

        self.passoMult = DoubleVar(value=1)

        self.j1 = DoubleVar(value=0)
        self.j2 = DoubleVar(value=15)
        self.j3 = DoubleVar(value=80)
        self.j4 = DoubleVar(value=0)
        self.j5 = DoubleVar(value=20)
        self.j6 = DoubleVar(value=0)

        self.hand = IntVar(value=30)

        
    
        self.title("PF4EA")
        self.geometry("1000x1200")
        self.page = Page1(self)
        self.start_position()


    def start_position(self):
       

        try:
            Position ="J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
            move_arm_to_position(Position)

            input_value = self.hand.get()
            move_hand(input_value)
               
            self.page.button_open.config(state=DISABLED)
        except:
            Page1.print_error("Errore di connessione")

            ##AGGIUNGI CONTROLLI EVENTUALI IN CASO SI VOGLIANO CAMBIARE LE POSIZIONI INIZIALI 
        


    def move(self, joint, var):

        if (joint is self.j1):
            index=0
            buttonsx= self.page.button_1s
            buttondx= self.page.button_1d
        elif (joint is self.j2):
            index=1
            buttonsx= self.page.button_2s
            buttondx= self.page.button_2d
        elif (joint is self.j3):
            index=2
            buttonsx= self.page.button_3s
            buttondx= self.page.button_3d
        elif (joint is self.j4):
            index=3
            buttonsx= self.page.button_4s
            buttondx= self.page.button_4d
        elif (joint is self.j5):
            index=4
            buttonsx= self.page.button_5s
            buttondx= self.page.button_5d
        elif (joint is self.j6):
            index=5
            buttonsx= self.page.button_6s
            buttondx= self.page.button_6d


        if(var == 0):
            j = joint.get() - int(self.passiBase[index] * self.passoMult.get())
            if j < self.minimi[index]:
                j = self.minimi[index]
            joint.set(j)
           

        elif(var == 1):
            j = joint.get() + int(self.passiBase[index] * self.passoMult.get())
            if j > self.massimi[index]:
                j = self.massimi[index]
            joint.set(j)




        if joint.get() == self.minimi[index]:
                buttonsx.config(state=DISABLED)
        else: 
                buttonsx.config(state=NORMAL)

        if joint.get() == self.massimi[index]:
                buttondx.config(state=DISABLED)
        else: 
                buttondx.config(state=NORMAL)
        
         

        Position ="@P J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        move_arm_to_position(Position)

    def modify_passo_mult(self, var):
        if var == 0:
            self.passoMult.set(self.passoMult.get() - 0.5)
        elif var == 1:
            self.passoMult.set(self.passoMult.get() + 0.5)
        else:
            Page1.print_error("Invalid var value")

        if self.passoMult.get() == 0.5:
            self.page.button_passos.config(state=DISABLED)
        else:
            self.page.button_passos.config(state=NORMAL)

        if self.passoMult.get() == 5:
            self.page.button_passod.config(state=DISABLED)
        else:
            self.page.button_passod.config(state=NORMAL)



    def close_hand(self):
      
        h = self.hand.get() - 3
        if h < 0:
            h = 0
        self.hand.set(h)

        if self.hand.get() == 0:
            self.page.button_close.config(state=DISABLED)

        self.page.button_open.config(state=NORMAL)

        input_value=self.hand.get()
        move_hand(input_value)

    def open_hand(self):
          
        self.hand.set(self.hand.get() + 3)

        h = self.hand.get() + 3
        if h > 30:
            h = 30
        self.hand.set(h)

        if self.hand.get() == 30:
            self.page.button_open.config(state=DISABLED)
        self.page.button_close.config(state=NORMAL)

        input_value=self.hand.get()
        move_hand(input_value)

##################### GESTURE#####################
############################################################################################################
        
    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        parser.add_argument('--use_static_image_mode', action='store_true')
        parser.add_argument("--min_detection_confidence",
                            help='min_detection_confidence',
                            type=float,
                            default=0.7)
        parser.add_argument("--min_tracking_confidence",
                            help='min_tracking_confidence',
                            type=int,
                            default=0.5)

        args = parser.parse_args()

        return args


    def start_gesture(self):
        # Argument parsing #################################################################
        args = self.get_args()

        cap_device = args.device
        cap_width = args.width
        cap_height = args.height

        use_static_image_mode = args.use_static_image_mode
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence

        use_brect = True

        # Camera preparation ###############################################################
        cap = cv.VideoCapture(cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

        # Model load #############################################################
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        keypoint_classifier = KeyPointClassifier()

       

        # Read labels ###########################################################
        with open('model2/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        

        # FPS Measurement ########################################################
        cvFpsCalc = CvFpsCalc(buffer_len=10)


        #  ########################################################################
        mode = 0

        a=0
        b=0
        c=0
        d=0
        e=0
        f=0
        g=0
        h=0
        joint = None
        robustezza = 10

        while True:
            fps = cvFpsCalc.get()

            # Process Key (ESC: end) #################################################
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
            number, mode = self.select_mode(key, mode)

            # Camera capture #####################################################
            ret, image = cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            # Detection implementation #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True

            #  ####################################################################
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                    results.multi_handedness):
                    # Bounding box calculation
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    # Landmark calculation
                    landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = self.pre_process_landmark(
                        landmark_list)
                    
                    # Write to the dataset file
                    self.logging_csv(number, mode, pre_processed_landmark_list)

                    # Hand sign classification
                    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                    
                    print(hand_sign_id)
                    print(keypoint_classifier_labels[hand_sign_id])
                    print()
                    print()

                    
                    
                    
                    
                    dxsx = handedness.classification[0].label[0:]
                    segno = keypoint_classifier_labels[hand_sign_id]


                    if segno == "LSign":
                        a=a+1
                        print("a:" + str(a))
                    if segno == "Pointer":
                        b=b+1
                    if segno == "ThumbUp":
                        c=c+1
                    if segno == "Shaker":
                        d=d+1
                    if segno == "Horns":
                        e=e+1
                    if segno == "3Fingers":
                        f=f+1
                    if segno == "Open":
                        g=g+1
                    if segno == "Close":
                        h=h+1


                  
                        
                    if a >=robustezza:
                        joint = self.j1
                        a=b=c=d=e=f=g=h=0
                        print("SONO ENTRATO")

                    if b>=robustezza:
                        joint = self.j2 
                        a=b=c=d=e=f=g=h=0

                    if c>=robustezza:
                        joint =  self.j3
                        a=b=c=d=e=f=g=h=0

                    if d>=robustezza:
                        joint = self.j4 
                        a=b=c=d=e=f=g=h=0

                    if e>=robustezza:
                        joint = self.j5
                        a=b=c=d=e=f=g=h=0

                    if f>=robustezza:
                        joint = self.j6
                        a=b=c=d=e=f=g=h=0

                    if g>=robustezza:
                        self.open_hand()
                        print("apro la mano")
                        a=b=c=d=e=f=g=h=0

                    if h>=robustezza:
                        self.close_hand()
                        print("chiudo la mano")
                        a=b=c=d=e=f=g=h=0



                    
                    if(joint != None):
                        if dxsx == "Right":
                            self.move(joint, 1)
                            print("mi sono mosso")
                        if dxsx == "Left":
                            self.move(joint, 0)
                            print("mi sono mosso")
                        joint=None
                        

                    print(keypoint_classifier_labels[hand_sign_id] + " " + dxsx)
                    # Drawing part
                    debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)
                    debug_image = self.draw_landmarks(debug_image, landmark_list)
                    debug_image = self.draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        keypoint_classifier_labels[hand_sign_id]
                    )

            debug_image = self.draw_info(debug_image, fps, mode, number)

            # Screen reflection #############################################################
            cv.imshow('Hand Gesture Recognition', debug_image)

        cap.release()
        cv.destroyAllWindows()


    def select_mode(self, key, mode):
        number = -1
        if 48 <= key <= 57:  # 0 ~ 9
            number = key - 48
        if key == 110:  # n
            mode = 0
        if key == 107:  # k
            mode = 1
        if key == 104:  # h
            mode = 2
        return number, mode


    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]


    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point


    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list



    def logging_csv(self, number, mode, landmark_list):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            csv_path = 'model2/keypoint_classifier/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 2 and (0 <= number <= 9):
            print("MODE = 2")
        return


    def draw_landmarks(self, image, landmark_point):
        if len(landmark_point) > 0:
            # Thumb
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (255, 255, 255), 2)

            # Index finger
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                    (255, 255, 255), 2)

            # Middle finger
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                    (255, 255, 255), 2)

            # Ring finger
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                    (255, 255, 255), 2)

            # Little finger
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                    (255, 255, 255), 2)

            # Palm
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                    (255, 255, 255), 2)

        # Key Points
        for index, landmark in enumerate(landmark_point):
            if index == 0:  # 手首1
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 1:  # 手首2
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 2:  # 親指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 3:  # 親指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 4:  # 親指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 5:  # 人差指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 6:  # 人差指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 7:  # 人差指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 8:  # 人差指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 9:  # 中指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 10:  # 中指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 11:  # 中指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 12:  # 中指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 13:  # 薬指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 14:  # 薬指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 15:  # 薬指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 16:  # 薬指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 17:  # 小指：付け根
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 18:  # 小指：第2関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 19:  # 小指：第1関節
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 20:  # 小指：指先
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        return image


    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            # Outer rectangle
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                        (0, 0, 0), 1)

        return image


    def draw_info_text(self, image, brect, handedness, hand_sign_text):
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                    (0, 0, 0), -1)

        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ':' + hand_sign_text
        cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

        return image


    

    
    def draw_info(self, image, fps, mode, number):
        cv.putText(image, "J1:" + str(self.j1.get()) + " J2:" + str(self.j2.get()) + " J3:" + str(self.j3.get()) + " J4:" + str(self.j4.get())
                   + " J5:" + str(self.j5.get()) + " J6:" + str(self.j6.get()) , (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 0), 4, cv.LINE_AA)
        
        cv.putText(image, "J1:" + str(self.j1.get()) + " J2:" + str(self.j2.get()) + " J3:" + str(self.j3.get()) + " J4:" + str(self.j4.get())
                   + " J5:" + str(self.j5.get()) + " J6:" + str(self.j6.get()), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2, cv.LINE_AA)

        mode_string = ['Logging Key Point']
        if 1 <= mode <= 2:
            cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv.LINE_AA)
            if 0 <= number <= 9:
                cv.putText(image, "NUM:" + str(number), (10, 110),
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                        cv.LINE_AA)
        return image
        
############################################################################################################        
  
    def update_message(self, message):
        """Aggiorna il testo del message_label nella pagina."""
        self.page.message_label.config(text=message)
    '''
    def use_voice (self):
        text = ""
        voice = True
        while voice: 
            recognizer_instance = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer_instance.adjust_for_ambient_noise(source)
                print("Cobotta è in ascolto: scegliere un giunto")
                audio = recognizer_instance.listen(source)
                text = recognizer_instance.recognize_google(audio, language="it-IT")
            print(text)
            
            joint_selected = False
            joint_mapping = {
                "uno": self.j1,
                "due": self.j2,
                "tre": self.j3,
                "quattro": self.j4,
                "cinque": self.j5,
                "sei": self.j6,
            }

            for key, joint_var in joint_mapping.items():
                if re.search(rf"\b{key}\b", text.lower()):
                    j = joint_var
                    joint_selected = True
                    print(f"Giunto selezionato: {key}")
                    break  

            if re.search(rf"\besci\b", text.lower()):
                voice = False
            
            while joint_selected:
                recognizer_instance = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer_instance.adjust_for_ambient_noise(source)
                    print("Cobotta è in ascolto: scegliere una direzione")
                    audio = recognizer_instance.listen(source)
                    text = recognizer_instance.recognize_google(audio, language="it-IT")
                print(text)
                if re.search(r"\bdestra\b", text.lower()):
                    self.move(j, 1)
                if re.search(r"\bsinistra\b", text.lower()):
                    self.move(j, 0)
                if re.search(r"\bstop\b", text.lower()):
                    joint_selected = False
    '''

    def stretch_arm(self):
       
        if self.j2.get() == self.massimi[1] or self.j3.get() == self.minimi[2]:
            return
        
        j2 = self.j2.get() + int(self.passiBase[1] * self.passoMult.get())
        if j2 > self.massimi[1]:
            j2 = self.massimi[1]
        self.j2.set(j2)

        j3 = self.j3.get() - int(self.passiBase[2] * self.passoMult.get())
        if j3 < self.minimi[2]:
            j3 = self.minimi[2]
        self.j3.set(j3)


        if self.j2.get() == self.massimi[1]:
                self.page.button_2d.config(state=DISABLED)

        if not(self.j2.get() == self.minimi[1]):
                self.page.button_2s.config(state=NORMAL)

        if self.j3.get() == self.minimi[2]:
                self.page.button_3s.config(state=DISABLED)
        
        if not(self.j3.get() == self.massimi[2]):
                self.page.button_3d.config(state=NORMAL)
        
         

        Position ="@P J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        move_arm_to_position(Position)


    def use_voice(self):
        text = ""
        joint_text=""
        voice = True
        joint_selected = False
        joint_mapping = {
            "uno": self.j1,
            "1": self.j1,
            "due": self.j2,
            "2": self.j2,
            "tre": self.j3,
            "3": self.j3,
            "quattro": self.j4,
            "4": self.j4,
            "cinque": self.j5,
            "5": self.j5,
            "sei": self.j6,
            "6": self.j6,
        }

        while voice:
            recognizer_instance = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer_instance.adjust_for_ambient_noise(source)
                if(not joint_selected):
                    self.update_message("Cobotta in ascolto...")
                else:
                    self.update_message(f"Cobotta in ascolto... Giunto: {joint_text}")
                
                try:
                    audio = recognizer_instance.listen(source, phrase_time_limit=60)
                    text = recognizer_instance.recognize_google(audio, language="it-IT")
                    print(text)
                except sr.UnknownValueError:
                    self.update_message("Non ho capito, riprova...")
                    continue
                except sr.RequestError as e:
                    self.update_message(f"Errore di connessione al servizio di riconoscimento vocale: {e}")
                    joint_selected = False
                    break
                
                increasing_words = ["destra", "giù", "scendi", "più", "aumenta"]
                decreasing_words = ["sinistra", "su", "sali" ,"meno", "diminuisci"]
                stop_words = ["stop", "esci", "ferma", "basta", "interrompi"]   
                open_words = ["apri", "apriti", "lascia", "rilascia", "molla"]
                close_words = ["chiudi", "chiuditi", "stringi", "prendi"]
                stretch_words = ["allunga", "allungati", "avanti", "estendi"]

                words = text.lower().split()
                for word in words:
                    if word in increasing_words:
                        if joint_selected:
                            self.update_message("Muovo il giunto...")
                            self.move(j, 1)
                        else:
                            self.update_message("Prima seleziona un giunto")
                    elif word in decreasing_words:
                        if joint_selected:
                            self.update_message("Muovo il giunto...")
                            self.move(j, 0)
                        else:
                            self.update_message("Prima seleziona un giunto")

                    elif word in stretch_words:
                        self.stretch_arm()
                        self.update_message("Allungo il braccio...")

                    elif word in joint_mapping.keys():
                        j = joint_mapping[word]
                        joint_selected = True
                        self.update_message(f"Giunto selezionato: {word}")
                        joint_text = word

                    elif word in open_words:
                        self.open_hand()
                        self.update_message("Apro la mano...")

                    elif word in close_words:
                        self.close_hand()
                        self.update_message("Chiudo la mano...")

                    elif word in stop_words:
                        joint_selected = False
                        voice = False
                        self.update_message("Smetto di ascoltare...")
                        self.update_message("")
                        break

#################################################
        
    def camera_button(self):
        t=threading.Thread(target=self.start_gesture)
        t.daemon=True
        t.start()

    def voice_button(self):
        t=threading.Thread(target=self.use_voice)
        t.daemon=True
        t.start()
            






app = App()
app.mainloop()
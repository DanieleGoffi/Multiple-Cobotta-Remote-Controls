from tkinter import *
from win32com.client import Dispatch
import bCAPClient.bcapclient as bcapclient
import threading
import csv
import copy
import itertools
import cv2 as cv
import numpy as np
import mediapipe as mp
from model2 import KeyPointClassifier
import speech_recognition as sr
from page import Page1



class App(Tk):
    def __init__(self):
        super().__init__()
        self.robot_lock = threading.Lock()
        self.configure(background='white')
        
        self.base_steps = [10, 5, 4, 11, 7, 11]

        self.min = [-150, -60, 20, -165, -85, -165]
        self.max = [150, 90, 140, 165, 125, 165]

        self.step_multiplier = DoubleVar(value=1)
        self.speed = IntVar(value = 50)

        self.j1 = DoubleVar(value=0)
        self.j2 = DoubleVar(value=15)
        self.j3 = DoubleVar(value=80)
        self.j4 = DoubleVar(value=0)
        self.j5 = DoubleVar(value=20)
        self.j6 = DoubleVar(value=0)
        self.hand = IntVar(value=30)

        self.title("Multiple Cobotta Remote Controls")
        self.geometry("500x750")
        self.page = Page1(self)
        self.start_position()


    # funzione per muovere il robot nella posizione desiderata
    def move_arm_to_position(self, Position):
        try:
            with self.robot_lock: 
                host = "192.168.0.1"
                port = 5007
                timeout = 2000
                m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
                m_bcapclient.service_start("")
                Name = ""
                Provider="CaoProv.DENSO.VRC"
                Machine = ("localhost")
                Option = ("")
                hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
                HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")

                Command = "TakeArm"
                Param = [0,0]
                m_bcapclient.robot_execute(HRobot,Command,Param)
                
                #velocià e accelerazione proporzionali
                Command = "ExtSpeed" 
                Speed = self.speed.get()
                Accel = self.speed.get()
                Decel = self.speed.get()
                Param = [Speed,Accel,Decel]
                m_bcapclient.robot_execute(HRobot,Command,Param)
              
                Comp=1
                m_bcapclient.robot_move(HRobot,Comp,Position,"")
                
                Command = "GiveArm"
                Param = None
                m_bcapclient.robot_execute(HRobot,Command,Param)
                
                
                if(HRobot != 0):
                    m_bcapclient.robot_release(HRobot)    
                if(hCtrl != 0):
                    m_bcapclient.controller_disconnect(hCtrl)        
                m_bcapclient.service_stop()
        except:
            Page1.print_error("Impossibile muovere il robot")
            #pass
      


    # funzione per muovere la mano del robot
    def move_hand(self, input_value):
        try:
            with self.robot_lock: 
                host = "192.168.0.1"
                port = 5007
                timeout = 2000
                m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
                m_bcapclient.service_start("")
                Name = ""
                Provider="CaoProv.DENSO.VRC"
                Machine = ("localhost")
                Option = ("")
                hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
                HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")

                Command = "TakeArm"
                Param = [0,0]
                m_bcapclient.robot_execute(HRobot,Command,Param)
                

                eng = Dispatch("CAO.CaoEngine")
                ctrl = eng.Workspaces(0).AddController(
                    "", "CaoProv.DENSO.RC8", "", "Server=" + "192.168.0.1"
                )
                caoRobot = ctrl.AddRobot("robot0", "")
                m_bcapclient.robot_execute(HRobot, "GiveArm")
                m_bcapclient.robot_execute(HRobot, "TakeArm", [0, 0])
                caoRobot.Execute("Motor", [1, 0])
                ctrl.Execute("HandMoveA", [input_value, 25])

                caoRobot.Execute("GiveArm")
                m_bcapclient.robot_execute(HRobot, "TakeArm", [0, 0])
                m_bcapclient.robot_execute(HRobot, "Motor", [1, 0])
        except:
            Page1.print_error("Impossibile muovere la mano del robot")
            #pass
            

    # funzione per bloccare il movimento del robot
    def stop(self):
        try:
            host = "192.168.0.1"
            port = 5007
            timeout = 2000
            m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
            m_bcapclient.service_start("")
            Name = ""
            Provider="CaoProv.DENSO.VRC"
            Machine = ("localhost")
            Option = ("")
            hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
            HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
            m_bcapclient.robot_execute(HRobot, "Motor", [0, 1])
        except:
            pass

    # funzione per portare il robot alla posizione iniziale
    def start_position(self): 

        Position ="J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        self.move_arm_to_position(Position)

        input_value = self.hand.get()
        self.move_hand(input_value)
            
        self.page.button_open.config(state=DISABLED)

        
    # funzione per muovere i giunti del robot in base al comando dato
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
            j = joint.get() - int(self.base_steps[index] * self.step_multiplier.get())
            if j < self.min[index]:
                j = self.min[index]
            joint.set(j)
        elif(var == 1):
            j = joint.get() + int(self.base_steps[index] * self.step_multiplier.get())
            if j > self.max[index]:
                j = self.max[index]
            joint.set(j)

        if joint.get() == self.min[index]:
                buttonsx.config(state=DISABLED)
        else: 
                buttonsx.config(state=NORMAL)

        if joint.get() == self.max[index]:
                buttondx.config(state=DISABLED)
        else: 
                buttondx.config(state=NORMAL)
    
        Position ="@P J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        self.move_arm_to_position(Position)


    # funzione per modificare il passo del robot 
    def modify_step_multiplier(self, var):
        if var == 0:
            self.step_multiplier.set(self.step_multiplier.get() - 0.5)
        elif var == 1:
            self.step_multiplier.set(self.step_multiplier.get() + 0.5)
        else:
            Page1.print_error("Invalid var value")

        if self.step_multiplier.get() == 0.5:
            self.page.button_passos.config(state=DISABLED)
        else:
            self.page.button_passos.config(state=NORMAL)

        if self.step_multiplier.get() == 5:
            self.page.button_passod.config(state=DISABLED)
        else:
            self.page.button_passod.config(state=NORMAL)


    # funzione per modificare la velocità del robot
    def modify_speed(self, var):
        if var == 0:
            self.speed.set(self.speed.get() - 10)
        elif var == 1:
            self.speed.set(self.speed.get() + 10)
        else:
            Page1.print_error("Invalid var value")

        
        if self.speed.get() == 10:
            self.page.button_speeds.config(state=DISABLED)
        else:
            self.page.button_speeds.config(state=NORMAL)

        if self.speed.get() == 100:
            self.page.button_speedd.config(state=DISABLED)
        else:
            self.page.button_speedd.config(state=NORMAL)
        

    # funzione per chiudere la mano del robot
    def close_hand(self):
      
        h = self.hand.get() - 3
        if h < 0:
            h = 0
        self.hand.set(h)

        if self.hand.get() == 0:
            self.page.button_close.config(state=DISABLED)

        self.page.button_open.config(state=NORMAL)

        input_value=self.hand.get()
        self.move_hand(input_value)


    # funzione per aprire la mano del robot
    def open_hand(self):
          
        h = self.hand.get() + 3
        if h > 30:
            h = 30
        self.hand.set(h)

        if self.hand.get() == 30:
            self.page.button_open.config(state=DISABLED)
        self.page.button_close.config(state=NORMAL)

        input_value=self.hand.get()
        self.move_hand(input_value)


    #### GESTURE ###
   
    # funzione per l'acquisizione dei gesti
    def start_gesture(self):
        self.page.button_camera.config(state=DISABLED)
        self.page.message_cam_label.config(text="Premere ESC per uscire")

        cap_device = 0
        cap_width = 960
        cap_height = 540
        min_detection_confidence = 0.7
        min_tracking_confidence = 0.5

        use_brect = True

        cap = cv.VideoCapture(cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        # uso del modello di riconoscimento dei gesti
        keypoint_classifier = KeyPointClassifier()
        
        with open('model2/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        
        mode = 0 # acquisizione immagini e riconoscimento gesti

        a=0
        b=0
        c=0
        d=0
        e=0
        f=0
        g=0
        h=0
        joint = None
        robustness = 10

        while True:

            # tasto esc per uscire dall'acquisizione gesti
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
         
            number, mode = self.select_mode(key, mode)

            ret, image = cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)  
            debug_image = copy.deepcopy(image)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                    results.multi_handedness):
                    
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    
                    landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                    pre_processed_landmark_list = self.pre_process_landmark(
                        landmark_list)
                                        
                    self.logging_csv(number, mode, pre_processed_landmark_list)

                    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                    
                    dxsx = handedness.classification[0].label[0:]
                    sign = keypoint_classifier_labels[hand_sign_id]
                    
                    # gestione della robustezza delle acquisizioni
                    if sign == "LSign":
                        a=a+1
                    if sign == "Pointer":
                        b=b+1
                    if sign == "ThumbUp":
                        c=c+1
                    if sign == "Shaker":
                        d=d+1
                    if sign == "Horns":
                        e=e+1
                    if sign == "3Fingers":
                        f=f+1
                    if sign == "Open":
                        g=g+1
                    if sign == "Close":
                        h=h+1

                    if a >=robustness:
                        joint = self.j1
                        a=b=c=d=e=f=g=h=0
                    if b>=robustness:
                        joint = self.j2 
                        a=b=c=d=e=f=g=h=0
                    if c>=robustness:
                        joint =  self.j3
                        a=b=c=d=e=f=g=h=0
                    if d>=robustness:
                        joint = self.j4 
                        a=b=c=d=e=f=g=h=0
                    if e>=robustness:
                        joint = self.j5
                        a=b=c=d=e=f=g=h=0
                    if f>=robustness:
                        joint = self.j6
                        a=b=c=d=e=f=g=h=0
                    if g>=robustness:
                        self.open_hand()
                        a=b=c=d=e=f=g=h=0
                    if h>=robustness:
                        self.close_hand()
                        a=b=c=d=e=f=g=h=0

                    if(joint != None):
                        if dxsx == "Right":
                            self.move(joint, 1)
                        if dxsx == "Left":
                            self.move(joint, 0)
                        joint=None
                        

                    debug_image = self.draw_bounding_rect(use_brect, debug_image, brect)
                    debug_image = self.draw_landmarks(debug_image, landmark_list)
                    debug_image = self.draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        keypoint_classifier_labels[hand_sign_id]
                    )

            debug_image = self.draw_info(debug_image, mode, number)

            cv.imshow('Hand Gesture Recognition', debug_image)

        cap.release()
        cv.destroyAllWindows()
        self.page.button_camera.config(state=NORMAL)
        self.page.message_cam_label.config(text="")


    # funzione per selezionare la modalità (normale / salvataggio gesto)
    def select_mode(self, key, mode):
        number = -1
        if 48 <= key <= 57:  # 0 ~ 9 per assegnare un id nel csv al gesto durante la modalità 1
            number = key - 48
        if key == 110:  # n per passare alla modalità di riconoscimento
            mode = 0
        if key == 107:  # k per passare alla modalita di salvataggio dei gesti
            mode = 1
        return number, mode


    # funzione per calcolare il rettangolo di delimitazione attorno ai punti chiave della mano
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


    # funzione per calcolare le coordinate dei punti chiave della mano
    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point.append([landmark_x, landmark_y])

        return landmark_point


    # funzione per pre-elaborare la lista dei punti chiave della mano
    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)
        base_x, base_y = 0, 0

        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]
            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value
        
        temp_landmark_list = list(map(normalize_, temp_landmark_list))
        return temp_landmark_list


    # funzione per il salvataggio dei dati dei punti chiave all'interno del file csv
    def logging_csv(self, number, mode, landmark_list):
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            csv_path = 'model2/keypoint_classifier/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        return


    # funzione per disegnare i punti chiave e le connessioni della mano sull'immagine
    def draw_landmarks(self, image, landmark_point):
        if len(landmark_point) > 0:
            # pollice
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                    (255, 255, 255), 2)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (0, 0, 0), 6)
            cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                    (255, 255, 255), 2)

            # indice
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

            # medio
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

            # anulare
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

            # mignolo
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

            # palmo
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

        for index, landmark in enumerate(landmark_point):
            if index == 0: 
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 1:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 2: 
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 3:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 4: 
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 5: 
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 6: 
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 7:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 8:  
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 9:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 10:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 11: 
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 12:  
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 13:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 14:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 15:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 16:  
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
            if index == 17:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 18:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 19:  
                cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
            if index == 20:  
                cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                        -1)
                cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

        return image


    # funzione per disegnare il rettangolo di delimitazione
    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                        (0, 0, 0), 1)
        return image

    # funzione per mostrare testo informativo
    def draw_info_text(self, image, brect, handedness, hand_sign_text):
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                    (0, 0, 0), -1)
        
        info_text = handedness.classification[0].label[0:]
        if hand_sign_text != "":
            info_text = info_text + ':' + hand_sign_text
        cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

        return image

    
    # funzione per mostrare informzaioni (valore dei giunti) sull'immagine
    def draw_info(self, image, mode, number):
        cv.putText(image, "J1:" + str(self.j1.get()) + " J2:" + str(self.j2.get()) + " J3:" + str(self.j3.get()) + " J4:" + str(self.j4.get())
                   + " J5:" + str(self.j5.get()) + " J6:" + str(self.j6.get()) , (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 0), 4, cv.LINE_AA)
        
        cv.putText(image, "J1:" + str(self.j1.get()) + " J2:" + str(self.j2.get()) + " J3:" + str(self.j3.get()) + " J4:" + str(self.j4.get())
                   + " J5:" + str(self.j5.get()) + " J6:" + str(self.j6.get()), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2, cv.LINE_AA)

        mode_string = ['Logging Key Point']
        if mode == 1:
            cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                    cv.LINE_AA)
            if 0 <= number <= 9:
                cv.putText(image, "NUM:" + str(number), (10, 110),
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                        cv.LINE_AA)
        return image
        

    #### VOICE ###        
  
    # funzione per eseguire l'azione definita (fare canestro)
    def play_basketball(self):
        self.return_to_start()

        Pos1 ="@P J(3.7,66.74,85.29,5.34,18.54,-5.13)"
        Pos2 ="@P J(25.13,34.56,20,5.93,55.16,-1.37)"
        Pos3 ="@P J(38.30,84.26,20,2.08,60.09,-87.74)"
        hand1 = 10
        hand2 = 15
        self.move_arm_to_position(Pos1)
        self.move_hand(hand1)
        self.move_arm_to_position(Pos2)
        self.move_arm_to_position(Pos3)
        self.move_hand(hand2)

        self.return_to_start()
    

    # funzione per allungare il braccio robot
    def stretch_arm(self):
        if self.j2.get() == self.max[1] or self.j3.get() == self.min[2]:
            return
        
        j2 = self.j2.get() + int(self.base_steps[1] * self.step_multiplier.get())
        if j2 > self.max[1]:
            j2 = self.max[1]
        self.j2.set(j2)

        j3 = self.j3.get() - int(self.base_steps[2] * self.step_multiplier.get())
        if j3 < self.min[2]:
            j3 = self.min[2]
        self.j3.set(j3)

        if self.j2.get() == self.max[1]:
                self.page.button_2d.config(state=DISABLED)
        if not(self.j2.get() == self.min[1]):
                self.page.button_2s.config(state=NORMAL)
        if self.j3.get() == self.min[2]:
                self.page.button_3s.config(state=DISABLED)
        if not(self.j3.get() == self.max[2]):
                self.page.button_3d.config(state=NORMAL)
        
        Position ="@P J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        self.move_arm_to_position(Position)


    # funzione per tornare alla posizione iniziale
    def return_to_start(self):
        self.j1.set(0)
        self.j2.set(15)
        self.j3.set(80)
        self.j4.set(0)
        self.j5.set(20)
        self.j6.set(0)
        self.hand.set(30)

        Position ="@P J("+ str(self.j1.get())+"," + str(self.j2.get())+"," + str(self.j3.get())+"," + str(self.j4.get())+"," + str(self.j5.get())+"," + str(self.j6.get())+")"
        self.move_arm_to_position(Position)
        input_value= self.hand.get()
        self.move_hand(input_value)
        
        cam_disabled = False
        if self.page.button_camera.cget("state")== DISABLED:
            cam_disabled = True

        for widget in self.page.winfo_children():
            if isinstance(widget, Button):
                widget.config(state=NORMAL)
        self.page.button_open.config(state=DISABLED)
        self.page.button_mic.config(state=DISABLED)
        
        if cam_disabled:
            self.page.button_camera.config(state=DISABLED)

    # funzione per utilizzare il riconoscmento vocale
    def use_voice(self):
        self.page.button_mic.config(state=DISABLED)
        text = ""
        joint_text=""
        voice = True
        joint_selected = False
        joint_mapping = {  # dizionario per associare i numeri ai giunti
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

        increasing_words = ["destra", "giù", "scendi", "più", "aumenta"]
        decreasing_words = ["sinistra", "su", "sali" ,"meno", "diminuisci"]
        exit_words = ["esci", "basta", "interrompi"]
        stop_words = ["stop", "ferma", "ahia"]   
        open_words = ["apri", "apriti", "lascia", "rilascia", "molla"]
        close_words = ["chiudi", "chiuditi", "stringi", "prendi"]
        stretch_words = ["allunga", "allungati", "avanti", "estendi"]
        start_position_words = ["iniziale", "inizio", "all'inizio", "partenza", "reset", "riparti", "ripristina"]
        basket_words = ["canestro", "pallacanestro", "basket", "lebron", "james", "23"]

        while voice:
            recognizer_instance = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer_instance.adjust_for_ambient_noise(source)
                if(not joint_selected):
                    self.update_message("Cobotta in ascolto...")
                else:
                    self.update_message(f"Giunto: {joint_text}...")

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
                        self.update_message("Allungo il braccio...")
                        self.stretch_arm()
                    elif word in joint_mapping.keys():
                        j = joint_mapping[word]
                        joint_selected = True
                        joint_text = word
                        self.update_message(f"Giunto selezionato: {word}")
                    elif word in open_words:
                        self.update_message("Apro la mano...")
                        self.open_hand()
                    elif word in close_words:
                        self.update_message("Chiudo la mano...")
                        self.close_hand()
                    elif word in start_position_words:
                        self.update_message("Ritorno alla posizione iniziale...")
                        self.return_to_start()
                    elif word in basket_words:
                        self.update_message("LeBron James...")
                        self.play_basketball()
                    elif word in exit_words:
                        joint_selected = False
                        voice = False
                        self.update_message("Smetto di ascoltare...")
                        self.update_message("")
                        self.page.button_mic.config(state=NORMAL)
                        break
                    elif word in stop_words:
                        self.stop_button()
                        self.update_message("STOP!")
                        break
                        
                

    ### funzioni associate ai bottoni della pagina che eseguono i relativi metodi in thread separati
    def move_button(self, joint, direction):
        t=threading.Thread(target=self.move, args=(joint, direction))
        t.daemon=True
        t.start()

    def camera_button(self):
        t=threading.Thread(target=self.start_gesture)
        t.daemon=True
        t.start()

    def voice_button(self):
        t=threading.Thread(target=self.use_voice)
        t.daemon=True
        t.start()

    def stop_button(self):
        t=threading.Thread(target=self.stop)
        t.daemon=True
        t.start()

    # funzione per modificare il messaggio di testo nella pagina
    def update_message(self, message):
        self.page.message_mic_label.config(text=message)


   
        

app = App()
app.mainloop()
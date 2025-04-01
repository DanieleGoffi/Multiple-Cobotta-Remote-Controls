from tkinter import *
from tkinter.messagebox import showerror



class Page1(Frame):

    def print_error(message:str):
        showerror("Error", message)

    
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(pady=5)

        # testo con i valori dei giunti
        self.label_j1 = Label(self, text='J1', font=('calibre', 10, 'bold'))
        self.entry_j1 = Entry(self, textvariable=parent.j1, font=('calibre', 10, 'normal'))
        
        self.label_j2 = Label(self, text='J2', font=('calibre', 10, 'bold'))
        self.entry_j2 = Entry(self, textvariable=parent.j2, font=('calibre', 10, 'normal'))
        
        self.label_j3 = Label(self, text='J3', font=('calibre', 10, 'bold'))
        self.entry_j3 = Entry(self, textvariable=parent.j3, font=('calibre', 10, 'normal'))
        
        self.label_j4 = Label(self, text='J4', font=('calibre', 10, 'bold'))
        self.entry_j4 = Entry(self, textvariable=parent.j4, font=('calibre', 10, 'normal'))
          
        self.label_j5 = Label(self, text='J5', font=('calibre', 10, 'bold'))
        self.entry_j5 = Entry(self, textvariable=parent.j5, font=('calibre', 10, 'normal'))
        
        self.label_j6 = Label(self, text='J6', font=('calibre', 10, 'bold'))
        self.entry_j6 = Entry(self, textvariable=parent.j6, font=('calibre', 10, 'normal'))

        self.label_j1.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        self.entry_j1.grid(row=0, column=2,sticky='w', padx=5, pady=5)
        self.label_j2.grid(row=1, column=1, sticky='e', padx=5, pady=5)
        self.entry_j2.grid(row=1, column=2,sticky='w', padx=5, pady=5)              
        self.label_j3.grid(row=2, column=1, sticky='e', padx=5, pady=5)
        self.entry_j3.grid(row=2, column=2,sticky='w', padx=5, pady=5)       
        self.label_j4.grid(row=3, column=1, sticky='e', padx=5, pady=5)
        self.entry_j4.grid(row=3, column=2,sticky='w', padx=5, pady=5)        
        self.label_j5.grid(row=4, column=1, sticky='e', padx=5, pady=5)
        self.entry_j5.grid(row=4, column=2,sticky='w', padx=5, pady=5)        
        self.label_j6.grid(row=5, column=1, sticky='e', padx=5, pady=5)
        self.entry_j6.grid(row=5, column=2,sticky='w', padx=5, pady=5) 

        # bottoni per muovere i giunti 
        self.button_1s = Button(self, text='<', command=lambda: parent.move_button(parent.j1, 0))
        self.button_1d = Button(self, text='>', command=lambda: parent.move_button(parent.j1, 1))

        self.button_2s = Button(self, text='<', command=lambda: parent.move_button(parent.j2, 0))
        self.button_2d = Button(self, text='>', command=lambda: parent.move_button(parent.j2, 1))

        self.button_3s = Button(self, text='<', command=lambda: parent.move_button(parent.j3, 0))
        self.button_3d = Button(self, text='>', command=lambda: parent.move_button(parent.j3, 1))

        self.button_4s = Button(self, text='<', command=lambda: parent.move_button(parent.j4, 0))
        self.button_4d = Button(self, text='>', command=lambda: parent.move_button(parent.j4, 1))

        self.button_5s = Button(self, text='<', command=lambda: parent.move_button(parent.j5, 0))
        self.button_5d = Button(self, text='>', command=lambda: parent.move_button(parent.j5, 1))

        self.button_6s = Button(self, text='<', command=lambda: parent.move_button(parent.j6, 0))
        self.button_6d = Button(self, text='>', command=lambda: parent.move_button(parent.j6, 1))
        
        self.button_1s.grid(row=0, column=0, columnspan=1, pady=10)
        self.button_1d.grid(row=0, column=3, columnspan=1, pady=10)
        self.button_2s.grid(row=1, column=0, columnspan=1, pady=10)
        self.button_2d.grid(row=1, column=3, columnspan=1, pady=10)
        self.button_3s.grid(row=2, column=0, columnspan=1, pady=10)
        self.button_3d.grid(row=2, column=3, columnspan=1, pady=10)
        self.button_4s.grid(row=3, column=0, columnspan=1, pady=10)
        self.button_4d.grid(row=3, column=3, columnspan=1, pady=10)
        self.button_5s.grid(row=4, column=0, columnspan=1, pady=10)
        self.button_5d.grid(row=4, column=3, columnspan=1, pady=10)
        self.button_6s.grid(row=5, column=0, columnspan=1, pady=10)
        self.button_6d.grid(row=5, column=3, columnspan=1, pady=10)

        # bottoni e testo per la presa
        self.button_open = Button(self, text='OPEN', command=parent.open_hand)
        self.button_open.grid(row=6, column=0, columnspan=1, pady=10)

        self.button_close = Button(self, text='CLOSE', command=parent.close_hand)
        self.button_close.grid(row=6, column=3, columnspan=1, pady=10)

        self.label_h = Label(self, text='H', font=('calibre', 10, 'bold'))
        self.entry_h = Entry(self, textvariable=parent.hand, font=('calibre', 10, 'normal'))
        self.label_h.grid(row=6, column=1, sticky='e', padx=5, pady=5)
        self.entry_h.grid(row=6, column=2, sticky='w', padx=5, pady=5)
        self.entry_h.config(state='readonly')

        # bottoni e testo per il passo 
        self.label_passoMult = Label(self, text='Step length : ', font=('calibre', 10, 'bold'))
        self.entry_passoMult = Entry(self, textvariable=parent.step_multiplier, font=('calibre', 10, 'normal'))

        self.label_passoMult.grid(row=7, column=2, sticky='w', padx=5, pady=5)
        self.entry_passoMult.grid(row=8, column=2, sticky='w', padx=5, pady=5) 

        self.button_passos = Button(self, text='<', command=lambda: parent.modify_step_multiplier(0))
        self.button_passod = Button(self, text='>', command=lambda: parent.modify_step_multiplier(1))

        self.button_passos.grid(row=8, column=0, columnspan=1, pady=10)
        self.button_passod.grid(row=8, column=3, columnspan=1, pady=10)

        # bottoni e testo per la velocità
        self.label_speed = Label(self, text='Speed: ', font=('calibre', 10, 'bold'))
        self.entry_speed = Entry(self, textvariable=parent.speed, font=('calibre', 10, 'normal'))

        self.label_speed.grid(row=9, column=2, sticky='w', padx=5, pady=5)
        self.entry_speed.grid(row=10, column=2, sticky='w', padx=5, pady=5) 

        
        self.button_speeds = Button(self, text='<', command=lambda: parent.modify_speed(0))
        self.button_speedd = Button(self, text='>', command=lambda: parent.modify_speed(1))

        self.button_speeds.grid(row=10, column=0, columnspan=1, pady=10)
        self.button_speedd.grid(row=10, column=3, columnspan=1, pady=10)
        
        # impostare in sola lettura il testo
        self.entry_j1.config(state='readonly')
        self.entry_j2.config(state='readonly')
        self.entry_j3.config(state='readonly')
        self.entry_j4.config(state='readonly')
        self.entry_j5.config(state='readonly')
        self.entry_j6.config(state='readonly')
        self.entry_passoMult.config(state='readonly')
        self.entry_speed.config(state='readonly')


        # bottoni e messaggi per la videocamera e il microfono
        self.button_camera = Button(self, text='OPEN CAMERA', command=parent.camera_button)
        self.button_camera.grid(row=35, column=0, columnspan=4, pady=10)

        self.message_cam_label = Label(self, text='', font=('calibre', 10, 'bold'), fg='blue', wraplength=400, justify='left')
        self.message_cam_label.grid(row=36, column=0, columnspan=4, pady=10)

        self.button_mic = Button(self, text='OPEN MIC', command=parent.voice_button)
        self.button_mic.grid(row=37, column=0, columnspan=4, pady=10)

        self.message_mic_label = Label(self, text='', font=('calibre', 10, 'bold'), fg='blue', wraplength=400, justify='left')
        self.message_mic_label.grid(row=38, column=0, columnspan=4, pady=10)

        # bottone per l'interruzione forzata del movimento
        self.button_stop = Button(self, text='STOP', command=parent.stop_button, fg='red')
    
        self.button_stop.grid(row=39, column=0, columnspan=4, pady=10, sticky="nsew")
        self.master.grid_rowconfigure(39, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.button_stop.config(font=("Arial", 20))


from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import tkinter.font as font
from tkinter.ttk import Treeview
from datetime import datetime

# View fail on põhiaken


class View(Tk):


    def __init__(self, controller):  # kogu akna asjad tehakse siin korraga
        super().__init__()  # Tk jaoks
        self.controller = controller
        self.__width__ = 550
        self.__height__ = 500
        self.default_font = font.Font(family='Verdana', size=14)  #  vidinate kirjastiil

        #  Akna omadused
        self.title('Arva ära GUI')
        self.center_window(self.__width__, self.__height__)

        #  Loome kaks frame´i
        self.top_frame = self.create_top_frame()
        self.bottom_frame = self.create_bottom_frame()

        #  Vidinate loomine
        self.btn_new_game, self.num_entry, self.btn_send, self.text_box, self.btn_scoreboard = self.create_frame_widgets()

        #   Enter klahvi vajutus tööle
        self.bind('<Return>', self.controller.send_click)
        self.protocol('WM_DELETE_WINDOW', self.on_close)    #Klikk close


    def main(self):
            self.mainloop()

        # teeme 2 frame'i funktsioonid
    def create_top_frame(self):
        frame = Frame(self, bg='lightblue', height=15)
        frame.pack(expand=True, fill=BOTH)  # BOTH on tkinteris konstant
        return frame  # tagastame frame´i et saaks seda mujal kasutada

    def create_bottom_frame(self):
        frame = Frame(self, bg='pink')
        frame.pack(expand=True, fill=BOTH)
        return frame  # frame´i peale lähevad nupud jm kastid

    def create_frame_widgets(self):
        #  nupp - uus mäng # lambda tahab sulge, command mitte
        btn_new_game = Button(self.top_frame, text='Uus mäng', font=self.default_font,
                              command=self.controller.new_game_click)
        btn_new_game.grid(row=0, column=0, padx=5, pady=5, sticky=EW)

        #  Label - sisesta tekst
        lbl_info = Label(self.top_frame, text='Sisesta number', font=self.default_font)
        lbl_info.grid(row=1, column=0, padx=5, pady=5)

        #  Sisestuskast numbrile
        num_entry = Entry(self.top_frame, font=self.default_font, state='disabled')
        num_entry.grid(row=1, column=1, padx=5, pady=5)
        num_entry.focus()

        #  nupp saada/sisesta - loeb vormilt, mis on kirjutatud ja tagastab
        btn_send = Button(self.top_frame, text='Saada', font=self.default_font,
                          state=DISABLED, command=self.controller.send_click)
        btn_send.grid(row=1, column=2, padx=5, pady=5)

        #  alumine kast koos kerimisribaga (scrollbar)
        text_box = Text(self.bottom_frame, font=self.default_font, state=DISABLED)
        scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL)
        scrollbar.config(command=text_box.yview)
        text_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)  #  scrollbar paremale poole ja täita vaid ülevalt alla osa
        text_box.pack(expand=True, fill=BOTH, padx=5, pady=5)
        #  edetabeli nupp
        btn_scoreboard = Button(self.top_frame, text='Edetabel', font=self.default_font, command=lambda: self.controller.scoreboard_click())
        btn_scoreboard.grid(row=0, column=2, padx=5, pady=5)

        #  tagastamine algusesse - lbl_info, scrollbar ei muutu
        return btn_new_game, num_entry, btn_send,text_box, btn_scoreboard

    def create_popup_window(self):
        top = Toplevel(self)
        top.title('Edetabel')
        top_width = 500
        top_height = 150

        x = (top.winfo_screenwidth() // 2) - (top_width // 2)  # asetab akna olemasoleva ekraani keskele
        y = (top.winfo_screenheight() // 2) - (top_height // 2)
        top.geometry(f'{top_width}x{top_height}+{x}+{y}')
        top.resizable(False, False) # Scoreboardi ei saa suurust muuta
        top.grab_set()  #Ei saa klikkida mängu põhiaknal
        top.focus() # Fookus top aknale

        frame = Frame(top)  #Frame luuakse top aknale
        frame.pack(fill=BOTH, expand=True)

        return frame    #Framei peale tuleb tabel

    def generate_scoreboard(self, frame, data):
        my_table = Treeview(frame)

        vsb = Scrollbar(frame, orient=VERTICAL, command=my_table.yview) #vertivalscrollbar, on vaja kõik kolm kirjutada, varem command puudu
        vsb.pack(side=RIGHT, fill=Y)
        my_table.configure(yscrollcommand=vsb.set)

        my_table['columns'] = ('name', 'steps', 'pc_nr', 'cheater', 'date_time')

        # Tabeli päise seaded. Esimene veerg on peidetud
        my_table.column('#0', width=0, stretch=NO)
        my_table.column('name', anchor=CENTER, width=100)
        my_table.column('steps', anchor=CENTER, width=50)
        my_table.column('pc_nr', anchor=CENTER, width=50)
        my_table.column('cheater', anchor=CENTER, width=50)
        my_table.column('date_time', anchor=CENTER, width=80)

        # Tabeli päise
        my_table.heading('#0', text='', anchor=CENTER)
        my_table.heading('name', text='Nimi', anchor=CENTER)
        my_table.heading('steps', text='Sammud', anchor=CENTER)
        my_table.heading('pc_nr', text='Arv', anchor=CENTER)
        my_table.heading('cheater', text='Petja', anchor=CENTER)
        my_table.heading('date_time', text='Kuupäev', anchor=CENTER)


        # Tabeli täitmine andmetega
        x = 0
        for player in data:
            date_time = datetime.strptime(player.date_time, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')

            #strptime() ja strftime()
            my_table.insert(parent='', index='end', iid=x, values=(player.name, player.steps, player.pc_nr, player.cheater, date_time))

            x += 1
        my_table.pack(fill=BOTH, expand=True)

    def on_close(self):
        if messagebox.askokcancel('Välju mängust', 'Kas soovid tõesti mängust väljuda?'):
            self.destroy()





    def center_window(self, width, height):
        x = (self.winfo_screenwidth() // 2) - (width // 2)  # asetab akna olemasoleva ekraani keskele
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') # ekraani laius * kõrgus ja liita x ja y-koordinaadid
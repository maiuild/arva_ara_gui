from tkinter import simpledialog

from Model import Model
from View import View


class Controller:  #  klassi nimi vastavalt faili nimele
    def __init__(self):
        self.model = Model()  #  self kasutame igas funktsioonil - mudelis vajalik info kogu faili ulatuses ligipääs
        self.view = View(self)  # viewle anname kontrolleri ehk 'self' kaasa


    def new_game_click(self):  #  Algab uus mäng
        self.model.start_new_game()
        self.view.btn_new_game['state'] = 'disabled'  #  Määrame staatuseks disabled
        self.view.num_entry['state'] = 'normal'  #  saab klikkida
        self.view.btn_send['state'] = 'normal'

    #  võtab vormist info ja töötleb
    def send_click(self, event=None):  #  event sulgudest kustutatud. Kas hiireklõps või enter mõlemad töötavad
        result = self.model.get_user_input(self.view.num_entry.get().strip())
        #  result on tekst, mida näidata kasutajale

        self.view.num_entry.delete(0, 'end') # tühjendab sisestuskasti
        self.view.text_box.config(state='normal')  #  Tekstikasti saab kirjutada
        self.view.text_box.insert('insert', result + '\n')  #  Kirjuta tulemus kasti
        self.view.text_box.see('end')  #  Viib vaatamise lõppu
        self.view.text_box.config(state='disabled')  #  Tekstikasti ei saa kirjutada

        if self.model.game_over:
            self.view.btn_new_game['state'] = 'normal'  #  mängu lõpus saab uut alustada nupust
            self.view.num_entry['state'] = 'disabled'
            self.view.btn_send['state'] = 'disabled'
            #  kontrollib petjat
          # if not self.model.cheater:  #  küsib nime vaid siis kui on tõene - ei ole petja
            self.ask_name()  #  küsi mängija nime
            self.model.add_or_not_database()  #Lisa mängija edetabelisse (database table)
             # TODO Enter klahv sisestuseks
                # view menüü to-do otsib üles

    def ask_name(self):
        name = simpledialog.askstring('Nimi', 'Kuidas on sinu nimi?')
        #  mängija nimi on alguses None.
        self.model.name = name  # omistame muutujale uue mängija_nime
        #  self.model.name on meie ainus setter. userinputkontroll

    def scoreboard_click(self):
        # TODO Edetabeli tegemine ja näitamine
        frame = self.view.create_popup_window()
        data = self.model.read_from_table()
        self.view.generate_scoreboard(frame, data)



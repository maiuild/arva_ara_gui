from Controller import Controller
class Game:
    def __init__(self):
        game = Controller()    #pass- Saab käivitada kuigi on tühi
        game.view.main()    #Teeb põhi akna nähtavaks

if __name__ == "__main__":  #Loob objecti Game.
    Game()
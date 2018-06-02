import tkinter as tk
from screens import SetUpScreen, GameScreen

class Window:
    """
    Class representing tkinter Tk() window.
    Manages the communication between the Setup and Game screens.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.width = 1024
        self.height = 675
        self.root.title("Minesweeper")
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root["bg"] = "#c9daf8"

        self.is_setup = False
        self.is_game = False

        ####setup screen
        self.setup_screen = SetUpScreen(self)
        self.setup_screen.but_play["command"] = self.showGameScreen

        ####game screen
        self.game_screen = GameScreen(self)
        self.game_screen.but_cancel["command"] = self.showSetUpScreen

    def showSetUpScreen(self):
        self.is_setup = True
        if self.is_game:
            self.game_screen.destroy()
        self.is_game = False

        self.setup_screen.show()

    def showGameScreen(self):
        h = self.setup_screen.height_option
        w = self.setup_screen.width_option
        n_m = self.setup_screen.mines_option
        if (h.ent.get().isdigit() \
           and h.mini <= int(h.ent.get()) <= h.maxi \
           and w.ent.get().isdigit() \
           and w.mini <= int(w.ent.get()) <= w.maxi \
           and n_m.ent.get().isdigit() \
           and n_m.mini <= int(n_m.ent.get()) <= n_m.maxi):

            self.game_screen.setNewGame(int(h.ent.get()), int(w.ent.get()),
                                        int(n_m.ent.get()))

            self.is_game = True
            if self.is_setup:
                self.setup_screen.destroy()
            self.is_setup = False

            self.game_screen.show()

###########################################################################

window = Window()

window.showSetUpScreen()

tk.mainloop()

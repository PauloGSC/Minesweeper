from time import monotonic
import tkinter as tk
from game import Grid

## colors:
## blue = #cfe2f3 < #9fc5e8 < #6fa8dc
## green = #65c680 < #17c651
## red = #c67474 < #c63d3d
## yellow = #ffd966 < #f1c232
##
## \u2620 = skull and bones
## \u2690 and \u2691 = flags
## \u23f1 = clock
##
## prefix for widgets names:
## but, lab, ent, frm

class Screen:
    """
    Abstract class. Sets a window for the screen and retrieves its
    height and width. Defines a abstract method (show) and a
    concrete one (destroy).
    """

    def __init__(self, window):
        self.master = window.root
        self.master_h = window.height #675
        self.master_w = window.width #1024

    def show(self):
        pass

    def destroy(self):
        for f in self.frames:
            f.pack_forget() #.destroy() breaks the program


class SetUpScreen(Screen):
    """
    Initial game screen. Sets the game's configuration (height of the grid,
    width of the grid and number of mines).
    """

    def __init__(self, window):
        super().__init__(window)

        self.frm_options = tk.Frame(self.master,
                                    bg=self.master["bg"],
                                    height=550, width=self.master_w)
        self.frm_play = tk.Frame(self.master,
                                bg=self.master["bg"],
                                height=125, width=self.master_w)

        self.frames = [self.frm_options, self.frm_play]

        self.height_option = SetUpOption(self.frm_options, "HEIGHT", 4, 20)
        self.width_option = SetUpOption(self.frm_options, "WIDTH", 4, 20)
        self.mines_option = SetUpOption(self.frm_options, "MINES", 2, 6)

        self.but_play = tk.Button(self.frm_play,
                                  text="PLAY", font=("Ubuntu Mono", 50, "bold"),
                                  highlightbackground="black", highlightthickness=5,
                                  bg="#17c651", activebackground="#65c680")

        for opt in [self.height_option, self.width_option]:
            for wid in [opt.ent, opt.but_minus, opt.but_plus]:
                wid.bind("<FocusOut>", self.correctMinesLimits)
                wid.bind("<Leave>", self.correctMinesLimits)

        self.options = [self.height_option, self.width_option, self.mines_option]

    def show(self):
        self.frm_options.pack()
        self.frm_play.pack()

        self.height_option.lab_name.grid(row=0, column=0,
                                         padx=(50, 10), pady=(75, 10))
        self.height_option.ent.grid(row=0, column=1,
                                    padx=(10, 2), pady=(75, 10))
        self.height_option.but_minus.grid(row=0, column=2,
                                          padx=(2, 2), pady=(75, 10),
                                          ipadx=8)
        self.height_option.but_plus.grid(row=0, column=3,
                                         padx=(2, 20), pady=(75, 10),
                                         ipadx=8)
        self.height_option.lab_limits.grid(row=0, column=4,
                                           padx=(20, 0), pady=(75, 10))

        self.width_option.lab_name.grid(row=1, column=0,
                                        padx=(50, 10), pady=(10, 45))
        self.width_option.ent.grid(row=1, column=1,
                                   padx=(10, 5), pady=(10, 45))
        self.width_option.but_minus.grid(row=1, column=2,
                                         padx=(5, 1), pady=(10, 45),
                                         ipadx=8)
        self.width_option.but_plus.grid(row=1, column=3,
                                        padx=(1, 20), pady=(10, 45),
                                        ipadx=8)
        self.width_option.lab_limits.grid(row=1, column=4,
                                          padx=(20, 0), pady=(10, 45))

        self.mines_option.lab_name.grid(row=2, column=0,
                                        padx=(50, 10), pady=(45, 0))
        self.mines_option.ent.grid(row=2, column=1,
                                   padx=(10, 2), pady=(45, 0))
        self.mines_option.but_minus.grid(row=2, column=2,
                                         padx=(2, 0), pady=(45, 0),
                                         ipadx=8)
        self.mines_option.but_plus.grid(row=2, column=3,
                                        padx=(0, 20), pady=(45, 0),
                                        ipadx=8)
        self.mines_option.lab_limits.grid(row=2, column=4,
                                          padx=(20, 0), pady=(45, 0))

        self.but_play.grid(row=0, column=0,
                           pady=(100, 0))

    def correctMinesLimits(self, event):
        h = self.height_option
        w = self.width_option
        if h.ent.get().isdigit() and h.mini <= int(h.ent.get()) <= h.maxi \
           and w.ent.get().isdigit() and h.mini <= int(w.ent.get()) <= w.maxi:
            h = int(h.ent.get())
            w = int(w.ent.get())
            self.mines_option.setMini(round(max(2, h*w * 1/12)))
            self.mines_option.setMaxi(round(min(h*w - 10, h*w * 5/6)))


class SetUpOption:
    """
    Class that contains 5 objects (tkinter widgets):
    name, entry, minus button, plus button and limits label.
    Also has code to manage these objects and theirs values.
    Created inside the first frame of the SetUpScreen.
    """

    def __init__(self, master, name, mini, maxi):
        self.master = master
        self.name = name
        self.mini = mini
        self.maxi = maxi

        self.lab_name = tk.Label(self.master,
                                 text=name, font=("Ubuntu Mono", 60, "bold"),
                                 bg=master["bg"])

        self.ent = tk.Entry(self.master,
                            width=3,
                            highlightbackground="black",
                            highlightthickness=3,
                            font=("Ubuntu Mono", 45, "bold"))
        self.ent.insert(0, mini)

        self.but_minus = tk.Button(self.master,
                                   text="-", font=("Ubuntu Mono", 45, "bold"),
                                   bg="#6fa8dc", activebackground="#9fc5e8",
                                   highlightbackground="black", highlightthickness=2,
                                   command=self.decreaseNumber)
        self.but_plus = tk.Button(self.master,
                                  text="+", font=("Ubuntu Mono", 45, "bold"),
                                  bg="#6fa8dc", activebackground="#9fc5e8",
                                  highlightbackground="black", highlightthickness=2,
                                  command=self.increaseNumber)

        self.lab_limits = tk.Label(self.master,
                                   text="({} - {})".format(mini, maxi),
                                   font=("Ubuntu Mono", 35, "bold"),
                                   bg=master["bg"])

        self.widgets = [self.lab_name, self.ent, self.but_minus,
                        self.but_plus, self.lab_limits]

    def setMini(self, new_mini):
        self.mini = new_mini
        self.lab_limits["text"] = "({} - {})".format(self.mini, self.maxi)

    def setMaxi(self, new_maxi):
        self.maxi = new_maxi
        self.lab_limits["text"] = "({} - {})".format(self.mini, self.maxi)

    def decreaseNumber(self):
        self.ent.focus()
        if self.ent.get().isdigit() \
           and int(self.ent.get()) > self.mini:
            n = int(self.ent.get())
            self.ent.delete(0, "end")
            self.ent.insert(0, int(n)-1)

    def increaseNumber(self):
        self.ent.focus()
        if self.ent.get().isdigit \
           and int(self.ent.get()) < self.maxi:
            n = int(self.ent.get())
            self.ent.delete(0, "end")
            self.ent.insert(0, int(n)+1)


class GameScreen(Screen):
    """
    Main screen of the program.
    Contains the game's grid, a frame to show flag numbers, a frame
    to show the timer of the match, a frame showing the match's state,
    one button to start over/play again and one to return to the SetUpScreen.
    """

    def __init__(self, window):
        super().__init__(window)

        #gridsize:fontsize for button based on grid's sizes
        self.gsize_fsize = {4:100, 5:80, 6:65, 7:55,
                            8:45, 9:40, 10:35, 11:30,
                            12:25, 13:21, 14:18, 15:15,
                            16:12, 17:10, 18:8, 19:7, 20:6}
        #additional left pady for the col=0 buttons based on the grid's width
        #works fine with squared grids, however fails with rectangular ones
        self.w_padyleft = {4:50, 5:40, 6:35, 7:30,
                           8:25, 9:15, 10:0, 11:0,
                           12:0, 13:0, 14:0, 15:0,
                           16:0, 17:0, 18:0, 19:0, 20:0}

        self.frm_grid = tk.Frame(self.master,
                                 width=self.master_w*0.8,
                                 height=self.master_h,
                                 bg=self.master["bg"])

        self.frm_info = tk.Frame(self.master,
                                 width=self.master_w*0.2,
                                 height=self.master_h,
                                 bg=self.master["bg"])

        self.frm_flag = tk.Frame(self.frm_info,
                                 width=self.master_w*0.2,
                                 height=self.master_h*0.2,
                                 bg=self.master["bg"])
        self.lab_flag = tk.Label(self.frm_flag,
                                 width=2, height=1,
                                 font=("Ubuntu Mono", 50),
                                 text="\u2691",
                                 bg=self.master["bg"], fg="black")
        self.lab_n_flags = tk.Label(self.frm_flag,
                                    width=7, height=1,
                                    font=("Ubuntu Mono", 40),
                                    text="000/000",
                                    bg=self.master["bg"])

        self.frm_clock = tk.Frame(self.frm_info,
                                  width=self.master_w*0.2,
                                  height=self.master_h*0.2,
                                  bg=self.master["bg"])
        self.lab_clock = tk.Label(self.frm_clock,
                                  width=2, height=1,
                                  font=("Ubuntu Mono", 55),
                                  text="\u23f1",
                                  bg=self.master["bg"], fg="black")
        self.lab_time = tk.Label(self.frm_clock,
                                 width=5, height=1,
                                 font=("Ubuntu Mono", 40),
                                 text="00:00",
                                 bg=self.master["bg"])

        self.frm_match = tk.Frame(self.frm_info,
                                  width=self.master_w*0.2,
                                  height=self.master_h*0.1,
                                  bg=self.master["bg"])
        self.lab_match = tk.Label(self.frm_match,
                                  width=8, height=1,
                                  font=("Ubuntu Mono", 33, "bold"),
                                  text="WAITING",
                                  bg=self.master["bg"], fg="#f1c232",
                                  highlightbackground="black",
                                  highlightthickness=3)

        self.frm_options = tk.Frame(self.frm_info,
                                    width=self.master_w*0.2,
                                    height=self.master_h*0.2,
                                    bg=self.master["bg"])
        self.but_overagain = tk.Button(self.frm_options,
                                       width=10, height=1,
                                       font=("Ubuntu Mono", 26, "bold"),
                                       bg="#f1c232", fg="black",
                                       highlightbackground="black",
                                       highlightthickness=2,
                                       activebackground="#ffd966")
        self.but_cancel = tk.Button(self.frm_options,
                                    width=10, height=1,
                                    font=("Ubuntu Mono", 26, "bold"),
                                    text="Cancel",
                                    bg="#c63d3d", fg="black",
                                    highlightbackground="black",
                                    highlightthickness=2,
                                    activebackground="#c67474")

        self.frames = [self.frm_grid, self.frm_info]

    def overAgain(self):
        self.destroy()
        self.setNewGame(self.grid.getHeight(), self.grid.getWidth(),
                        self.grid.getNMines())
        self.show()

    def setNewGame(self, height, width, n_mines):
        self.grid = Grid(height, width, n_mines)
        self.time_start = 0 #serve as a control variable too

        self.lab_n_flags["text"] = "0/{}".format(n_mines)
        self.lab_time["text"] = "00:00"
        self.lab_match.config(fg="#f1c232", text="WAITING")
        self.but_overagain.config(bg="#f1c232", activebackground="#ffd966",
                                  text="Start over", command=self.overAgain)

    def show(self):
        self.frm_grid.pack(side="left")
        self.frm_info.pack(side="right")

        fsize = min(self.gsize_fsize[self.grid.getHeight()],
                    + self.gsize_fsize[self.grid.getWidth()])
        for r in range(self.grid.getHeight()):
            for c in range(self.grid.getWidth()):
                b = tk.Button(self.frm_grid,
                              width=2, height=1,
                              font=("Ubuntu Mono", fsize),
                              fg="black", text=" ", activeforeground="black",
                              bg="#6fa8dc", activebackground="#9fc5e8",
                              highlightbackground="black", highlightthickness=2,
                              state="normal")
                padx = (0, 0)
                pady = (0, 0)
                if r == 0:
                    pady = (20, 0)
                elif r == self.grid.getHeight()-1:
                    pady = (0, 20)
                if c == 0:
                    padx = (20+self.w_padyleft[self.grid.getWidth()],
                            0)
                elif c == self.grid.getWidth()-1:
                    padx = (0, 20)
                b.grid(row=r, column=c,
                       padx=padx, pady=pady)
                b.bind("<Button-1>", self.start)
                b.bind("<Button-3>", self.flag)
                self.grid.getSquare(r, c).setButton(b)
        self.frm_flag.pack(pady=(0, 15))
        self.frm_clock.pack(pady=(15, 30))
        self.frm_match.pack(pady=(30, 30))
        self.frm_options.pack(pady=(30, 0))

        self.lab_flag.pack()
        self.lab_n_flags.pack()
        self.lab_clock.pack()
        self.lab_time.pack()
        self.lab_match.pack(padx=2, ipadx=4, ipady=5)
        self.but_overagain.pack(padx=4, pady=(0, 2),
                                ipady=5)
        self.but_cancel.pack(padx=4, pady=(2, 0),
                             ipady=5)

    def updateTime(self):
        time_now = int(monotonic())
        passed = time_now - self.time_start
        m = passed // 60
        s = passed % 60
        m = str(m) if m > 9 else "0" + str(m)
        s = str(s) if s > 9 else "0" + str(s)
        self.lab_time["text"] = m + ":" + s
        self.id_time = self.lab_time.after(995, self.updateTime)

    def start(self, event):
        self.is_start = True

        self.time_start = int(monotonic()) #start time
        self.updateTime()

        self.lab_match.config(fg="black", text="IN GAME")
        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        self.grid.setMines(row, col)

        for r in self.grid.getGrid():
            for sq in r:
                sq.getButton().bind("<Button-1>", self.play)

        self.play(event)

    def play(self, event):
        """
        Called when user clicks the mouse's left button.
        If the square clicked is a flag or is revealed, does nothing.
        If the square is a mine, the player loses, the grid becomes
        disabled and the timer stops.
        If the square is anything else, the game expands the grid from
        this square. Check if, after the expansion, the player wins.
        """

        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]

        if self.grid.getSquare(row, col).getState() == 1 \
           or self.grid.getSquare(row, col).getFlag() == "\u2691" \
           and not self.is_start:
            return #nothing happens

        if self.grid.getSquare(row, col).getValue() == "\u2620": #mine
            self.lab_time.after_cancel(self.id_time)
            self.lab_match.config(fg="#c63d3d", text="YOU LOSE")
            self.but_overagain.config(bg="#17c651", activebackground="#65c680",
                                      text="Play again")
            self.grid.showAll(lose=True)
            self.grid.getSquare(row, col).getButton().config(
                disabledforeground="red")
            return
        else: #normal play
            self.grid.expandPosition(row, col)
            self.updateNFlaggedSquares()
            if self.hadVictory(): #victory
                self.lab_time.after_cancel(self.id_time)
                self.time_start = 0
                self.grid.showAll(win=True)
                self.updateNFlaggedSquares()
                self.lab_match.config(fg="#17c651", text="YOU WIN")
                self.but_overagain.config(bg="#17c651", activebackground="#65c680",
                                          text="Play again")

        if self.is_start:
            self.is_start = False

    def updateNFlaggedSquares(self):
        self.lab_n_flags["text"] = "{}/{}".format(
            self.grid.getNFlaggedSquares(), self.grid.getNMines())

    def flag(self, event):
        """
        Called when player clicks mouse's right button.
        The square must be unrevealed to be flagged.
        If square has no flag, it gets a flag and the number of flagged
        squares increases.
        If square has a flag, it gets a question mark, and the number of
        flagged squares decreases.
        If square has a question mark, it has its flag removed.
        """

        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        if self.grid.getSquare(row, col).getState() == 0:
            f = self.grid.getNFlaggedSquares()
            n = self.grid.getNMines()

            if self.grid.getSquare(row, col).getFlag() == "":
                if f < n:
                    self.grid.getSquare(row, col).setFlag("\u2691")
                    self.grid.addFlaggedSquare()
                else:
                    self.grid.getSquare(row, col).setFlag("?")

            elif self.grid.getSquare(row, col).getFlag() == "\u2691":
                self.grid.getSquare(row, col).setFlag("?")
                self.grid.removeFlaggedSquare()

            elif self.grid.getSquare(row, col).getFlag() == "?":
                self.grid.getSquare(row, col).setFlag("")

            self.updateNFlaggedSquares()

    def hadVictory(self):
        for r in self.grid.getGrid():
            for sq in r:
                if sq.getState() == 0 and sq.getValue() == " ":
                    return False
        return True

    def destroy(self):
        if self.time_start != 0: #game started
            self.lab_time.after_cancel(self.id_time)
        for r in self.grid.getGrid():
            for sq in r:
                sq.getButton().grid_forget()
        super().destroy()

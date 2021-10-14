from tkinter import *
from DotsAndBoxes import *

class Game(Frame):
    def __init__(self, master=None):
        # Setup Canvas and other structures
        super().__init__(master)
        self.master = master
        self.master.title('Dots and Boxes')
        self.frame = Frame(self.master, bg='grey', width=300)
        self.frame.pack(side='top', fill='both', expand=True)
        self.canvas = Canvas(master, width=300, height=400, bg='white')
        self.canvas.pack(side='top', fill='both', expand=True)

        self.create_frame()
        self.font = ('Times', '16', 'bold')
        self.player = self.canvas.create_text(200,10,text=f'Player: 0', fill='Purple', font=self.font)
        self.cpu = self.canvas.create_text(400,10, text=f'AI: 0', fill='Orange', font=self.font)
        self.cpu_first = False

        self.line_ids = dict()
        self.text_ids = dict()

    def create_frame(self):
        Label(self.frame, text='Rows:').pack(side='left', padx=0, fill='both')
        self.entry_rows = Entry(self.frame, width=10)
        self.entry_rows.pack(side='left', padx=0, fill='both')

        Label(self.frame, text='Columns:').pack(side='left', padx=0, fill='both')
        self.entry_cols = Entry(self.frame, width=10)
        self.entry_cols.pack(side='left', padx=0, fill='both')
        
        Label(self.frame, text='Ply:').pack(side='left', padx=0, fill='both')
        self.entry_ply = Entry (self.frame, width=10)
        self.entry_ply.pack(side='left', padx=0, fill='both')
        
        self.button1 = Button(self.frame, text='Begin Game', command=self.get_game_params)
        self.button1.pack(side='top', padx=0, fill='both')

        self.check = Checkbutton(self.frame, text='AI goes first?', command=self.check_button)
        self.check.pack(side='left', padx=0, fill='both')

        self.button2 = Button(self.frame, text='Reset', command=self.reset)
        self.button2.pack(side='top', padx=0, fill='both')

        self.button3 = Button(self.frame, text='Debug', command=self.Debug)
        self.button3.pack(side='top', padx=0, fill='both')    
    def check_button(self):
        self.cpu_first = True
    def get_game_params(self):
        self.start_game(int(self.entry_rows.get()), int(self.entry_cols.get()), int(self.entry_ply.get()))

    def cpu_turn(self):
        move = self.game.cpu_turn()
        print(self.game.grid)
        for id,coord in self.line_ids.items():
            if coord == move:
                self.canvas.itemconfig(id, dash=(), fill='red')
                break
        self.box_complete(self.game.check_grid(player=False), player=False)
    def player_turn(self, event):
        id = event.widget.find_closest(event.x, event.y)
        self.canvas.itemconfig(id, dash=(), fill='red')
        self.game.grid[self.line_ids[id[0]]] = 1
        self.box_complete(self.game.check_grid(player=True), player=True)
        self.cpu_turn()
    def box_complete(self, coords, player=False):
        if coords:
            if player:
                self.canvas.itemconfig(self.text_ids[f'{coords[0]},{coords[1]}'], fill='Purple', font=self.font)
                self.canvas.itemconfig(self.player, text=f'Player: {self.game.player_score}')
            else:
                self.canvas.itemconfig(self.text_ids[f'{coords[0]},{coords[1]}'], fill='Orange', font=self.font)
                self.canvas.itemconfig(self.cpu, text=f'AI: {self.game.cpu_score}')
            if self.game.boxes_complete == self.game.board_size[0] * self.game.board_size[1]:
                if self.game.player_score > self.game.cpu_score:
                    msg = 'Congratulations, you win!'
                else:
                    msg = 'You lose, please try again.'
                popup = Toplevel(self.master)
                popup.wm_title('Game Over!')
                popup.tkraise(self.master)
                Label(popup, text=msg).pack(side='top', fill='x', pady=10)
                Button(popup, text='Close', command = popup.destroy).pack()

    # Reset Canvas
    def reset(self):
        self.canvas.delete('all')
        self.player = self.canvas.create_text(200,10,text=f'Player: 0', fill='Purple', font=self.font)
        self.cpu = self.canvas.create_text(400,10, text=f'AI: 0', fill='Orange', font=self.font)
        self.entry_cols.delete(0)
        self.entry_rows.delete(0)
        self.entry_ply.delete(0)
        self.check.deselect()
        self.cpu_first = False
        
        self.game = None
        self.line_ids = dict()
    def create_board(self):
        H,W = self.game.board_size
        # Position of board on canvas
        if H < 3:
            x,y = 200, 100
        else:
            x,y = 150, 50
        
        # Draw the circles and lines on the canvas. 
        m = 0
        for i in range(H+1):
            n = 0
            for j in range(W+1):
                self.canvas.create_oval(x,y,x+20,y+20,fill='blue')
                self.game.grid.append(0)
                n += 1
                if j != W:
                    # Horizontal Lines
                    horz_id = self.canvas.create_line(x+21,y+10, x+59, y+10, fill='white' )
                    # Keep track of line ids and position on the matrix grid
                    self.line_ids[horz_id] = (m,n)
                    # Add to a matrix to keep track of the game.
                    self.game.grid.append(-1)
                    n += 1
                    # Bind the left click to the line.
                    self.canvas.tag_bind(horz_id, '<ButtonPress-1>', self.player_turn)
                x += 60
            # Adjust position for next row.
            x -= ((W+1) * 60)
            # Matrix indicies 
            m += 1
            if i != H:
                n = 0
            for j in range(W+1):
                if i != H:
                    # Verticle Lines
                    vert_id = self.canvas.create_line(x+10, y+21, x+10, y+59, fill='white' )
                    # Keep track of line ids and position on the matrix grid
                    self.line_ids[vert_id] = (m,n)
                    # Add to a matrix to keep track of the game
                    self.game.grid.append(-1)
                    n += 1
                    # Bind the left click to the line.
                    self.canvas.tag_bind(vert_id, '<ButtonPress-1>', self.player_turn)
                    if j != W:
                        text_id = self.canvas.create_text(x+40, y+40, text=f'{self.game.scores[i,j]}')
                        self.text_ids[f'{i},{j}'] = text_id
                        self.game.grid.append(0)
                        n += 1
                x += 60
            # Adjust position for next row.
            x -= ((W+1) * 60)
            y += 60
            # Matrix indicies
            if i != H:
                m += 1
        # Reshape the grid from array to matrix
        self.game.grid = np.reshape(self.game.grid, (m,n))
    def start_game(self, rows, cols, ply):
        self.game = DotsAndBoxes((rows,cols), ply, self.cpu_first)
        self.create_board()
        if self.cpu_first:
            self.cpu_turn()
    def Debug(self):
        print(self.game)
        print(self.game.grid)
        
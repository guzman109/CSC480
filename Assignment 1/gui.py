from tkinter import *

class Transform_Editor(Frame):
    def __init__(self, master=None):
        # Setup Canvas and other structures
        super().__init__(master)
        self.master = master
        self.master.title('2D Transform Editor')
        self.frame = Frame(self.master, bg='grey', width=3000, height=300)
        self.frame.pack(side='top', fill='both', expand=True)
        self.canvas = Canvas(root, width=3000, height=3000, bg='white')
        self.canvas.pack(side="top", fill="both", expand=True)
        self.create_buttons()
        self.x, self.y = 0,0
        self.poly = None
        # Bind Mouse
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        def create_buttons(self):
            self.button1 = Button(self.frame, text='Draw Rectangle', command=self.draw_polygon)
            self.button1.pack(side='left', padx=10)
            self.button2 = Button(self.frame, text='Clear', command=self.clear_screen)
            self.button2.pack(side='left', padx=10)

            self.button2 = Button(self.frame, text='Perspective', command=self.projective)
            self.button2.pack(side='right', padx=10)
            self.button3 = Button(self.frame, text='Affine', command=self.affine)
            self.button3.pack(side='right', padx=10)
            self.button4 = Button(self.frame, text='Similarity', command=self.similarity)
            self.button4.pack(side='right', padx=10)
            self.button5 = Button(self.frame, text='Rigid', command=self.rigid)
            self.button5.pack(side='right', padx=10)
            self.button6 = Button(self.frame, text='Translation', command=self.translation)
            self.button6.pack(side='right', padx=10)
    # Mouse binding functions
    def on_click(self, event):
        pass
    def on_release(self, event):
        pass
    # Reset Canvas
    def clear_screen(self):
        self.canvas.delete('all')
        self.verts = []
if __name__=='__main__':
    root = Tk()
    app = Transform_Editor(master=root)
    app.mainloop()
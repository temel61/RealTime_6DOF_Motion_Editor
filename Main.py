from tkinter import ttk
import tkinter
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import Tk, PhotoImage
import tkinter.messagebox
from matplotlib.figure import Figure
from tkinter import filedialog
import numpy as np
from tkinter import *
from myCanvas import PathInteractor
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Menu, Button
from tkinter import LEFT, TOP, X, FLAT, RAISED
import struct
import matplotlib
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import  axes3d,Axes3D
from matplotlib import style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


style.use('fivethirtyeight')
gs = gridspec.GridSpec(3, 5)

class App:

    def __init__(self, master):

        global canvas, ax, fig, fig1
        fig = Figure(figsize=(18, 8), dpi=100)
        ax = fig.add_subplot(gs[0, :])

        p = 150

        pos_x = 0.0
        pos_y = 0.0

        def init_stewart_platform():
            # Customize the view angle so it's easier to see that the scatter points lie
            # on the plane y=0
            ax4.set_xlim(-200, 200)
            ax4.set_ylim(-200, 200)
            ax4.set_zlim(0, 300)
            ax4.set_xlabel('X')
            ax4.set_ylabel('Y')
            ax4.set_zlabel('Z')

            update_stewart_platform()

            canvas.draw()

        def temel():
            print("temel61")

        def update_stewart_platform():
            platform_vertice = np.array([[-86 , -100 , p], [86 , -100, p], [130 , -25 , p],
                                         [43, 125, p], [-43, 125, p], [-130, -25, p]])
            base_vertice = np.array([[-43, -125, 0], [43, -125, 0], [130, 25, 0], [86, 100, 0], [-86, 100, 0], [-130, 25, 0]])

            # ax4.scatter3D(platform_vertice[:, 0], platform_vertice[:, 1], platform_vertice[:, 2])

            platform = [[platform_vertice[0], platform_vertice[1], platform_vertice[2], platform_vertice[3],platform_vertice[4], platform_vertice[5]]]
            base = [[base_vertice[0], base_vertice[1], base_vertice[2], base_vertice[3], base_vertice[4], base_vertice[5]]]

            actuators = [
                [base_vertice[0], platform_vertice[0]],
                [base_vertice[1], platform_vertice[1]],
                [base_vertice[2], platform_vertice[2]],
                [base_vertice[3], platform_vertice[3]],
                [base_vertice[4], platform_vertice[4]],
                [base_vertice[5], platform_vertice[5]]
            ]


            ax4.add_collection3d(Poly3DCollection(platform, facecolors='gray', linewidths=1, edgecolors='black'))
            ax4.add_collection3d(Poly3DCollection(base, facecolors='gray', linewidths=1, edgecolors='black'))
            ax4.add_collection3d(Poly3DCollection(actuators, linewidths=3, edgecolors='black'))

            canvas.draw()


        def set_values(fileName):

            verts = []
            codes = []

            Path = mpath.Path
            codes.append(Path.MOVETO)

            x_data, y_data = np.loadtxt(fileName, delimiter=',', unpack=True)

            for x, y in zip(x_data, y_data):
                temp = (x, y)
                verts.append(temp)

            for x in range(len(x_data) - 1):
                codes.append(Path.LINETO)

            path = mpath.Path(verts, codes)

            patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)

            ax.add_patch(patch)

            myPlt1 = PathInteractor(patch)

            canvas.draw()
            fig.show()


        color = "#ffff00"

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.X)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar._message_label.config(background=color)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

        ax4 = fig.add_subplot(gs[1:3, 1:4], projection='3d', aspect='equal')

        slider_x = ttk.Scale(master, from_=-100, to=100, command=update_stewart_platform)
        slider_x.place(x=1500, y=600, width=100, height=50)


        init_stewart_platform()


        def _quit():
            if tkinter.messagebox.askokcancel("Quit", "Do you want to quit ?"):
                root.destroy()
                root.quit()     # stops mainloop

        def save_dat_file(filename):
            show_message("Save File" , "File was saved succesfully")

        def openFile():
            filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Dat Files","*.dat"),("All Files","*.*")))
            if filename:
                set_values(filename)
                #readDatFile(filename)

        def saveFile():
            filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("Dat Files","*.dat"),("All Files","*.*")))
            if filename:
                save_dat_file(filename)

        def show_message(myTitle, myMessage):
            tkinter.messagebox.showinfo(myTitle, myMessage)


        #test = Button(master=root, text="test", command=update_stewart_platform)
        #test.place(x=50, y=100)

        #openFile_button = ttk.Button(master=root, text="Open File", command=openFile)
        #openFile_button.place(x=50, y=150)

        menubar = Menu(root, background='#000000', foreground='white',
                activebackground='#004c99', activeforeground='white')

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0, background='#ffffff', foreground='black',activebackground='#004c99', activeforeground='black')
        filemenu.add_command(label="Open", command=openFile)
        #filemenu.add_command(label="Save", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=_quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0, background='#ffffff', foreground='black',activebackground='#004c99', activeforeground='black')
        #editmenu.add_command(label="Cut", command=hello)
        #editmenu.add_command(label="Copy", command=hello)
        #editmenu.add_command(label="Paste", command=hello)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0, background='#ffffff', foreground='black',activebackground='#004c99', activeforeground='black')
        #helpmenu.add_command(label="About", command=hello)
        menubar.add_cascade(label="Help", menu=helpmenu)

        toolbar = Frame(root, bd=1, relief=RAISED)

        icons_png_file_path = "D:/LOCAL FILES/DOF_Motion_Editor/crystal-clear-icons-by-everaldo/png/"
        icons_icon_file_path = "D:/LOCAL FILES/DOF_Motion_Editor/crystal-clear-icons-by-everaldo/ico/"

        self.img = Image.open("C:/Users/DOF/Desktop/open-file-icon.png")
        eimg = ImageTk.PhotoImage(self.img)

        openFileButton = Button(toolbar, image=eimg, relief=FLAT, command=openFile)
        openFileButton.image = eimg
        openFileButton.pack(side=LEFT, padx=2, pady=2)



        self.img1 = Image.open("C:/Users/DOF/Desktop/dat.png")
        eimg1 = ImageTk.PhotoImage(self.img1)

        saveFileButton = Button(toolbar, image=eimg1, relief=FLAT, command=saveFile)
        saveFileButton.image = eimg1
        saveFileButton.pack(side=LEFT, padx=2, pady=2)



        self.img2 = Image.open("C:/Users/DOF/Desktop/exit.png")
        eimg2 = ImageTk.PhotoImage(self.img2)

        quitButton = Button(toolbar, image=eimg2, relief=FLAT, command=_quit)
        quitButton.image = eimg2
        quitButton.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

        # display the menu
        root.config(menu=menubar)
        root.protocol("WM_DELETE_WINDOW", _quit)


root = Tk()
root.title("DOF Movie Data Editor")

root.iconphoto(root, PhotoImage(file="C:/Users/DOF/Desktop/ts.png"))
width, height = root.winfo_screenwidth()-10, root.winfo_screenheight()-90

root.geometry('%dx%d+0+0' % (width,height))

style = ttk.Style()
style.map("TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')] )

app = App(root)

root.mainloop()
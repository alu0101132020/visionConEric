from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import matplotlib.pyplot as plt
import sys
from statistics  import stdev
from PIL import Image, ImageTk
import sklearn
import math
import os
from main import *

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

master = Tk()

def exitApplication():
    value = messagebox.askquestion("Exit", "Would you like to exit the application?")
    if value == "yes" :
        master.destroy()

def openFile():
    file_path = filedialog.askopenfilename(title="Open File", filetypes=(("Imágenes", "*.jpg"), 
        ("Imágenes", "*.png"), ("Todos los ficheros", "*.*")))
    global img_name
    img_name = file_path.split('/')[-1]
    global img
    img = grayscale_check_and_convertion(file_path)
    displayed_img = ImageTk.PhotoImage(img)
    l=Label(image=displayed_img)
    l.pack()    
    # canvas.create_image(20,20, anchor=NW, image=img) 
    master.mainloop()

def saveOurImage():
    img.save(img_name)

def saveAsOurImage():
    img_name = filedialog.asksaveasfilename(confirmoverwrite=False)
    if (img_name.split('.')[-1] != 'jpg') :
        img_name += '.jpg'
    img.save(img_name)

menuBar=Menu(master)
master.config(menu=menuBar, width=300, height=300)

fileMenu=Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Abrir imagen", command=openFile)
fileMenu.add_command(label="Guardar", command=saveOurImage)
fileMenu.add_command(label="Guardar como...", command=saveAsOurImage)
fileMenu.add_command(label="Cerrar", command=exitApplication)

propertyMenu=Menu(menuBar, tearoff=0)
propertyMenu.add_command(label="Histograma abs.")
propertyMenu.add_command(label="Histograma acc.")
propertyMenu.add_command(label="Brillo")
propertyMenu.add_command(label="Contraste")

editMenu=Menu(menuBar, tearoff=0)
editMenu.add_command(label="Lineal")
editMenu.add_command(label="Gamma")
editMenu.add_command(label="Ecualización")
editMenu.add_command(label="Diferencia")

helpMenu=Menu(menuBar, tearoff=0)
helpMenu.add_command(label="License")
helpMenu.add_command(label="About")

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Properties", menu=propertyMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label="Help", menu=helpMenu)

#create main window
# master.title("VPC")
# # master.iconbitmap("images/ull.ico")
# master.geometry("300x300")





# #make a label for the window
# label1 = tkinter.Label(master, text='Hellooooo')
# # Lay out label
# label1.pack()

# Run forever!
master.mainloop()
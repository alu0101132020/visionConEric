from tkinter import *
import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


master = Tk()

menuBar=Menu(master)
master.config(menu=menuBar, width=300, height=300)

fileMenu=Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Abrir")
fileMenu.add_command(label="Guardar")
fileMenu.add_command(label="Guardar como...")
fileMenu.add_command(label="Cerrar")

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

#create main window
master.title("VPC")
#master.iconbitmap("images/ull.ico")
master.geometry("300x300")





# #make a label for the window
# label1 = tkinter.Label(master, text='Hellooooo')
# # Lay out label
# label1.pack()

# Run forever!
master.mainloop()
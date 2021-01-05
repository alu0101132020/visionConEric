from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
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
    #print('no display found. Using :0.0')
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
    refreshImageVisualization()

def saveOurImage():
    img.save(img_name)

def saveAsOurImage():
    img_name = filedialog.asksaveasfilename(confirmoverwrite=False)
    if (img_name.split('.')[-1] != 'jpg') :
        img_name += '.jpg'
    img.save(img_name)

def refreshImageVisualization() :
    displayed_img = ImageTk.PhotoImage(img)
    l.configure(image=displayed_img)
    l.image = displayed_img
    master.mainloop()

def absoluteHistogram():
    if (img != None):
        show_absolute_histogram(img)

def cumulativeHistogram():
    if (img != None):
        show_accumulative_histogram(img)

def editLineal():
    global img
    if (img != None):
        bright_value = simpledialog.askfloat("Input", "Introduzca el valor del brillo", parent=master)
        contrast_value = simpledialog.askfloat("Input", "Introduzca el valor del contraste", parent=master)
        img = conversion(img, bright_value, contrast_value)
        refreshImageVisualization()

def editGamma():    
    global img
    if (img != None):
        gamma_value = simpledialog.askfloat("Input", "Introduzca el valor de gamma", parent=master)
        img = gamma_correction(img, gamma_value)
        refreshImageVisualization()
        
def editBySections():
    global img
    if (img != None):
        number_of_sections = simpledialog.askinteger("Input", "Introduzca el numero de las secciones", parent=master)
        sections = define_sections(number_of_sections)
        
        if not (len(sections) != number_of_sections) :
            sections.append(255)
            array = y_axis_setter()

            for i in range (number_of_sections) :
                fill_sections_array(i, sections, array)

            img = transformation_by_sections(img, array)
            refreshImageVisualization()
        else:
            error_string = 'Error introduciendo secciones.'
            error_string = "El inicio de la seccion no puede ser mayor que el final de una seccion o el final de una seccion no puede ser mayor que 255"
            messagebox.showinfo(message=error_string, title="Error introduciendo secciones")

        

def define_sections(number_of_sections) :
    sections = [0]
    start_of_section = 0
    for i in range (number_of_sections - 1) :
        string = 'La seccion ' + str(i + 1) + ' empieza en ' + str(start_of_section) + '. ¿Donde quieres que termine?'
        end_of_section = simpledialog.askinteger("Input", string, parent=master)
        if (start_of_section < 255 and start_of_section < end_of_section) :
            sections.append(end_of_section)
            start_of_section = end_of_section
        else:
            break
    return sections

def fill_sections_array(index_start_of_section, sections, array) :
    index_end_of_section = index_start_of_section + 1

    string_start_value = 'Introduce which value from 0 to 255 you want the section [' + str(sections[index_start_of_section]) + ', ' + str(sections[index_end_of_section]) + '] to start: '
    string_end_value = 'Introduce which value from 0 to 255 you want the section [' + str(sections[index_start_of_section]) + ', ' + str(sections[index_end_of_section]) + '] to end: '
    start_value = simpledialog.askinteger("Input", string_start_value, parent=master)
    end_value = simpledialog.askinteger("Input", string_end_value, parent=master)

    y_difference = end_value - start_value
    x_difference = sections[index_end_of_section] - sections[index_start_of_section]
    A = y_difference / x_difference
    B = start_value - A * sections[index_start_of_section]
    j = sections[index_start_of_section]
    while j < sections[index_end_of_section] : 
        value = array[j] * A + B
        if value > 255:
            array[j] = 255
        elif value < 0:
            array[j] = 0
        else:
            array[j] = int(value)
        j += 1 

def editEcualization():
    global img
    if (img != None):
        img = equalize_histogram(img)
        refreshImageVisualization()

menuBar=Menu(master)
master.config(menu=menuBar, width=300, height=300)

fileMenu=Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Abrir imagen", command=openFile)
fileMenu.add_command(label="Guardar", command=saveOurImage)
fileMenu.add_command(label="Guardar como...", command=saveAsOurImage)
fileMenu.add_command(label="Cerrar", command=exitApplication)

propertyMenu=Menu(menuBar, tearoff=0)
propertyMenu.add_command(label="Histograma abs.", command=absoluteHistogram)
propertyMenu.add_command(label="Histograma acc.", command=cumulativeHistogram)
propertyMenu.add_command(label="Brillo")
propertyMenu.add_command(label="Contraste")

editMenu=Menu(menuBar, tearoff=0)
editMenu.add_command(label="Lineal", command=editLineal)
editMenu.add_command(label="Transformacion por tramos", command=editBySections)
editMenu.add_command(label="Gamma", command=editGamma)
editMenu.add_command(label="Ecualización", command=editEcualization)
editMenu.add_command(label="Diferencia")

helpMenu=Menu(menuBar, tearoff=0)
helpMenu.add_command(label="License")
helpMenu.add_command(label="About")

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Properties", menu=propertyMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label="Help", menu=helpMenu)


displayed_img = ImageTk.PhotoImage(Image.open("inicio.jpg"))
l=Label(master, image=displayed_img)
l.pack(side="bottom", fill="both", expand="yes")

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
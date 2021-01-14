from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import webbrowser
import matplotlib.pyplot as plt
import sys
from statistics  import stdev
from functools import partial
from PIL import Image, ImageTk
import sklearn
import math
import os
from processing_functions import *

if os.environ.get('DISPLAY','') == '':
    #print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

master = Tk()

def exit_application():
    value = messagebox.askquestion("Exit", "Would you like to exit the application?")
    if value == "yes" :
        master.destroy()

def open_image():
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=(("Imágenes", "*.jpg"), 
        ("Imágenes", "*.png"), ("Todos los ficheros", "*.*")))
    global img_name
    img_name = file_path.split('/')[-1]
    global img
    img = grayscale_check_and_convertion(file_path)
    refresh_image_visualization()

def open_aux_image():
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=(("Imágenes", "*.jpg"), 
        ("Imágenes", "*.png"), ("Todos los ficheros", "*.*")))
    img_name = file_path.split('/')[-1]
    img = grayscale_check_and_convertion(file_path)
    return img

def save_our_image():
    img.save(img_name)

def save_as_our_image():
    img_name = filedialog.asksaveasfilename(confirmoverwrite=False)
    if (img_name.split('.')[-1] != 'jpg') :
        img_name += '.jpg'
    img.save(img_name)

def refresh_image_visualization() :
    displayed_img = ImageTk.PhotoImage(img)
    l.configure(image=displayed_img)
    l.image = displayed_img
    master.mainloop()

def absolute_histogram():
    if (img != None):
        show_absolute_histogram(img)

def accumulative_histogram():
    if (img != None):
        show_accumulative_histogram(img)

def editLineal():
    global img
    if (img != None):
        bright_value = simpledialog.askfloat("Input", "Introduzca el valor del brillo", parent=master)
        contrast_value = simpledialog.askfloat("Input", "Introduzca el valor del contraste", parent=master)
        img = conversion(img, bright_value, contrast_value)
        refresh_image_visualization()

def edit_gamma():    
    global img
    if (img != None):
        gamma_value = simpledialog.askfloat("Input", "Introduzca el valor de gamma", parent=master)
        img = gamma_correction(img, gamma_value)
        refresh_image_visualization()
        
def edit_by_sections():
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
            refresh_image_visualization()
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

def edit_ecualization():
    global img
    if (img != None):
        img = equalize_histogram(img)
        refresh_image_visualization()

def edit_specify_histogram():
    global img
    if (img != None):
        img2 = open_aux_image()
        img = specify_histogram(img, img2)
        refresh_image_visualization()

def edit_differences_between_images(option = 0):
    global img
    if (img != None):
        img2 = open_aux_image()
        img = differences_between_images(img, img2, option)
        refresh_image_visualization()

def differences_between_images(img1, img2, option=0):
    img3 = img1.copy()
    new_img = img3.load()
    w,h = img3.size
    for i in range(w):
        for j in range(h):
            new_img[i, j] = abs(img1.getpixel((i,j)) - img2.getpixel((i,j)))

    if option == 1:
        show_absolute_histogram(img3)
        threshold_value = simpledialog.askinteger("Input", "Introduce el valor umbral para ver diferencias.", parent=master)
        img3 = img3.convert(mode='RGB')
        for i in range(w):
            for j in range(h):
                if (img3.getpixel((i,j)) > (threshold_value, threshold_value, threshold_value)):
                    img3.putpixel((i,j), (255, 0, 0))
                else:
                    img3.putpixel((i,j), (img1.getpixel((i,j)), img1.getpixel((i,j)), img1.getpixel((i,j))))
    return img3
# --------------------- SEGUNDA PARTE -----------------------

def geom_vertical_mirror():
    global img
    if (img != None):
        img = vertical_mirror(img)
        refresh_image_visualization()

def geom_horizontal_mirror():
    global img
    if (img != None):
        img = horizontal_mirror(img)
        refresh_image_visualization()

def geom_traspose():
    global img
    if (img != None):
        img = traspose(img)
        refresh_image_visualization()

def geom_escalate_percentage():
    global img
    if (img != None):
        img = escalate_percentage(img, 120, 120, 0, 0)
        refresh_image_visualization()

def geom_escalate_dimensions():
    global img
    if (img != None):
        img = escalate_percentage(img, 120, 120, 1, 0)
        refresh_image_visualization()

menuBar=Menu(master)
master.config(menu=menuBar, width=300, height=300)

fileMenu=Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Abrir imagen", command=open_image)
fileMenu.add_command(label="Guardar", command=save_our_image)
fileMenu.add_command(label="Guardar como...", command=save_as_our_image)
fileMenu.add_command(label="Cerrar", command=exit_application)

propertyMenu=Menu(menuBar, tearoff=0)
propertyMenu.add_command(label="Histograma abs.", command=absolute_histogram)
propertyMenu.add_command(label="Histograma acc.", command=accumulative_histogram)
propertyMenu.add_command(label="Brillo")
propertyMenu.add_command(label="Contraste")

editMenu=Menu(menuBar, tearoff=0)
editMenu.add_command(label="Lineal", command=editLineal)
editMenu.add_command(label="Transformacion por tramos", command=edit_by_sections)
editMenu.add_command(label="Gamma", command=edit_gamma)
editMenu.add_command(label="Ecualización", command=edit_ecualization)
editMenu.add_command(label="Especificar hist.", command=edit_specify_histogram)

differenceMenu=Menu(editMenu, tearoff=0)
editMenu.add_cascade(label="Diferencia", menu=differenceMenu)
differenceMenu.add_command(label="Crear imagen diferencia", command=edit_differences_between_images)
differenceMenu.add_command(label="Mostrar diferencias", command=partial(edit_differences_between_images, 1))

helpMenu=Menu(menuBar, tearoff=0)
helpMenu.add_command(label="License")
helpMenu.add_command(label="About")

geometricMenu=Menu(menuBar, tearoff=0)
mirrorMenu=Menu(geometricMenu, tearoff=0)
geometricMenu.add_cascade(label="Espejos", menu=mirrorMenu)
mirrorMenu.add_command(label="Vertical", command=geom_vertical_mirror)
mirrorMenu.add_command(label="Horizontal", command=geom_horizontal_mirror)
mirrorMenu.add_command(label="Traspuesta", command=geom_traspose)

rotateMenu=Menu(geometricMenu, tearoff=0)
geometricMenu.add_cascade(label="Rotacion", menu=rotateMenu)
rotateMenu.add_command(label="90º")
rotateMenu.add_command(label="180º")
rotateMenu.add_command(label="270º")
rotateMenu.add_command(label="...")

scaleMenu=Menu(geometricMenu, tearoff=0)
geometricMenu.add_cascade(label="Escalado", menu=scaleMenu)
scaleMenu.add_command(label="Dimensiones", command=geom_escalate_dimensions)
scaleMenu.add_command(label="Porcentajes", command=geom_escalate_percentage)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Properties", menu=propertyMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label="Op. Geom.", menu=geometricMenu)
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
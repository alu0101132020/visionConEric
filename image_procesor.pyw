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
# import pyautogui

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
        # show_absolute_histogram(img3)
        threshold_value = simpledialog.askinteger("Input", "Introduce el valor umbral para ver diferencias.", parent=master)
        img3 = img3.convert(mode='RGB')
        for i in range(w):
            for j in range(h):
                if (img3.getpixel((i,j)) > (threshold_value, threshold_value, threshold_value)):
                    img3.putpixel((i,j), (255, 0, 0))
                else:
                    img3.putpixel((i,j), (img1.getpixel((i,j)), img1.getpixel((i,j)), img1.getpixel((i,j))))
    return img3
    

def edit_ROI():
    master.bind("<Button 1>", get_origin)
    master.bind("<Button 1>", get_ending)
    print_ROI

def get_origin(eventorigin):
    x_origin = eventorigin.x
    y_origin = eventorigin.y

def get_ending(eventorigin):
    x_ending = eventorigin.x
    y_ending = eventorigin.y

def print_ROI():
    print(x_origin, y_origin, x_ending, y_ending)

def callback(event):
    print("clicked at: ", event.x, event.y)

master.bind("<Button-1>", callback)

def motion(event):   
    print("Mouse position: (%s %s)" % (event.x, event.y))   
    return

def get_brightness_img():
    print(get_bright(img))

def get_contrast_img():
    print(get_contrast(img))

def show_profile_of_image():    
    global img
    if (img != None):
        first_point = [0, 0]
        second_point = [0, 0]
        first_point[0] = simpledialog.askinteger("Input", "Coordenada x del primer punto", parent=master)
        first_point[1] = simpledialog.askinteger("Input", "Coordenada y del primer punto", parent=master)
        second_point[0] = simpledialog.askinteger("Input", "Coordenada x del segundo punto", parent=master)
        second_point[1] = simpledialog.askinteger("Input", "Coordenada y del segundo punto", parent=master)
        img = profile_of_image(img, first_point, second_point)
        refresh_image_visualization()

def profile_of_image(img, first_point, second_point):
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize - 1
    max_y = -sys.maxsize - 1
    for point in [first_point, second_point]:
        if point[0] < min_x:
            min_x = point[0]
        if point[1] < min_y:
            min_y = point [1]
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point [1]
    w, h = img.size
    if (min_x >= 0 and max_x < w) and (min_y >= 0 and max_y < h):
        if first_point[0] < second_point[0]:
            A = second_point[1] - first_point[1] / second_point[0] - first_point[0]
            B = -(first_point[0] * A) + first_point[1]
        else:
            A = first_point[1] - second_point[1] / first_point[0] - second_point[0]
            B = -(first_point[0] * A) + first_point[1]
        histogram_of_profile = []
        histogram_of_profile_derivated = []
        if abs(max_x - min_x) > abs(max_y - min_y):
            i = min_x
            while i < max_x:
                current_pixel = int(i * A + B)
                next_pixel = int((i + 1) * A + B)
                histogram_of_profile.append(img.getpixel((i, current_pixel)))
                histogram_of_profile_derivated.append(img.getpixel((i + 1, next_pixel)) - img.getpixel((i, current_pixel)))     
                # img.putpixel((current_pixel, i), (255))    
                i += 1
        else:
            i = min_y
            while i < max_y:
                current_pixel = int((i - B) / A)
                next_pixel = int(((i + 1) - B) / A)
                histogram_of_profile.append(img.getpixel((current_pixel, i)))
                histogram_of_profile_derivated.append(img.getpixel((next_pixel, i + 1)) - img.getpixel((current_pixel, i)))
                # img.putpixel((current_pixel, i), (255))
                i += 1

        histogram_of_profile_VMP = histogram_of_profile.copy()
        histogram_of_profile_VMP_derivated = histogram_of_profile.copy()
        i = 1
        histogram_of_profile_VMP[0] = int((histogram_of_profile[1] + histogram_of_profile[0]) / 2)
        histogram_of_profile_VMP_derivated[0] = int((histogram_of_profile_derivated[1] + histogram_of_profile_derivated[0]) / 2)
        while i < len(histogram_of_profile) - 1:
            j = i - 1
            summ = 0
            summ_derivated = 0
            while j < i + 1:
                summ += histogram_of_profile[j]
                summ_derivated += histogram_of_profile_derivated[j]
                j += 1
            summ /= 3
            summ_derivated /= 3
            histogram_of_profile_VMP[i] = summ
            histogram_of_profile_VMP_derivated[i] = summ_derivated
            i += 1
        histogram_of_profile_VMP[i] = int((histogram_of_profile[i] + histogram_of_profile[i - 1]) / 2)
        histogram_of_profile_VMP_derivated[i] = int((histogram_of_profile_derivated[i] + histogram_of_profile_derivated[i - 1]) / 2)

        show_histogram_from_list(histogram_of_profile)
        show_histogram_from_list(histogram_of_profile_derivated)
        show_histogram_from_list(histogram_of_profile_VMP)
        show_histogram_from_list(histogram_of_profile_VMP_derivated)
        return img
    else:
        print("Los valores no son válidos.")


# --------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -----------------------

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
        panel = Tk()
        panel.title("Introduzca los valores")
        panel.geometry("250x250")
        # panel.iconbitmap('C:/Users/ericf/Desktop/ULL/VPC/visionConEric/ull.ico')
        img = escalate_percentage(img, 80, 80, 0)
        refresh_image_visualization()

def geom_escalate_dimensions():
    global img
    if (img != None):
        img = escalate_dimensions(img, 120, 120, 0)
        refresh_image_visualization()

def geom_rotate(times=0):
    global img
    if (img != None):
        for i in range(times):
            img = rotate_img(img)
        refresh_image_visualization()

def geom_freestyle_420_xXx_rotation():
    global img
    if (img != None):
        img = rotate_freestyle_img(img, 211)
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
propertyMenu.add_command(label="Brillo", command=get_brightness_img)
propertyMenu.add_command(label="Contraste", command=get_contrast_img)

editMenu=Menu(menuBar, tearoff=0)
editMenu.add_command(label="Lineal", command=editLineal)
editMenu.add_command(label="Transformacion por tramos", command=edit_by_sections)
editMenu.add_command(label="Gamma", command=edit_gamma)
editMenu.add_command(label="Ecualización", command=edit_ecualization)
editMenu.add_command(label="Especificar hist.", command=edit_specify_histogram)
editMenu.add_command(label="Region de Interes", command=edit_ROI)

differenceMenu=Menu(editMenu, tearoff=0)
editMenu.add_cascade(label="Diferencia", menu=differenceMenu)
differenceMenu.add_command(label="Crear imagen diferencia", command=edit_differences_between_images)
differenceMenu.add_command(label="Mostrar diferencias", command=partial(edit_differences_between_images, 1))

showMenu=Menu(menuBar, tearoff=0)
showMenu.add_command(label="Zona de interes")
showMenu.add_command(label="Perfil", command=show_profile_of_image)


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
rotateMenu.add_command(label="90º", command=partial(geom_rotate, 1))
rotateMenu.add_command(label="180º", command=partial(geom_rotate, 2))
rotateMenu.add_command(label="270º", command=partial(geom_rotate, 3))
rotateMenu.add_command(label="...", command=geom_freestyle_420_xXx_rotation)

scaleMenu=Menu(geometricMenu, tearoff=0)
geometricMenu.add_cascade(label="Escalado", menu=scaleMenu)
scaleMenu.add_command(label="Dimensiones", command=geom_escalate_dimensions)
scaleMenu.add_command(label="Porcentajes", command=geom_escalate_percentage)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Properties", menu=propertyMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label="Op. Geom.", menu=geometricMenu)
menuBar.add_cascade(label="Show", menu=showMenu)
menuBar.add_cascade(label="Help", menu=helpMenu)


displayed_img = ImageTk.PhotoImage(Image.open("inicio.jpg"))
l=Label(master, image=displayed_img)
l.pack(side="bottom", fill="both", expand="yes")
# l.bind('<Motion>',motion)
x_origin = 0
y_origin = 0
x_ending = 0
y_ending = 0
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
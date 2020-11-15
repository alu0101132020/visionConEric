package com.company;

import java.io.File;
import java.io.IOException;
import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;


public class MyImage {

    public static void main(String[] args) throws IOException {
        int width = 963;
        int height = 640;
        BufferedImage myPicture = null;
        File f = null;
        try {
            f = new File ("./imagenes-de-prueba/arbol_gris.jpg");
            myPicture = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);
            myPicture = ImageIO.read(f);
            System.out.println("Reading complete.");
        } catch (IOException e) {
            System.out.println("Error: " + e);
        }

        // Código para dar de salida una imagen.
        // try {
        //     f = new File("./imagenes-de-prueba/salida.jpg");
        //     ImageIO.write(myPicture, "jpg", f);
        //     System.out.println("Writing complete.");
        // } catch (IOException e) {
        //     System.out.println("Error: " + e);
        // }
    }

}
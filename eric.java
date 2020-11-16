package com.company;


import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.io.*;
import javax.imageio.*;
import javax.swing.*;
import java.awt.image.BufferedImage;

public class ProcesamientoImagen {
    ;

    public static void main(String[] args) throws IOException {
        BufferedImage img = ImageIO.read(new File("test.png"));
 
        BufferedImage bwimg = Imagen(img);
 
        ImageIO.write(bwimg, "png", new File("example-bw.png"));
    }

    public static BufferedImage Imagen (BufferedImage _image){
        BufferedImage imagen = _image;
        int width = _image.getWidth();
        int height = _image.getHeight();
        int[] histogramaAbsoluto = new int[255];
        int[] histogramaAcumulativo = new int[255];

        histogramaAbsoluto = computeHistogram(imagen);
        histogramaAcumulativo = computeAccHistogram(histogramaAbsoluto);

        System.out.println(histogramaAbsoluto);
        
        int l = histogramaAbsoluto.length;
        
        for (int i = 0; i < histogramaAbsoluto.length; i++)
            System.out.println(histogramaAbsoluto[i]);
        
        return imagen;
    }


    private static int luminance(int rgb) {
        int r = (rgb >> 16) & 0xFF;
        int g = (rgb >> 8) & 0xFF;
        int b = rgb & 0xFF;
        return (r + b + g) / 3;
    }

    private static int[] computeHistogram(BufferedImage img) {
        int width = img.getWidth();
        int height = img.getHeight();
 
        int[] histo = new int[256];

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                histo[luminance(img.getRGB(x, y))]++;
            }
        }

        return histo;
    }

    private static int[] computeAccHistogram(int[] histo_abs) {
        int[] histo = new int[256];

        histo[0] = histo_abs[0];

        for (int i = 1; i < histo_abs.length; i++) {
                histo[i] = histo_abs[i] + histo[i-1] ;
        }

        return histo;
    }
}
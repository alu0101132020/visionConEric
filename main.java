package com.company;

import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;


public class Myclass {
    // public class Image {
    //     private final BufferedImage image;
    //     private final int[] histogramaAbsoluto = new int[255];
    //     private final int[] histogramaAcumulativo = new int[255];

    //     public Image(BufferedImage image) {
    //         this.image = image;
    //     }
    // }

    public static void main(String[] args) {
        String imagePath = "imagenes-de-prueba/arbol_gris.jpg";
        BufferedImage myPicture = ImageIO.read(new File(imagePath));
        Graphics2D g = (Graphics2D) myPicture.getGraphics();
        g.setStroke(new BasicStroke(3));
        g.setColor(Color.BLUE);
        g.drawRect(10, 10, myPicture.getWidth() - 20, myPicture.getHeight() - 20);
        JLabel picLabel = new JLabel(new ImageIcon(myPicture));
        JPanel jPanel = new JPanel();
        jPanel.add(picLabel);
        JFrame f = new JFrame();
        f.setSize(new Dimension(myPicture.getWidth(), myPicture.getHeight()));
        f.add(jPanel);
        f.setVisible(true);
    }
}
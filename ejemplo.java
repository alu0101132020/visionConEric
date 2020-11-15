import javax.swing.JFrame;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

public class ShowImage extends JFrame{
    private static BufferedImage image = null;
    // Stores image
    public void paint(Graphics g){
        super.paint(g);
        g.drawImage( image, 5, 35, null); // Draws the image
        // Upper left corner at 5,35 (avoid drawing over border)
    }
    public ShowImage(){
        setSize(810, 645);  
        // Size of the window in pixels
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
    }
    //-----------------------------------------------------------
    /*** Main method.  You have to add the "throws Exception" at*
     *  the end here.  Later we will see a better way to do this* 
     * using "try" and "catch".*/
    public static void main(String[] args) throws Exception{
        ShowImage myWindow = new ShowImage();
        // These next two lines read the image from the file
        File input = new File("./imagenes-de-prueba/pokemon.jpg");
        image = ImageIO.read(input);
        myWindow.repaint();
    }
}
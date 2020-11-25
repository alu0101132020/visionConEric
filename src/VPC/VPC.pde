PImage foto;

void setup() {
  foto = loadImage("../assets/arbol.jpg");
  size(1000, 1000);
  background(0);
}

void draw() {
  loadPixels();
  for (int x = 0; x < foto.width; x++) {
    for (int y = 0; y < foto.height; y++) {
      int posicion = x + y * foto.width;
      float red = red(foto.pixels[posicion]);
      float blue = blue(foto.pixels[posicion]);
      float green = green(foto.pixels[posicion]);
      pixels[x + y * width] = color((red + green + blue)/ 3);
    }
  }
  updatePixels();
}

void count () {
  for (int x = 0; x < foto.width; x++) {
    for (int y = 0; y < foto.height; y++) {
      int posicion = x+y*foto.width;
      text("a", 20, 20, width-40, height-40);
      }
  }
}

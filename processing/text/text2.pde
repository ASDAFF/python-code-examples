// An array of news headlines
String[] headlines = {
  "Processing downloads break downloading record.", 
  "New study shows computer programming lowers cholesterol.",
  };

PFont f;  // Global font variable
float x,y,z;  // horizontal location of headline
int index = 0;

void setup() {
  size(400,200);
  f = createFont("Arial",16,true);  
  // Initialize headline offscreen to the right 
  x = width; 
  y = random(height);
  z = random(height);
  color c = color(0, 126, 255, 102);

}

void draw() {
  background(255);
  fill(0);

  // Display headline at x  location
  textFont(f,16);        
  textAlign(LEFT);

  text(headlines[index],x,y,z); 

  // Decrement x
  x = x - 3;
  // If x is less than the negative width, 
  // then it is off the screen
  float w = textWidth(headlines[index]);
  if (x < -w) {
    x = width; 
    index = (index + 1) % headlines.length;
      y = random(height);
  }
  //saveFrame();
}



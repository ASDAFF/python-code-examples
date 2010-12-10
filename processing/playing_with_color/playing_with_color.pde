size(300, 300);
float stepsize;
// Before we deal with pixels
loadPixels();  
stepsize = 6;
// Loop through every pixel
for (int i = 0; i < pixels.length; i++) {
  // Pick a random number, 0 to 255
  //float rand = random(255) , random(255) , random(255),random(255)) ;
  // Create a grayscale color based on random number
//  color c = color(random(255),random(255),random(255));
color c = color(random(255 * i / pixels.length) , (255 * i / pixels.length) , random(255 * (pixels.length - i) / pixels.length));
  // Set pixel at that location to random color
  pixels[i] = c;
  //pixels[i] = c;
}
for (int i = 0; i < pixels.length; i++) {
color c = color(255);
  if (i % stepsize == 0){
   if (random(5000)<5 ) {
     stepsize = stepsize +1 ;
   }
      c = color((255 - (255 * i / pixels.length )));  
      pixels[i] = c;
}
}

// When we are finished dealing with pixels
updatePixels();

float numFrames = 50;
float csize = 200;
float thismouseX;
void setup() {
  size(480, 120);
  smooth();
}

void draw() {
  if (mousePressed) {
    fill(200);
  } else {
    fill(255);
  }
  ellipse(mouseX, mouseY, csize, csize);

  if (mouseX != thismouseX){
      csize = csize  - 1;
      thismouseX = mouseX;
  }
  if(csize <20){
    csize = 200;
  }
}


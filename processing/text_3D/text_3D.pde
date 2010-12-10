// An array of news headlines
String[] headlines = {
"Newcastle   ","Norwich ","Nice ","Paris ","Rennes ","Rome","Shannon  ","Strasbourg ","Toulouse ","Valencia",
"Vienna ","Bangkok ","Durban  ","Buffalo","Charlotte","Chicago","Cincinnati","Cleveland","Columbus",
"Dallas Forth Worth ","Halifax","Honolulu","Houston","Las Vegas","Los Angeles","Maui","Miami","Montreal",
"New York JFK","Newark","Orlando","Philadelphia","Pittsburgh","Portland","Raleigh Durham","Seattle",
"Toronto","Torrance","Washington Dulles",
"Aberdeen","Alicante","Amsterdam","Barcelona","Belfast","Bilbao","Birmingham","Bordeau","Bristol","Brussels",
"Copenhagen","Cork","Dublin","East Midlands","Edinburgh","Frankfurt","Glasgow","Leeds-Bradford","Lille",
"London","Lyon ","Madrid ","Manchester  ","Marseille  ","Milano ","Montpellier  ","Mulhouse ","Nantes"
  };

PFont f;  // Global font variable
float x,y,rotation,z,alphaValue,alphaincrement,starttime, outTime ,speed;  // horizontal location of headline
int index = 0;
boolean   done;

void setup() {
  size(640,416,P3D);
  f = createFont("Synchro LET",(height/5),true);  
  // Initialize headline offscreen to the right 
  x = 00; 
  z = 0;
  speed = 3;
  done = false;
  outTime = 1700;
  alphaValue = 1;
  starttime = millis();
  alphaincrement = 10;
  y = random(height);
  rotation = 30;
  color c = color(0, 126, 255, 102);
}

void draw() {
  background(255);
  fill(0);
  // Display headline at x  location
  textFont(f,(height/5.5));        
  textAlign(LEFT);

rotateY(radians(rotation));
  alphaValue = alphaValue + alphaincrement;
  fill(255,0,0, alphaValue);
  text(headlines[index],x,y,z); 
  float w = textWidth(headlines[index]);

if  (millis() - starttime > outTime){
       alphaincrement = -10;
 }
 if (alphaValue <10){
  done = true;
 }

  x = x + speed;

  // If x is less than the negative width, 
  // then it is off the screen

  if (done == true) {
    x = 0;
    index = (index + 1) % headlines.length;
      y =  random(height/2) + (height/4);
      rotation = random(40)-20;
      starttime = millis();  
      alphaValue = 1;
      speed = (random(40)/10 ) +1.7;
      if (random(2)>1){
        speed= -1 * speed;
      }
      z = 0;
      if(speed<0){
      x = width- 50 - random(40); 
      }
      done = false;
      alphaincrement = 10;
      outTime = (width/200) * (1200+ (30* random(30)));
  }
  saveFrame();
}

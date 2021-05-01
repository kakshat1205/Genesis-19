#include<Servo.h>

Servo s1;
Servo s2;
Servo pen;
int q = 1;
double angle1, angle2;      //ANGLE1--base servo(8-160)  ANGLE2--joint servo(1-142)- calibration.
float a1 = 15, a2 = 17.2, x, y; //link lengths a1 and a2 
int c = 1;
int iangle1, iangle2;     //target angles
int diff1, diff2;
void sweep(int, int);     //function for smooth change of angles
 
int xangle1, xangle2;     //current state
void setup()
{
  Serial.begin(9600);

  angle1 = 90; //initial angle values
  angle2 = 0;
  xangle1 = 90;
  xangle2 = 0;
  angle1=map(angle1,0,180,4,164);                      //servo calibration
  angle2=map(angle2,0,180,20,180);
  //angle1 = (angle1 / 180) * 150 + 10;
  //angle2 = (angle2 / 180) * 152 + 0;
  s1.attach(10);
  s2.attach(11);
  pen.attach(9);
  s1.write(angle1);
  s2.write(angle2);                                    //writing initial angles
  pen.write(100);
}

void loop() {
  if (Serial.available() > 0)
  {
    x = Serial.readStringUntil(' ').toFloat();           //recieving values from python code
    y = Serial.readStringUntil('\n').toFloat();
    Serial.println(x);
    Serial.println(y);
    //x=600-x;
    // x = map(x, 0, 600, -22, -3.8); 
    //y = map(y, 0, 600, 3.8, 21.2);
    y = ((y / 600) * 18.5) + 3.5;                        //mapping according to A4
    x = -(22 - ((x / 600) * 18.5 ));
    Serial.print(angle1);
    Serial.println(y);
    angle2 = acos((x * x + y * y - a1 * a1 - a2 * a2) / (2 * a1 * a2));        //INVERSE KINEMATICS FOR ANGLE 2(END EFFECTOR)      
    angle1 = atan(y / x) - atan((a2 * sin(angle2)) / (a1 + a2 * cos(angle2))); //INVERSE KINEMATICS FOR ANGLE 1(BASE)
    if (angle1 < 0)
    { angle1 += 3.14;
    }
    angle1 = angle1 * 57.2957795;
    angle2 = angle2 * 57.2957795;
    Serial.print(angle1);
    Serial.print(angle2);
    sweep(angle1, angle2);
    pen.write(30);
  }
}

void sweep(int iangle1, int iangle2)
{ //Serial.println("sweep");
  if (xangle1 > iangle1)
  {
    diff1 = 0;
  }
  else
  {
    diff1 = 1;
  }
  if (xangle2 > iangle2)
  {
    diff2 = 0;
  }
  else {
    diff2 = 1;
  }
  int i = xangle1;
  int j = xangle2;
  while (!((i == iangle1) && (j == iangle2)))
  {

    if (diff1 == 0 && diff2 == 0)
    {
      if (i-iangle1 > q) {
        i -= q;
      }
      else{i=iangle1;}
      if (j-iangle2 > q) {
        j -= q;
      }
      else{j=iangle2;}
    }
    if (diff1 == 0 && diff2 == 1) {
      if (i -iangle1>q ) {
        i -= q;
      }
      else{i=iangle1;}
      if (iangle2-j > q) {
        j += q;
      }
      else{j=iangle2;}
    }
    if (diff1 == 1 && diff2 == 0)
    {
      if (iangle1-i > q) {
        i += q;
      }
      else{i=iangle1;}
      if (j-iangle2 > q) {
        j -= q;
      }
      else{j=iangle2;}
    }
    if (diff1 == 1 && diff2 == 1) {
      if (iangle1-i > q) {
        i += q;
      }
      else{i=iangle1;}
      if (iangle2-j > q) {
        j += q;
      }
      else{j=iangle2;}
    }
    int i1 = i;
    int j1 = j;
    i1=map(i1,0,180,4,164);
  j1=map(j1,0,180,20,180);
    //i1 = (i1 / 180) * 150 + 10;
    //j1 = (j1 g/ 180) * 152 + 0;
    s1.write(i1);
    s2.write(j1);
    Serial.println(i);
    Serial.println(j);
    delay(10);
  }
  xangle1 = iangle1;
  xangle2 = iangle2;
}

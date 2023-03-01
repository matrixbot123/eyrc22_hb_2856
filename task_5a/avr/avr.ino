#include "AccelStepper.h"
#include "MultiStepper.h"
#define PI 3.1415

const int w1dpin = 6;
const int w2dpin = 10;
const int w3dpin = 8;
const int w1spin = 7;
const int w2spin = 11;
const int w3spin = 9;
const int stepsPerRevolution = 200;
const int rad = 3;//in cms
const float timeQuanta = 0.04f;//NOT VALID NEEDS TO BE CHANGED

volatile float elapsedTime = 0;
static int vx, vy, w;

int theta = PI/3;
int gspeed = 300;

AccelStepper motor1(AccelStepper::DRIVER, w1spin, w1dpin);
AccelStepper motor2(AccelStepper::DRIVER, w2spin, w2dpin);
AccelStepper motor3(AccelStepper::DRIVER, w3spin, w3dpin);
MultiStepper robot;
String recvdata = "";

//for debug
int r = 6;
int g = 7;
int b = 8;
int tmp = 1;
//for debug
void changecol(){

    if(tmp==1){                         //If data is even, turn on Blue LED
      analogWrite(r,255);
      analogWrite(g,0);
    }
    else{                                //If data is odd, turn on Red LED
      analogWrite(r,0);
      analogWrite(g,255);
    }
    tmp = 1 - tmp;
}

ISR(TIMER1_COMPA_vect)        // interrupt service routine 
{
  elapsedTime += timeQuanta;

  motor1.runSpeed();
  motor2.runSpeed();
  motor3.runSpeed();
}


void setup()
{
  Serial.begin(115200);
  
  cli();
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  OCR1A = 625;// = (16*10^6) / (5*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 8 prescaler
  TCCR1B |= (1 << CS11);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  sei();             
  
  motor1.setMaxSpeed(1000);
  motor2.setMaxSpeed(1000);
  motor3.setMaxSpeed(1000);
  analogWrite(r,0);
  analogWrite(g,255);
  analogWrite(b,255);
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  
}

void setvel(int w, int x, int y, float t) {
  int d = 1;
  long vf = -d*w + x;
  long vr = (long)(-d*w + (double)-cos(theta)*x + (double)-sin(theta)*y);
  long vl = (long)(-d*w + (double)-cos(theta)*x + (double)sin(theta)*y);

  motor1.setSpeed(vf);
  motor2.setSpeed(vr);
  motor3.setSpeed(vl);
  float tmpTime = elapsedTime;
  while( elapsedTime < (tmpTime + t) )
    {
      motor1.runSpeed();
      motor2.runSpeed();
      motor3.runSpeed();
    }
    
}

void setvelcont(int w, int x, int y) {
  int d = 1;
  long vf = -d*w + x;
  long vr = (long)(-d*w + (double)-cos(theta)*x + (double)-sin(theta)*y);
  long vl = (long)(-d*w + (double)-cos(theta)*x + (double)sin(theta)*y);

  motor1.setSpeed(vf);
  motor2.setSpeed(vr);
  motor3.setSpeed(vl);
}

void makeL() {
  int speed = 200;
  setvel(0, 0, speed, 3);
  delay(1000);
  setvel(0, 0, -speed, 3);
  delay(1000);
  setvel(0, speed, 0, 3);
  delay(1000);
  setvel(0, -speed, 0, 3);
  delay(1000); 
}

void makeTriangle() {
  int speed = 300;
  float sin60 = sqrt(3)/2;
  setvel(0, 0, speed, 3);
  delay(1000);
  setvel(0, speed*sin60, -speed/2, 3);
  delay(1000);
  setvel(0, -speed*sin60, -speed/2, 3);
  delay(1000);
}

void makeCircle() {
  int nst = 200;
  float noS = 2*PI/nst;
  double cnos = cos(noS);
  double snos  = sin(noS);
  
  float xs[nst], ys[nst];

  xs[0] = 300;
  ys[0] = 0;
  
  for(int i = 1; i<nst ;i++) {
    xs[i] = xs[i-1] * cnos + -ys[i-1] * snos;
    ys[i] = xs[i-1] * snos + ys[i-1] * cnos;
  }

  int ctr = 0;
  while(ctr<nst) {
    setvel(0, xs[ctr%nst], ys[ctr%nst], timeQuanta);
    Serial.print(xs[ctr]);
    Serial.print(", ");
    Serial.println(ys[ctr]);
    ctr++;
  }
  
}

void loop_old() {
    delay(2000);
    makeL();
    delay(2000);
    makeTriangle();
    delay(2000);
    makeCircle();
}
void loop() {
  
  if (Serial.available()) {
    vx = Serial.readStringUntil(' ').toInt();
    vy = Serial.readStringUntil(' ').toInt();
    w = Serial.readStringUntil('\n').toInt();

    //changecol();
    setvelcont(w, vx, vy);
  }
}

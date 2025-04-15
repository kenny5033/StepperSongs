/*Make Music With Stepper Motors! By Whiteshadow11 https://www.instructables.com/Make-Music-With-Stepper-Motors/*/

//Next steps are implementing serial communication to Raspberry Pi


// Define Pins
const int stepPin = 4; 
const int dirPin = 3; 

//Setting Frequency to match piano keys
int coun;
bool dir=0;
int del;
int c=1912;
int cf=1805;
int d= 1703;
int df=1607;
int e=1517;
int f=1431;
int ff=1351;
int g= 1275;
int gf=1203;
//int a = 1760; //original
int a=1136;
int af=1072;
int b=1012;
int c1=floor(c/2);
int cf1=floor(cf/2);
int d1=floor(d/2);
int df1=floor(df/2);
int e1=floor(e/2);
int f1=floor(1431/2);
int ff1=floor(1351/2);
int g1= floor(1275/2);
int gf1=floor(1203/2);
int a1=floor(1136/2);
int af1=floor(1072/2);
int b1=floor(1012/2);
int e0=e*2;
int g0=g*2;
int b0=b*2;
int af0=af*2;
int a0=a*2;
int f0=f*2;
int use = 300;
int use2=180;
int tempo=120;
int oct=5;

void setup() {
  //Step and Direction pins, DRV8825 has 2 other pins set to high (5V) directly from source
  //Other Drivers need to have different pin sets ups but still use STEP and DIR in the same methond
  //Will stick with DRV8825 drivers since they produce the least amount of non-needed noise
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
}
void loop() {
  oct=5;
  ////Testing notes at different lengths
  // note(e1,250);
  // note(e1,500);
  // note(e1,250);
  // pa(250);
  // note(c1,250);
  // note(e1,500);
  // note(g1,1000);
  // note(g,1000);
  // note(c1,500);
  // pa(250);
  // note(g,250);
  // pa(500);
  // note(e,500);
  // pa(250);
  // note(a,250);
  // pa(250);
  // note(b,250);
  // pa(250);
  // note(af,250);
  // note(a,500);
  // note(g,330);
  // note(e1,330);
  // note(g1,330);
  // note(a1,500);
  // note(f1,250);
  // note(g1,250);
  // pa(250);
  // note(e1,250);
  // pa(250);
  // note(c1,250);
  // note(d1,250);
  // note(b,250);
  // pa(1000);
  //twinkle twinkle star
  for (int i = 0; i < 4; i++) {
    note(c, 100);
    pa(use);
    note(c, 100);
    pa(use);
    note(g, 100);
    pa(use);
    note(g, 100);
    pa(use);
    note(a, 100);
    pa(use);
    note(a, 100);
    pa(use);
    note(g, 100);
    pa(500);

    note(f, 100);
    pa(use);
    note(f, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(d, 100);
    pa(use);
    note(d, 100);
    pa(use);
    note(c, 100);
    pa(500);

    note(g, 100);
    pa(use);
    note(g, 100);
    pa(use);
    note(f, 100);
    pa(use);
    note(f, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(d, 100);
    pa(500);

    note(g, 100);
    pa(use);
    note(g, 100);
    pa(use);
    note(f, 100);
    pa(use);
    note(f, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(e, 100);
    pa(use);
    note(d, 100);
    pa(1000);
  }
  //Rob scallon Rain.
  for (int i = 0; i < 3; i++){
    note(d,100);
    pa(use2);
    note(f,100);
    pa(use2);
    note(c1,100);
    pa(use2);
    note(f,100);
    pa(use2);}
    note(c1,100);
    pa(use2);
    note(c1,100);
    pa(use2);
    note(af,100);
    pa(use2);
    note(a,100);
    pa(use2);
  for (int i = 0; i < 3; i++){
    note(c,100);
    pa(use2);
    note(e,100);
    pa(use2);
    note(af,100);
    pa(use2);
    note(e,100);
    pa(use2);}
  note(af,100);
  pa(use2);
  note(af,100);
  pa(use2);
  note(a,100);
  pa(use2);
  note(f,100);
  pa(use2);
  for (int i = 0; i < 3; i++){
    note(d,100);
    pa(use2);
    note(f,100);
    pa(use2);
    note(af,100);
    pa(use2);
    note(f,100);
    pa(use2);}
  for (int i = 0; i < 3; i++){
    note(af0,100);
    pa(use2);
    note(d,100);
    pa(use2);
    note(f,100);
    pa(use2);
    note(a,100);
    pa(use2);}
}

void note(int num,long dur) {
  del=(num*oct)/10;
  dir=!dir;
  digitalWrite(dirPin,dir);
  coun=floor((dur*5*tempo)/del);
  for(int x = 0; x < coun; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(del);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(del);
  }

}

void pa(int durp){
  int ker=floor(durp/100)*tempo;
delay(ker);
  
}
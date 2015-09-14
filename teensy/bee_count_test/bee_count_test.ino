int gs[87];
int currentRead;
int myPins[] = {0,27,2,1,3,4,5,6,7,26,25,24,23,22,19,18,32,28,33,29,34,30,35,21,8,9,10,11,12,13,14,15,16,17,38,39,40,41,42,43,44,45,20,31}; //44

#define arr_len( x )  ( sizeof( x ) / sizeof( *x ) )

int numIR = arr_len(myPins); // 44, 0 to 45 minus 36 and 37
// if you're missing 28-35 it's because you forgot to solder in headers for internal pins
// if you get blank scrolling in the serial monitor, you're probably trying to access a pin you shouldn't be.

void setup() {
  // set pins to input mode
  for (int i = 0; i < numIR; i++) {
    pinMode(myPins[i], INPUT);
  }
  // start serial connection
  Serial.begin(38400);
}

void loop() {
  for(int i = 0; i < numIR; i++) {
    gs[i] = digitalRead(myPins[i]);
    // only print if last value changed, last value initialized to 0
    if(gs[i] != gs[i+numIR]) {
      Serial.print(myPins[i]);
      Serial.print(":");
      Serial.print(gs[i]);
      Serial.print("| ");
      //gs[i+numIR] = gs[i];
    }
  }
  Serial.println();
}

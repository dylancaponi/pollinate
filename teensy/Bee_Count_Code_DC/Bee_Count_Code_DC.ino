
// bee counter for use with bee counter v1.0 instructable by hydronics
// dylan caponi - 2015

int gs[131]; // 22 channels x 2 gates x 2 historic value + 44 ins and outs count for every gate
// 1st pin status, last 1st pin status, 2nd pin status, last 2nd pin status for each gate

int myPins[] = {0,27,2,1,3,4,5,6,7,26,25,24,23,22,20,31,19,18,32,28,33,29,34,30,35,21,8,9,10,11,12,13,14,15,16,17,38,39,40,41,42,43,44,45}; //44

#define arr_len( x )  ( sizeof( x ) / sizeof( *x ) )

int numIR = arr_len(myPins); // 44, 0 to 45 minus 36 and 37
// if you're missing 28-35 it's because you forgot to solder in headers for internal pins
// if you get blank scrolling in the serial monitor, you're probably trying to access a pin you shouldn't be.

// fix - should be defined by size of myPins
int inOuts[44];

// Variables will change:
int ins = 0;  // counts ins and outs
int outs = 0;
int count = 0;
int lcount = 0;
int currentRead;
int inputStatus = 0;
int outputStatus = 0;
int lastInputStatus = 0;
int lastOutputStatus = 0;

void setup() {
  // set pins to input mode
  for (int i = 0; i < numIR; i++) {
    pinMode(myPins[i], INPUT);
  }
  // start serial connection
  Serial.begin(38400);
}
      
void loop() {
  // read digital pins into array
  for(int i = 0; i < numIR; i++) {
    gs[i] = digitalRead(myPins[i]);
  }
  
  // loop through gates and count: 0-44 multiples of 2
  
  // was < numIR trying to find error
  for (int gate = 0; gate < numIR; gate+=2) {
    inputStatus = gs[gate];
    outputStatus = gs[gate+1];
    lastInputStatus = gs[gate+numIR];
    lastOutputStatus = gs[gate+numIR+1];
    
    if (lastInputStatus != inputStatus) {
      if (inputStatus > outputStatus) {
        ins++;
        //gs[gate + numIR * 2 ]+=1; // update gate specific value
        
        // 0 to 42
        inOuts[gate]++;
    }}
    if (lastOutputStatus != outputStatus) {
      if (outputStatus > inputStatus) {
        outs++;
        //gs[gate + numIR * 2 +1]+=1;// update gate specific value
        inOuts[gate+1]++;
    }}   
  }
  // update historic gate status values
  for (int gate = 0; gate < numIR; gate++) {
    gs[gate+numIR] = gs[gate];
  }
  count = ins + outs;
  if (lcount != count){   // if the count has changed we print the new count
//  print out for show
//      Serial.print("number In:  ");
//      Serial.print(ins);
//      Serial.print(" number Out:  ");
//      Serial.print(outs);
      
//      Serial.print(" ch1 ins: ");
//      Serial.print(inOuts[0]);
//      Serial.print(" ch1 outs: ");
//      Serial.println(inOuts[1]);
//      Serial.print(" ch22 ins: ");
//      Serial.print(inOuts[40]);
//      Serial.print(" ch22 outs: ");
//      Serial.print(inOuts[41]);

// print out for serial comm
    Serial.print(ins);
    Serial.print(",");
    Serial.print(outs);
    Serial.print(",");
    
    // goes from 0 to 42 because 44 is more than 43
    for (int gate = 0; gate < numIR; gate+=2) {
      Serial.print(inOuts[gate]);
      Serial.print(",");
      Serial.print(inOuts[gate+1]);
      if (gate != (numIR-2)) {
        Serial.print(",");
      }
    }
    Serial.println();

      lcount = count;
}
  //delay(1000);
}

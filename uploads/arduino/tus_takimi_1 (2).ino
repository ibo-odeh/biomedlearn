// tuştakımının pinlerini tuşlar size bakacak şekilde soldan sağa doğru 
// 2-3-4-5-6-7-8 sıralamasında arduinoya bağlayınız.
#include <Keypad.h>
const byte SAT = 4; //4 satır
const byte SUT = 3; //3 sütun
char keys[SAT][SUT] = {
                        {'1','2','3'},
                        {'4','5','6'},
                        {'7','8','9'},
                        {'*','0','#'}
};
byte satPinleri[SAT] = {2, 3, 4, 5}; //satır pinlerini arduinoya bağlayın
byte sutPinleri[SUT] = {6, 7, 8};    //sütun pinlerini arduinoya bağlayın

Keypad keypad = Keypad( makeKeymap(keys), satPinleri, sutPinleri, SAT, SUT );

void setup(){
  Serial.begin(9600);
}
  
void loop(){
  char tus = keypad.getKey();
  if (tus) Serial.println(tus);
}


#include <Keypad.h>

const byte ROWS = 4; // 4 satır
const byte COLS = 3; // 3 sütun
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte rowPins[ROWS] = {8, 7, 6, 5}; // Satır pinleri
byte colPins[COLS] = {4, 3, 2};    // Sütun pinleri

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

const String password = "1234"; // Şifre
String inputPassword;
const int buzzer = 9;
const int relay = 10;

void setup() {
  pinMode(buzzer, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW); // Röleyi başlangıçta kapalı tut
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();

  if (key) {
    if (key == '#') { // Şifreyi onayla
      if (inputPassword == password) {
        Serial.println("Doğru Şifre!");
        digitalWrite(relay, HIGH); // Kapıyı aç
        tone(buzzer, 1000, 200); // Buzzer çalsın
        delay(5000);             // Kapı 5 saniye açık kalsın
        digitalWrite(relay, LOW); // Kapıyı kapat
      } else {
        Serial.println("Yanlış Şifre!");
        tone(buzzer, 500, 500); // Hatalı girişte uyarı
      }
      inputPassword = ""; // Şifreyi sıfırla
    } else if (key == '*') { // Şifreyi temizle
      inputPassword = "";
      Serial.println("Şifre Temizlendi");
    } else {
      inputPassword += key;
      Serial.println(inputPassword);
    }
  }
}

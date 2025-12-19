#include <Servo.h>
#include <Keypad.h>
#include <DHT.h>
#include <LiquidCrystal.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// LCD: RS=11, E=12, D4=13, D5=A0, D6=A1, D7=A2
LiquidCrystal lcd(11, 12, 13, A0, A1, A2);

Servo myServo;

// Keypad tanımı
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {3, 4, 5, 6};
byte colPins[COLS] = {7, 8, 10};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

int bpm = 12;
unsigned long lastBreath = 0;
int buzzerPin = A3;

void setup() {
  Serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);
  myServo.attach(9);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  lcd.setCursor(0, 0);
  lcd.print("Ventilator Hazir");
  delay(2000);
  lcd.clear();
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    lcd.setCursor(0, 0);
    lcd.print("DHT Hatasi");
    digitalWrite(buzzerPin, HIGH);
    delay(1000);
    digitalWrite(buzzerPin, LOW);
    return;
  }

  lcd.setCursor(0, 0);
  lcd.print("BPM:");
  lcd.print(bpm);
  lcd.print(" T:");
  lcd.print(temp);

  lcd.setCursor(0, 1);
  lcd.print("H:");
  lcd.print(hum);
  lcd.print(" %   ");

  if (temp > 30) {
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }

  // Solunum hareketi
  unsigned long interval = (60000 / bpm);
  if (millis() - lastBreath >= interval) {
    lastBreath = millis();
    myServo.write(0);
    delay(400);
    myServo.write(90);
    delay(400);
  }

  // BPM değiştirme
  char key = keypad.getKey();
  if (key == '#') {
    lcd.clear();
    lcd.print("Yeni BPM Gir:");
    String input = "";
    while (true) {
      char k = keypad.getKey();
      if (k && isDigit(k)) {
        input += k;
        lcd.setCursor(0, 1);
        lcd.print(input);
      } else if (k == '*') {
        int val = input.toInt();
        if (val > 5 && val < 60) {
          bpm = val;
          lcd.clear();
          lcd.print("BPM: ");
          lcd.print(bpm);
          delay(1000);
        }
        break;
      }
    }
  }
}

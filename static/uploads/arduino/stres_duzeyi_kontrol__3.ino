#include <Keypad.h>  
#include <LiquidCrystal.h> // LCD kütüphanesi ekleniyor

// Tuş takımı tanımlamaları  
const byte ROWS = 4; // 4 satır  
const byte COLS = 3; // 3 sütun  
char keys[ROWS][COLS] = {  
  {'1', '2', '3'},  
  {'4', '5', '6'},  
  {'7', '8', '9'},  
  {'*', '0', '#'}  
};  
byte rowPins[ROWS] = {10, 9, 8, 7}; // Satır pinleri  
byte colPins[COLS] = {6, A5, A4};    // Sütun pinleri  
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);  

// RGB LED pinleri  
const int redPin = A0;  
const int greenPin = A1;  
const int bluePin = A2;  

// Buzzer pini  
const int buzzerPin = A3;  

// LCD ekran pinleri  
LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // LCD pinleri

// Stres seviyesi değişkeni  
int stressLevel = 0;  

// Sorular  
#define MAX_QUESTIONS 3
String questions[MAX_QUESTIONS][2] = {
  {"Bugun nasil", "hissediyorsunuz?"},
  {"Stresli bir", "olay oldu mu?"},
  {"Enerjik misiniz?", ""}
};
void setup() {  
  pinMode(redPin, OUTPUT);  
  pinMode(greenPin, OUTPUT);  
  pinMode(bluePin, OUTPUT);  
  pinMode(buzzerPin, OUTPUT);  

  lcd.begin(16, 2);  // LCD ekranı başlat
  showMessage("Duygusal Durum", "Izleyici Basladi");
  showMessage("Sorulara cevap", "vermek icin 1-5 arasi");
  showMessage("bir tus basin.", "Anahtarlar: 1-5");
  showMessage("1=Cok Iyi","2=Iyi");
  showMessage("3=Orta","4=Kotu");
  showMessage("5=Cok Kotu","");
}

void loop() {  
  for (int i = 0; i < MAX_QUESTIONS; i++) {  
    // İki satırda soruyu yazdır
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(questions[i][0]);   // İlk satır
    lcd.setCursor(0, 1);
    lcd.print(questions[i][1]);   // İkinci satır
    delay(1000);  // Soruyu 1 saniye göster
    lcd.clear();

    // Cevap al
    char key = 0;  
    while (!key) {  
      key = keypad.getKey();  
    }  

    if (key >= '1' && key <= '5') {  
      int score = key - '0'; // Karakteri sayıya çevir  
      stressLevel += score;  
      lcd.clear();
      lcd.print("Girilen: ");  
      lcd.print(score);  
      delay(1000);  // Kullanıcıya yanıtı göster
    } else {  
      lcd.clear();
      lcd.print("Gecersiz tus! Lutfen 1-5 arasi bir deger girin.");
      delay(1500); // Geçersiz tuş mesajını göster
      i--; // Soruyu yeniden sor
    }  
  }  

  lcd.clear();
  lcd.print("Toplam Stres: ");  
  lcd.println(stressLevel);  

  // Stres seviyesini belirleme ve LED rengi ayarlama  
  if (stressLevel <= 7) {  
    lcd.clear();
    lcd.print("Stres: Dusuk");  
    setColor(0, 255, 0); // Yeşil  
  } else if (stressLevel > 7 && stressLevel <= 13) {  
    lcd.clear();
    lcd.print("Stres: Orta");  
    setColor(0, 0, 255); // Mavi  
  } else {  
    lcd.clear();
    lcd.print("Stres: Yüksek");  
    setColor(255, 0, 0); // Kırmızı  
    digitalWrite(buzzerPin, HIGH); // Buzzer aktif  
    delay(500);  
    digitalWrite(buzzerPin, LOW);  
  }  

  delay(5000); // Sonuçları 5 saniye göster  
  stressLevel = 0; // Yeniden başlamak için sıfırla  
}  

void setColor(int red, int green, int blue) {  
  analogWrite(redPin, red);  
  analogWrite(greenPin, green);  
  analogWrite(bluePin, blue);  
}

void showMessage(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);   // Üst satır
  lcd.print(line1);      // İlk satırda yazıyı yazdır
  lcd.setCursor(0, 1);   // Alt satır
  lcd.print(line2);      // İkinci satırda yazıyı yazdır
  delay(1500);           // Mesajı 1,5 saniye süreyle ekranda göster
  lcd.clear();           // Ekranı temizle
}

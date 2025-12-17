#include <DHT.h>

// DHT11 tanımlamaları
#define DHTPIN 8        // DHT11 veri pini Arduino D2'ye bağlı
#define DHTTYPE DHT11   // DHT11 sensör tipi
DHT dht(DHTPIN, DHTTYPE);

// RGB LED pin tanımlamaları
#define REDPIN 9
#define GREENPIN 10
#define BLUEPIN 11

void setup() {
  // Başlangıç ayarları
  Serial.begin(9600); // Seri monitör için
  dht.begin();

  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);
}

void loop() {
  // Nem değerini oku
  float nem = dht.readHumidity();

  // Okuma hatası kontrolü
  if (isnan(nem)) {
    Serial.println("DHT sensöründen veri alınamıyor!");
    return;
  }

  // Nem durumuna göre RGB LED renklerini ayarla
  if (nem >= 0 && nem < 30) {
    setRGB(0, 0, 255); // Mavi
  } else if (nem >= 30 && nem < 60) {
    setRGB(0, 255, 0); // Yeşil
  } else if (nem >= 60) {
    setRGB(255, 0, 0); // Kırmızı
  }

  // Seri monitöre veri yazdır
  Serial.print("Nem: ");
  Serial.print(nem);
  Serial.println("%");

  delay(2000); // 2 saniye bekle
}

// RGB LED renk ayarı fonksiyonu
void setRGB(int red, int green, int blue) {
  analogWrite(REDPIN, red);
  analogWrite(GREENPIN, green);
  analogWrite(BLUEPIN, blue);
}

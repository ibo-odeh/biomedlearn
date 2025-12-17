int pirPin = 6;   // PIR sensörünün OUT pini
int ledPin = 13;   // LED baglantisi
int deger = 0;             
void setup() {
  pinMode(pirPin, INPUT);       // PIR Pin'i giriş yapılıyor
  pinMode(ledPin, OUTPUT);      // LED Pin'i çıkış yapılıyor
  Serial.begin(9600);           //Serial Porttan veri göndermek için baundrate ayarlanıyor.
}
 
void loop(){
  deger = digitalRead(pirPin);    // Dijital pin okunuyor
  Serial.println(deger);          // Okunan değer seri porttan okunuyor.
  if (deger == HIGH) digitalWrite(ledPin, HIGH); // Eğer okunan değer 1 ise LED yakılıyor.
  else digitalWrite(ledPin,LOW);   // Eğer okunan değer 0 ise LED söndürülüyor.
}




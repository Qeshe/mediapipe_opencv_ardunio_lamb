int ledPins[] = {2, 3, 4, 5, 6}; // 5 LED için pinler
int parmakSayisi = 0;

void setup() {
  Serial.begin(9600);
  
  // LED pinlerini çıkış olarak ayarla
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    parmakSayisi = Serial.parseInt(); // Gelen tam sayıyı oku

    // Güvenlik için sınırla (0-5 arası olsun)
    if (parmakSayisi < 0) parmakSayisi = 0;
    if (parmakSayisi > 5) parmakSayisi = 5;

    // Tüm ledleri kapat
    for (int i = 0; i < 5; i++) {
      digitalWrite(ledPins[i], LOW);
    }

    // Gelen parmak sayısı kadar LED yak
    for (int i = 0; i < parmakSayisi; i++) {
      digitalWrite(ledPins[i], HIGH);
    }
  }
}

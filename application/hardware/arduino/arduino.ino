#include <Adafruit_NeoPixel.h>

#define LED_PIN 4
#define LED_COUNT 60

Adafruit_NeoPixel pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int IntReceived;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  pixels.begin();
  pixels.clear();
  pixels.setBrightness(50);
}

void loop() {
  pixels.clear();
  receiveData();
}

void receiveData() {
  while (Serial.available()==0) {}
  IntReceived = Serial.parseInt();
  IntReceived--;
  for (int i = 0; i < LED_COUNT; i++) {
    if (i <= IntReceived) {
      pixels.setPixelColor(i, pixels.Color(255, 0, 0));
    }
    else if (i <= (IntReceived + 3) && IntReceived != -1) {
      pixels.setPixelColor(i, pixels.Color(255, 255, 0));
    }
    else {
      pixels.setPixelColor(i, pixels.Color(0, 255, 0));
    }
  }
  pixels.show();
}
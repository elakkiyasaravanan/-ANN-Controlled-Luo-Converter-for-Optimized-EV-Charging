#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define PWM1 9
#define PWM2 5
#define ANALOG_IN_PIN A0

float adc_voltage = 0.0;
float in_voltage = 0.0;
float R1 = 30000.0;
float R2 = 7500.0;
float ref_voltage = 5.0;
int adc_value = 0;

void setup() {
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  
  Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");

  TCCR1A = (1 << COM1A1) | (1 << WGM11);
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS10);
  ICR1 = 15999;
  OCR1A = ICR1 / 2;

  TCCR0A = (1 << COM0B1) | (1 << WGM01) | (1 << WGM00);
  TCCR0B = (1 << CS01);
  OCR0B = 127;

  lcd.clear();
}

void loop() {
  adc_value = analogRead(ANALOG_IN_PIN);
  adc_voltage  = (adc_value * ref_voltage) / 1024.0;
  in_voltage = adc_voltage * (R1 + R2) / R2;
  
  lcd.setCursor(0, 0);
  lcd.print("Voltage: ");
  lcd.print(in_voltage, 2);
  lcd.print(" V  ");

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
  
    Serial.print(in_voltage);
    Serial.print(",");
    Serial.print(in_voltage);
    Serial.println();

    if (input.startsWith("F1")) {
      int freq1 = input.substring(2).toInt();
      if (freq1 >= 100 && freq1 <= 10000) {
        ICR1 = (16000000 / freq1) - 1;
      }
    }

    else if (input.startsWith("D1")) {
      int duty1 = input.substring(2).toInt();
      if (duty1 >= 0 && duty1 <= 100) {
        OCR1A = (ICR1 * duty1) / 100;
      }
    }
  }

  delay(500);
}

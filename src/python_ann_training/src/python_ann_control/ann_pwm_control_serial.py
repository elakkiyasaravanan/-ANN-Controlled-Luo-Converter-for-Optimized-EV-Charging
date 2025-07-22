import pandas as pd
import numpy as np
import tensorflow as tf
import serial
import time
import joblib

# Load ANN Model
model1 = tf.keras.models.load_model("ann_pwm_model.h5")
scaler_X1 = joblib.load("scaler_x.pkl")
scaler_y1 = joblib.load("scaler_y.pkl")

arduino_port = "COM3"  # Update as per your system
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)
except serial.SerialException:
    print("Error: Could not open serial port.")
    exit()

def predict_pwm1(voltage):
    voltage_scaled = scaler_X1.transform(np.array([[voltage]]))
    pred_scaled = model1.predict(voltage_scaled)
    pred = scaler_y1.inverse_transform(pred_scaled)
    frequency, duty_cycle = pred[0]
    return int(frequency), int(duty_cycle)

print("Serial connection established!")

while True:
    try:
        data = ser.readline().decode().strip()
        values = data.split(',')
        if len(values) == 2:
            vv, kk = values
            F1, D1 = predict_pwm1(float(vv))
            command1 = f"F1{F1}\nD1{D1}\n"
            ser.write(command1.encode())
            print(f"Sent to Arduino - PWM1: {F1}Hz, {D1}%")
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        ser.close()
        break
    except Exception as e:
        print(f"Error: {e}")

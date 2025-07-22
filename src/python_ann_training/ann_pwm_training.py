import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

voltages = np.linspace(0, 24, 500)  # 0V to 24V
frequencies = 100 + (voltages * (500 - 100) / 24)  # Mapping 100 Hz to 10kHz
duty_cycles = 5 + (voltages * (20 - 5) / 24)  # Mapping 5% to 80%
# Create DataFrame
data = pd.DataFrame({'Voltage': voltages, 'Frequency': frequencies, 'DutyCycle': duty_cycles})
data.to_csv("pwm_data.csv", index=False)  # Save dataset

# Load Dataset
df = pd.read_csv("pwm_data.csv")
X = df[['Voltage']].values  # Input: Voltage
y = df[['Frequency', 'DutyCycle']].values  # Output: Frequency & Duty Cycle

# Normalize Data
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_x.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Save Scalers
joblib.dump(scaler_x, "scaler_x.pkl")
joblib.dump(scaler_y, "scaler_y.pkl")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Build ANN Model
model = keras.Sequential([
    keras.layers.Dense(10, activation="relu", input_shape=(1,)),
    keras.layers.Dense(10, activation="relu"),
    keras.layers.Dense(2, activation="linear")  # Output: Frequency & Duty Cycle
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# Train Model
model.fit(X_train, y_train, epochs=200, batch_size=16, validation_data=(X_test, y_test))

# Save Model
model.save("ann_pwm_model.h5")
print("Model trained and saved successfully!")
    

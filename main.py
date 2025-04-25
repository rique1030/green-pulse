import argparse
import pandas as pd
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Argument Parsing
parser = argparse.ArgumentParser(description="Train Autoencoder Model")
parser.add_argument("--csv_path", type=str, required=True, help="Path to the CSV file")
parser.add_argument("--window_size", type=int, default=24, help="Number of consecutive readings per sample (default: 24).")
parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs (default: 50).")
parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training (default: 32).")
args = parser.parse_args()

# Load data from CSV
df = pd.read_csv(args.csv_path)
if "power" not in df.columns:
    raise ValueError("CSV file does not contain 'power_kWh' column")

data = df["power"].values.reshape(-1, 1)

# Normalize data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)
# Windowed Sequences
def create_windows(data, window_size=24):
    windows = []
    for i in range(len(data) - window_size):
        windows.append(data[i:i+window_size].flatten())
    return np.array(windows)
x = create_windows(data_scaled, args.window_size)

# Autoencoder Model
input_dim = x.shape[1]
input_layer = Input(shape=(input_dim,))

# Encoder layers
encoded = Dense(12, activation='relu')(input_layer)
encoded = Dense(6, activation='relu')(encoded)

decoded = Dense(6, activation='relu')(encoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded)

# create the autoencoder model
autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train
history = autoencoder.fit(x, x,
                          epochs=args.epochs,
                          batch_size=args.batch_size,
                          shuffle=True,
                          validation_split=0.2)

# Reconstruction Errors
reconstructions = autoencoder.predict(x)
mse = np.mean(np.power(x - reconstructions, 2), axis=1)

# anomaly threshold
threshold = np.percentile(mse, 95)
print(f"Anomaly Threshold: {threshold}")
print(f"Number of Anomalies: {np.sum(mse > threshold)}")

# Reconstruction Errors Plotting
plt.figure(figsize=(10, 5))
plt.plot(mse, label="Reconstruction Error")
plt.axhline(y=threshold, color='r', linestyle='--', label="Anomaly Threshold")
plt.title("Reconstruction Errors per Sample")
plt.xlabel("Sample Index")
plt.ylabel("Mean Squared Error")
plt.legend()
plt.savefig("reconstruction_errors.png", bbox_inches="tight")

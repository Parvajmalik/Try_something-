import serial
import time
from datetime import datetime


PORT = "COM7"       
BAUD_RATE = 115200
OUTPUT_FILE = "ina219_data.csv"


ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for ESP32 to reset

print("Press Ctrl+C to stop.\n")

with open(OUTPUT_FILE, "a") as f:
    f.write("Timestamp,Bus Voltage (V),Shunt Voltage (mV),Current (mA)\n")


try:
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line.startswith("Bus Voltage:"):
            # Example incoming lines:
            # Bus Voltage: 4.98 V
            # Shunt Voltage: 5.20 mV
            # Current: 51.00 mA

            # Read three consecutive lines
            bus_voltage = line.split(":")[1].strip().split(" ")[0]
            shunt_voltage = ser.readline().decode().strip().split(":")[1].strip().split(" ")[0]
            current = ser.readline().decode().strip().split(":")[1].strip().split(" ")[0]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to file
            with open(OUTPUT_FILE, "a") as f:
                f.write(f"{timestamp},{bus_voltage},{shunt_voltage},{current}\n")

            print(f"{timestamp} | Vbus={bus_voltage}V | Vshunt={shunt_voltage}mV | I={current}mA")

except KeyboardInterrupt:
    print("\nLogging stopped by user.")
    ser.close()

import serial
import csv
import time
import os #acts as a bridge between python and operating system windoes, os, mac

# SD Card path configuration (adjust drive letter as needed)
SD_CARD_PATH = "E:/"  # Change to your SD card drive letter (D:/, E:/, etc.)
CSV_FILE_PATH = os.path.join(SD_CARD_PATH, "telemetry_data.csv")

telemetry_running = False


def arduino_read():

    port = serial.Serial('COM3', 9600)  # Update with your serial port and baud rate



def telem_control():
    global telemetry_running
    while True:
        print("1 - Start Telemetry")
        print("2 - Stop Telemetry")
        print("3 - Save Log to CSV")
        choice = int(input("Enter your choice: "))



        if choice == 1:
            print("Starting telemetry...")
            telemetry_running = True
            # Code to start telemetry
        elif choice == 2:
            print("Stopping telemetry...")
            telemetry_running = False

            # Code to stop telemetry
        elif choice == 3:
            print("Saving log to CSV...")
            timestamp = time.time()  # Example of getting the current timestamp

            with(open(CSV_FILE_PATH, "w", newline='')) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, "Distance", "Velocity", "Acceleration", "RPM"])  # Write header
                print(timestamp, "Distance", "Velocity", "Acceleration", "RPM")  # Example of writing telemetry data to CSV

        else:
            print("Invalid choice. Please try again.")



def calculations(): #NEEDS WORK
    velocity = distance / time
    acceleration = velocity / time

    # Code to perform calculations on the telemetry data


    

GRAFANA_URL = "http://localhost:3000/" # Your Grafana URL
GRAFANA_API_KEY = "sa-1-telemetry-dashboard-a3a58f0b-6b33-454a-842b-8dd1d499a844"  # Your Grafana API key with permissions to push to live stream
LIVE_STREAM = "f1_telemetry" # Whatever you want to call your stream



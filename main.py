import serial
import csv



def arduino_read():

    port = serial.Serial('COM3', 9600)  # Update with your serial port and baud rate

    while True:
        print("1 - Start Telemetry")
        print("2 - Stop Telemetry")
        print("3 - Save Log to CSV")
        choice = int(input("Enter your choice: "))


        if choice == 1:
            print("Starting telemetry...")
            # Code to start telemetry
        elif choice == 2:
            print("Stopping telemetry...")
            # Code to stop telemetry
        elif choice == 3:
            print("Saving log to CSV...")
        else:
            print("Invalid choice. Please try again.")




with(open("telemetry_data.csv", "w", newline='')) as csvfile:
    writer = csv.write(csvfile)
    writer.writerow([#Whatever the metrics are])
    

GRAFANA_URL = "http://localhost:3000/" # Your Grafana URL
GRAFANA_API_KEY = "sa-1-telemetry-dashboard-a3a58f0b-6b33-454a-842b-8dd1d499a844"  # Your Grafana API key with permissions to push to live stream
LIVE_STREAM = "f1_telemetry" # Whatever you want to call your stream


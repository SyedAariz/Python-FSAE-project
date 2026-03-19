import serial
import requests
import csv
import time
import os #acts as a bridge between python and operating system windoes, os, mac


GRAFANA_URL = "http://localhost:3000" # Your Grafana URL
GRAFANA_API_KEY = "eyJrIjoieEJLNW9jNkZaMXB1a0dGRzlqZXYxY0UzMEt2cld3OUciLCJuIjoidGVsZW1ldHJ5IiwiaWQiOjF"  # Your Grafana API key with permissions to push to live stream
LIVE_STREAM = "telemetry" # Whatever you want to call your stream

grafana_headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "text/plain",
}


# SD Card path configuration (adjust drive letter as needed)
SD_CARD_PATH = "."  # Change to your SD card drive letter (D:/, E:/, etc.)
CSV_FILE_PATH = os.path.join(SD_CARD_PATH, "telemetry_data.csv")


port = serial.Serial('/dev/cu.usbserial-0001', 115200)  # Update with your serial port and baud rate


telemetry_running = False  # Flag to control telemetry state


def save_to_csv():

    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Voltage", "Distance", "Velocity", "Acceleration", "RPM"])
            print("CSV header written")


def data_logging(voltage):
    timestamp = time.time()

    with open(CSV_FILE_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, voltage])

       
def grafana(line):
    # ---- Grafana Live push (true streaming) ----
            # We use Grafana Live features to push real-time data

    try:
        data = (
        f"telemetry"
                f" Voltage={line}"        
            )
        requests.post(
            f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
            headers=grafana_headers,
            data=data,
            timeout=0.05,
        )
    except requests.exceptions.RequestException:
        pass  # never block telemetry


#def calculations(voltage): #NEEDS WORK
    #position = (voltage/3.3) * max_distance #How do we get max distance? We can set it to 100 for now, but we need to figure out how to get it from the telemetry data
    #displacement = position - initial_position #initial position can be set to 0
    
    #velocity = position / time.stamp()  # Example of calculating velocity using position and time
    #acceleration = velocity / time.stamp()  # Example of calculating acceleration using velocity and time

    # Code to perform calculations on the telemetry data

def telem_control():
    global telemetry_running

    telemetry_running = False

    while True:
        if not telemetry_running:
            print("1 - Start Telemetry")
            print("2 - Stop Telemetry")
            print("3 - Save Log to CSV")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                print("Starting telemetry...")
                telemetry_running = True

            elif choice == 2:
                print("Telemetry already stopped.")

            elif choice == 3:
                print("Saving log to CSV...")
                save_to_csv()

        else:
            line = port.readline().decode('utf-8', errors="ignore").strip()

            if line:
                print(line)

                if "travel_mm=" in line:
                    try:
                        value = float(line.split("travel_mm=")[1].split()[0])
                    except:
                        continue

                    grafana(value)
                    data_logging(value)

            # allow stopping
            if port.in_waiting == 0:
                if input("Press 2 to stop telemetry: ") == "2":
                    print("Stopping telemetry...")
                    telemetry_running = False

    

if __name__ == "__main__":
    telem_control()



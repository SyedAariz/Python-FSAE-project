import serial
import requests
import csv
import time
import os #acts as a bridge between python and operating system windoes, os, mac


GRAFANA_URL = "http://localhost:3000" # Your Grafana URL
GRAFANA_API_KEY = "----"  # Your Grafana API key with permissions to push to live stream
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
            #line = port.readline().decode().strip()
            writer = csv.writer(csvfile)
            writer.writerow(["Travel_mm"])  # Write header only if file is new
            print("CSV header written")


def data_logging(voltage):
    

    with open(CSV_FILE_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([voltage])

       
def grafana(line):
    # ---- Grafana Live push (true streaming) ----
            # We use Grafana Live features to push real-time data

    try:
        data = (
        f"telemetry"
                f" Travel_mm={line}"        
            )
        requests.post(
            f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
            headers=grafana_headers,
            data=data,
            timeout=0.05,
        )
    except requests.exceptions.RequestException:
        pass  # never block telemetry

def run_funcs():
    save_to_csv()

    try:
        line = port.readline().decode(errors="ignore").strip()

        if "travel_mm=" in line:
            # Extract travel_mm value
            travel_part = line.split("travel_mm=")[1].split()[0]
            voltage = float(travel_part)

            print(f"Travel_mm: {voltage}")

            data_logging(voltage)
            grafana(voltage)

    except Exception as e:
        print("Error:", e)


#def calculations(voltage): #NEEDS WORK
    #position = (voltage/3.3) * max_distance #How do we get max distance? We can set it to 100 for now, but we need to figure out how to get it from the telemetry data
    #displacement = position - initial_position #initial position can be set to 0
    
    #velocity = position / time.stamp()  # Example of calculating velocity using position and time
    #acceleration = velocity / time.stamp()  # Example of calculating acceleration using velocity and time

    # Code to perform calculations on the telemetry data


#def calculations(travel_mm):
    #global begin_velocity, begin_position, prev_time, initial_position
    #current_time = time.time()
    #position = travel_mm


    #if initial_position is None:
        #initial_position = position
        #prev_position = position
        #prev_time = current_time
    #return position, 0.0, 0.0, 0.0


    #delta_time = current_time - prev_time
        #if delta_time == 0:
            #return posiition, 0.0, 0.0, 0.0



    #velocity = (position - prev_position) / delta_time          # mm/s
    #acceleration = (velocity - begin_velocity) / delta_time      # mm/s²


    #prev_position = position
    #prev_time = current_time
    #prev_velocity = velocity
    #return position, velocity, acceleration



if __name__ == "__main__":
    while True:
        run_funcs()



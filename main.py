import serial
import requests
import csv
import time
import os #acts as a bridge between python and operating system windoes, os, mac


GRAFANA_URL = "http://localhost:3000/" # Your Grafana URL
GRAFANA_API_KEY = "GRAFANA_KEY"  # Your Grafana API key with permissions to push to live stream
LIVE_STREAM = "telemetry" # Whatever you want to call your stream

grafana_headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "text/plain",
}


# SD Card path configuration (adjust drive letter as needed)
SD_CARD_PATH = "E:/"  # Change to your SD card drive letter (D:/, E:/, etc.)
CSV_FILE_PATH = os.path.join(SD_CARD_PATH, "telemetry_data.csv")


port = serial.Serial('COM3', 115200)  # Update with your serial port and baud rate





def save_to_csv():

    with(open(CSV_FILE_PATH, "a", newline='')) as csvfile:
        timestamp = time.time()  # Get the current timestamp
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, "Voltage", "Distance", "Velocity", "Acceleration", "RPM"])  # Write header
        print(timestamp, "Distance", "Velocity", "Acceleration", "RPM")  # Example of writing telemetry data to CSV
        data_logging(writer, csvfile)


def data_logging(writer, csvfile):
    while telemetry_running:
        line = port.readline().decode('utf-8').strip()  # Read a line from the serial port
        if line:
            print(line)  # Print the telemetry data to the console
            
            try:
                Voltage = float(line.split("=")[1])  # Example of parsing voltage from the telemetry data
                timestamp = time.time()  # Get the current timestamp
                writer.writerow([timestamp, Voltage])  # Write timestamp and voltage to CSV. Need to write more.
                csvfile.flush()  # Ensure data is written to the file
            except:
                pass

       
def grafana(data):
    # ---- Grafana Live push (true streaming) ----
            # We use Grafana Live features to push real-time data
    
    line = (
        f"telemetry"
                f"m_voltage={data["Voltage"]}"        
            )

    try:
        requests.post(
            f"{GRAFANA_URL}/api/live/push/{LIVE_STREAM}",
            headers=grafana_headers,
            data=line,
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
    while True:
        print("1 - Start Telemetry")
        print("2 - Stop Telemetry")
        print("3 - Save Log to CSV")
        choice = int(input("Enter your choice: "))



        if choice == 1:
            print("Starting telemetry...")
            telemetry_running = True
            grafana(data)  # Call the function to push data to Grafana Live
            # Code to start telemetry
        elif choice == 2:
            print("Stopping telemetry...")
            telemetry_running = False

            # Code to stop telemetry
        elif choice == 3:
            print("Saving log to CSV...")
            timestamp = time.time()  # Example of getting the current timestamp
            data_logging(writer, csvfile)  # Call the data logging function to read from serial and write to CSV
            save_to_csv()  # Call the function to save data to CSV


    

if __name__ == "__main__":
    telem_control()



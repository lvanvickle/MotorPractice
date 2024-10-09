# Import statement for premade modules
import serial # Allows for create serial (usb) communication
import random # Allows us to program random movement
import time # Gives us ability to create delays

# Import statement for custom modules
from motor_func import move_forward, move_backward, turn_left, turn_right, stop_motors # Gives us motor functionality

# Initialize the serial connection
ser = None

def setup_serial():
    global ser
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino on /dev/ttyUSB0")
    except serial.SerialException as e:
        print(f"Error: {e}")

# Function to read distance data from the Arduino
def read_distance():
    if ser and ser.in_waiting > 0:
        try:
            distance = float(ser.readline().decode().strip())
            return distance
        except ValueError:
            return None
    return None

# Autonomous behavior function
def start_autonomy(get_mode):
    while get_mode() == "autonomous": # Use global mode from main.py
        distance = read_distance()
        
        if distance is not None and distance < 20:  # If obstacle is closer than 20 cm
            print(f"Obstacle detected at {distance} cm. Stopping and backing up.")
            stop_motors()
            time.sleep(1)
            move_backward(0.3)
            time.sleep(1)
            stop_motors()
            
            # Randomly turn left or right
            if random.choice([True, False]):
                print("Turning left to avoid obstacle.")
                turn_left(0.3)
            else:
                print("Turning right to avoid obstacle.")
                turn_right(0.3)
            time.sleep(1)
            stop_motors()

        # Move forward if no obstacle
        print(f"Closest obstacle {distance} cm away.")
        print("Moving forward.")
        move_forward(0.5)
        time.sleep(0.5)  # Move forward for a short time before checking again

    stop_motors()  # Ensure motors are stopped if mode changes
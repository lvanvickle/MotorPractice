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
    while get_mode() == "autonomous":
        distance = read_distance()

        if distance is not None and distance < 20:
            print(f"Obstacle detected at {distance} cm. Stopping and backing up.")
            stop_motors()

            # Move backward but check distance in real-time
            start_time = time.time()
            while time.time() - start_time < 1:  # Moving backward for 1 second
                move_backward(0.3)
                distance = read_distance()
                if distance > 20:  # Stop if the obstacle is cleared
                    break
            stop_motors()

            # Randomly turn left or right with real-time sensor check
            if random.choice([True, False]):
                print("Turning left to avoid obstacle.")
                start_time = time.time()
                while time.time() - start_time < 1:
                    turn_left(0.3)
                    distance = read_distance()
                    if distance > 20:  # Stop turning if no obstacle
                        break
            else:
                print("Turning right to avoid obstacle.")
                start_time = time.time()
                while time.time() - start_time < 1:
                    turn_right(0.3)
                    distance = read_distance()
                    if distance > 20:
                        break
            stop_motors()

        else:
            print(f"Closest obstacle {distance} cm away. Moving forward.")
            move_forward(0.5)

            # Keep checking sensor while moving forward
            start_time = time.time()
            while time.time() - start_time < 0.5:  # Move for 0.5 seconds, but check often
                distance = read_distance()
                if distance < 20:
                    break  # Immediately stop if an obstacle is detected
            stop_motors()
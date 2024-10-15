# Importing necessary modules
import serial  # Provides communication between the Raspberry Pi and Arduino via USB
import random  # Allows us to generate random choices for turning left or right
import time  # Gives us the ability to add delays (pauses) in the code

# Importing custom motor functions to control the robot's movement
from motor_func import move_forward, move_backward, turn_left, turn_right, stop_motors

# Initializing the serial connection to None (not connected yet)
ser = None

# This function sets up the serial connection between the Raspberry Pi and Arduino
# The Raspberry Pi will communicate with the Arduino via USB
def setup_serial():
    global ser  # This makes sure we can access the 'ser' variable defined outside the function
    try:
        # Try to connect to Arduino on port /dev/ttyUSB0 with a baud rate of 9600
        # 'timeout=1' means it will wait 1 second for a response before timing out
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        print("Connected to Arduino on /dev/ttyUSB0")
    except serial.SerialException as e:
        # If there's an error in setting up the connection, print the error message
        print(f"Error: {e}")

# This function reads the distance data sent from the Arduino
# It returns the distance value in centimeters
def read_distance():
    # Check if the serial connection is active and if there's any data to read
    if ser and ser.in_waiting > 0:
        try:
            # Read the incoming data, decode it into a string, and strip any extra spaces or newlines
            # Convert it into a float (decimal number) representing the distance in cm
            distance = float(ser.readline().decode().strip())
            return distance  # Return the distance value
        except ValueError:
            # If there's an issue converting the data to a number, return None (no valid distance)
            return None
    return None  # If there's no data to read, return None

# This function handles the robot's autonomous movement behavior
# It will keep moving and reacting to obstacles as long as the mode is set to 'autonomous'
def start_autonomy(get_mode):
    # Continue the loop while the mode is set to "autonomous"
    while get_mode() == "autonomous":
        # Get the current distance from the read_distance function
        distance = read_distance()

        # If the distance is valid (not None) and an obstacle is closer than 20 cm
        if distance is not None and distance < 20:
            print(f"Obstacle detected at {distance} cm. Stopping and backing up.")
            stop_motors()  # Stop the robot immediately

            # Move backward for 1 second, continuously checking the distance to avoid obstacles
            start_time = time.time()  # Record the current time
            while time.time() - start_time < 1:  # Keep moving backward for 1 second
                move_backward(0.5)  # Move backward at 30% speed
                distance = read_distance()  # Read the distance again while moving
                if distance is not None and distance > 20:  # If the path is clear
                    break  # Stop moving backward
            stop_motors()  # Stop the motors after moving backward

            # Randomly decide whether to turn left or right to avoid the obstacle
            if random.choice([True, False]):  # Randomly choose True (left) or False (right)
                print("Turning left to avoid obstacle.")
                start_time = time.time()
                while time.time() - start_time < 1:  # Turn left for 1 second
                    turn_left(0.5)  # Turn left at 30% speed
                    distance = read_distance()  # Check if the path is clear while turning
                    if distance is not None and distance > 20:  # If no obstacles ahead
                        break  # Stop turning
            else:
                print("Turning right to avoid obstacle.")
                start_time = time.time()
                while time.time() - start_time < 1:  # Turn right for 1 second
                    turn_right(0.5)  # Turn right at 30% speed
                    distance = read_distance()  # Check if the path is clear while turning
                    if distance is not None and distance > 20:  # If no obstacles ahead
                        break  # Stop turning
            stop_motors()  # Stop the motors after turning

        # If there are no close obstacles (or distance data is valid)
        elif distance is not None:
            print(f"Closest obstacle {distance} cm away. Moving forward.")
            move_forward(1)  # Move forward at 50% speed

            # Keep checking the distance while moving forward
            start_time = time.time()
            while time.time() - start_time < 0.5:  # Move for 0.5 seconds
                distance = read_distance()  # Check if there's a new obstacle
                if distance is not None and distance < 20:  # If a new obstacle is detected
                    break  # Stop moving forward immediately
            stop_motors()  # Stop the motors after moving forward

# Main function that sets up and starts the robot in autonomous mode
def main():
    # Set up the serial connection
    setup_serial()

    # Placeholder for mode control (example function that could be used to switch modes)
    def get_mode():
        return "autonomous"

    # Start the autonomous behavior
    start_autonomy(get_mode)

# This ensures that the script will run if executed directly but won't run if imported as a module
if __name__ == "__main__":
    main()

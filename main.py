# Import statements for premade modules
import threading # Allows us to switch between manual and autonomous modes
import tkinter as tk # Allows us to create GUI
from tkinter import messagebox # Allows us to display notifications
import ttkbootstrap as ttk # Contains more modern looking GUI elements
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER # Design themes

# Import statements for custom modules
from motor_func import move_forward, move_backward, turn_left, turn_right, stop_motors # Contains functionality for motors
from autonomous import start_autonomy, setup_serial

# Global variables (We can use these anywhere in the script)
speed = 1.0 # Default speed for full throttle
mode = "manual" # Start in manual mode
autonomous_thread = None # Placeholder for the autonomous thread

# Function to toggle between fast and slow
def toggle_speed():
    global speed # Access global speed variable
    if speed == 1.0:
        speed = 0.5 # Set speed to half if toggled at full speed
        speed_button.config(text="Fast Mode: Off")
    else:
        speed = 1.0 # Set speed to full if toggled at half speed
        speed_button.config(text="Fast Mode: On")
    print(f"Speed set to {'Slow' if speed == 0.5 else 'Fast'}.")
    
# Function to toggle between manual and autonomous modes
def toggle_mode():
    global mode, autonomous_thread # Access global mode and autonomous thread
    if mode == "manual":
        mode = "autonomous"
        mode_button.config(text="Autonomous Mode: On")
        # Start autonomous mode in a separate thread
        autonomous_thread = threading.Thread(target=start_autonomy, args=(get_mode,))
        autonomous_thread.start()
    else:
        mode = "manual"
        mode_button.config(text="Autonomous Mode: Off")
        print("Switching to Manual Mode.")
        stop_motors() # Ensure the motors stop when switching to manual
        
# Function to return the current mode
def get_mode():
    return mode

# Call each movement direction based on button pressed
def forward_press(event): # Triggered if user presses "Forward" button
    move_forward(speed) # Imported from motor_func.py

def backward_press(event): # Triggered if user presses "Backward" button
    move_backward(speed) # Imported from motor_func.py

def left_press(event): # Triggered if user presses "Left" button
    turn_left(speed) # Imported from motor_func.py

def right_press(event): # Triggered if user presses "Right" button
    turn_right(speed) # Imported from motor_func.py

def stop_release(event): # Triggered if user presses "Stop" button
    stop_motors() # Imported from motor_func.py
    mode = "manual"

#-------------------------------------------------------------------------------------------#

# Set up the GUI
root = ttk.Window(themename="darkly")
root.title("Rover Control")

# Create the buttons for movement
forward_button = ttk.Button(root, text="Forward", width=10)
backward_button = ttk.Button(root, text="Backward", width=10)
left_button = ttk.Button(root, text="Left", width=10)
right_button = ttk.Button(root, text="Right", width=10)
stop_button = ttk.Button(root, text="Stop", width=10, command=stop_motors)
speed_button = ttk.Button(root, text="Fast Mode: On", width=15, command=toggle_speed)
mode_button = ttk.Button(root, text="Autonomous Mode: Off", width=20, command=toggle_mode)

# Bind the buttons to their respective functions
forward_button.bind("<ButtonPress-1>", forward_press)
forward_button.bind("<ButtonRelease-1>", stop_release)
backward_button.bind("<ButtonPress-1>", backward_press)
backward_button.bind("<ButtonRelease-1>", stop_release)
left_button.bind("<ButtonPress-1>", left_press)
left_button.bind("<ButtonRelease-1>", stop_release)
right_button.bind("<ButtonPress-1>", right_press)
right_button.bind("<ButtonRelease-1>", stop_release)

# Layout the buttons in the grid
forward_button.grid(row=0, column=1, padx=10, pady=10)
backward_button.grid(row=2, column=1, padx=10, pady=10)
left_button.grid(row=1, column=0, padx=10, pady=10)
right_button.grid(row=1, column=2, padx=10, pady=10)
stop_button.grid(row=1, column=1, padx=10, pady=10)
speed_button.grid(row=3, column=1, padx=10, pady=10)
mode_button.grid(row=4, column=1, padx=10, pady=10)

# Initialize the serial connection for the Arduino
setup_serial()

root.mainloop()
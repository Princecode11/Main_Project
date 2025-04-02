import tkinter as tk

class TrafficLight:
    def __init__(self, color):
        # Initialize the traffic light with a given color and default state
        self.color = color
        self.state = "white"  # Current state of the light
        self.light_state = {"red": "gray", "yellow": "gray", "green": "gray"}  # Light colors initially set to gray
        self.remaining_time = 4  # Set initial countdown time

    def change_state(self):
        # Change the state of the traffic light based on the current state
        if self.state == "red":
            # Transition from red to green
            self.state = "green"
            self.light_state = {"red": "gray", "yellow": "gray", "green": "green"}
            self.remaining_time = 15  # Set countdown for green light
        elif self.state == "green":
            # Transition from green to yellow
            self.state = "yellow"
            self.light_state = {"red": "gray", "yellow": "yellow", "green": "gray"}
            self.remaining_time = 6  # Set countdown for yellow light
        else:
            # Transition from yellow to red
            self.state = "red"
            self.light_state = {"red": "red", "yellow": "gray", "green": "gray"}
            self.remaining_time = 10  # Set countdown for red light

    def update_countdown(self, label):
        # Update the countdown timer and change the state when time is up
        if self.remaining_time >= 0:
            # Update the label with the remaining time and the current state color
            label.config(text=str(self.remaining_time), fg=self.state)
            self.remaining_time -= 1  # Decrement remaining time
            # Schedule the countdown to update again after 1000 ms (1 second)
            label.after(1000, self.update_countdown, label)
        else:
            # Change the state of the traffic light when countdown reaches zero
            self.change_state()
            # Restart the countdown process
            label.after(1, self.update_countdown, label)

class TrafficLightApp:
    def __init__(self, master):
        # Initialize the main application window
        self.master = master
        self.master.title("Traffic Light Simulator created by PRINCE")  # Set window title
        self.master.configure(bg="black")  # Set background color

        self.traffic_lights = []  # List to hold the traffic light instances

        # Create three traffic lights (red, yellow, green) and their frames
        for i, color in enumerate(["red", "yellow", "green"]):
            light = TrafficLight(color)  # Create a TrafficLight instance
            self.traffic_lights.append(light)  # Add it to the list
            self.create_light_frame(i, light)  # Create a visual frame for the light

        self.update_lights()  # Start updating the light states visually

    def create_light_frame(self, index, traffic_light):
        # Create a frame for each traffic light with its visual components
        frame = tk.Frame(self.master, bg="black")  # Frame for the light
        frame.pack(side=tk.LEFT, padx=10)  # Pack the frame to the left

        light_canvas = tk.Canvas(frame, width=100, height=300, bg="black")  # Canvas to draw light
        light_canvas.pack()  # Pack the canvas into the frame

        # Store the canvas in the traffic light object to manipulate later
        traffic_light.light_canvas = light_canvas
        # Create oval shapes for red, yellow, and green lights on the canvas
        traffic_light.shape = {
            "red": light_canvas.create_oval(25, 25, 75, 75, fill="gray"),
            "yellow": light_canvas.create_oval(25, 125, 75, 175, fill="gray"),
            "green": light_canvas.create_oval(25, 225, 75, 275, fill="gray"),
        }

        # Create a countdown label to display remaining time
        countdown_label = tk.Label(frame, text="", font=("Arial", 16), fg="white", bg="black")
        countdown_label.pack()  # Pack the label into the frame

        # Start the countdown timer for this traffic light
        traffic_light.update_countdown(countdown_label)

    def update_lights(self):
        # Update the colors of the traffic lights based on their current state
        for light in self.traffic_lights:
            colors = light.light_state  # Get the current light states
            for color, state in colors.items():
                # Update the color of the corresponding shape in the canvas
                light.light_canvas.itemconfig(light.shape[color], fill=state)

        # Schedule the update_lights method to run every 1000 ms (1 second)
        self.master.after(1000, self.update_lights)

# Main execution starts here
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = TrafficLightApp(root)  # Initialize the traffic light application
    root.mainloop()  # Run the application event loop
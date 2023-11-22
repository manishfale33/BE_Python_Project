import tkinter as tk
from bulkemail import send_email  # Import the send_email function from the bulkemail module
from fb import your_existing_facebook_function  # Import your existing Facebook function

# Create a function to display the selected option in a label
def show_selected_option(option):
    selected_option_label.config(text=f"Selected Option: {option}")

# Function to open the email interface
def open_email_interface():
    show_selected_option("Email")
    # Call the existing send_email function or implement the email functionality here
    send_email()

# Function to open the Facebook interface
def open_facebook_interface():
    show_selected_option("Facebook")
    # Call your existing Facebook function or implement the Facebook functionality here
    your_existing_facebook_function()

# Function to open other interfaces
def open_other_interface():
    show_selected_option("Other")
    # Implement the functionality for other interfaces here

# Create the main window
root = tk.Tk()
root.title("Home Interface")

# Create buttons to access different interfaces
email_button = tk.Button(root, text="Email Interface", command=open_email_interface)
email_button.pack(pady=10)

facebook_button = tk.Button(root, text="Facebook Interface", command=open_facebook_interface)
facebook_button.pack(pady=10)

# Add more buttons for other interfaces if needed
# other_button = tk.Button(root, text="Other Interface", command=open_other_interface)
# other_button.pack(pady=10)

# Create a label to display the selected option
selected_option_label = tk.Label(root, text="Selected Option: None")
selected_option_label.pack()

# Start the main event loop
root.mainloop()

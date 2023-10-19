import tkinter as tk
from bulkemail import send_email  # Import the send_email function from the bulkemail module

def open_email_interface():
    pass  # Call the existing send_email function

def open_facebook_interface():
    # Implement the functionality for Facebook interface here
    pass

def open_other_interface():
    # Implement the functionality for other interfaces here
    pass

# Create a function to display the selected option in a label
def show_selected_option(option):
    selected_option_label.config(text=f"Selected Option: {option}")

# Create the main window
root = tk.Tk()
root.title("Home Interface")

# Create buttons to access different interfaces
email_button = tk.Button(root, text="Email Interface", command=lambda: [show_selected_option("Email"), open_email_interface(send_email())])
email_button.pack(pady=10)

facebook_button = tk.Button(root, text="Facebook Interface", command=lambda: [show_selected_option("Facebook"), open_facebook_interface()])
facebook_button.pack(pady=10)

# Add more buttons for other interfaces if needed
# other_button = tk.Button(root, text="Other Interface", command=lambda: [show_selected_option("Other"), open_other_interface()])
# other_button.pack(pady=10)

# Create a label to display the selected option
selected_option_label = tk.Label(root, text="Selected Option: None")
selected_option_label.pack()

# Start the main event loop
root.mainloop()

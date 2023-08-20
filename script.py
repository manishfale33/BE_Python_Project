import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading

# Path to Chrome WebDriver executable
webdriver_path = 'chromedriver.exe'

# Set up Chrome service with the executable path
chrome_service = webdriver.ChromeService(executable_path=webdriver_path)

# Initialize the Chrome browser with the service
driver = webdriver.Chrome(service=chrome_service)

# Function to load phone numbers from a CSV file
def load_numbers():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as file:
            numbers = file.read().splitlines()
            recipients_text.delete("1.0", tk.END)
            for number in numbers:
                recipients_text.insert(tk.END, number + '\n')

# Function to send messages
def send_messages():
    recipient_names = recipients_text.get("1.0", "end-1c").split('\n')
    message_text = message_entry.get("1.0", "end-1c")

    driver.get('https://web.whatsapp.com/')
    input("Scan the QR code and press Enter after logging in...")

    for recipient_name in recipient_names:
        if recipient_name:
            search_bar = driver.find_element_by_xpath('//div[contains(@class, "copyable-text")]')
            search_bar.click()
            search_bar.send_keys(recipient_name)
            search_bar.send_keys(Keys.ENTER)

            time.sleep(2)

            message_input = driver.find_element_by_xpath('//div[contains(@class, "copyable-text")]')
            message_input.send_keys(message_text)
            message_input.send_keys(Keys.ENTER)
            time.sleep(1)

# Create the main window
root = tk.Tk()
root.title("WhatsApp Blaster")

# Recipients Entry (loaded from CSV)
recipients_label = tk.Label(root, text="Recipients:")
recipients_label.pack()
recipients_text = tk.Text(root, height=10, width=40)
recipients_text.pack()

# Load Numbers Button
load_button = tk.Button(root, text="Load Numbers", command=load_numbers)
load_button.pack()

# Message Entry
message_label = tk.Label(root, text="Message:")
message_label.pack()
message_entry = tk.Text(root, height=5, width=40)
message_entry.pack()

# Send Messages Button
send_button = tk.Button(root, text="Send Messages", command=lambda: threading.Thread(target=send_messages).start())
send_button.pack()

# Function to close the browser and destroy the GUI window
def close_browser_and_exit():
    driver.quit()
    root.destroy()

# Bind the window close event to the close_browser_and_exit function
root.protocol("WM_DELETE_WINDOW", close_browser_and_exit)

# Start the GUI event loop
root.mainloop()

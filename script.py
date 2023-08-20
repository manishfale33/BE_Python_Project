import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import openai
import pyautogui  # Import the pyautogui library for file uploads

# Set up your OpenAI API key
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual API key

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

# Function to generate a message using AI
def generate_message(recipient_name):
    prompt = f"Generate a message for {recipient_name}: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,  # Adjust the max length of the generated message
        n=1,  # Number of completions to generate
        stop=None,  # You can set stop words if needed
        temperature=0.7  # Adjust the temperature for randomness
    )
    message = response.choices[0].text.strip()
    return message

# Function to send messages
def send_messages():
    recipient_names = recipients_text.get("1.0", "end-1c").split('\n')
    manual_message = message_entry.get("1.0", "end-1c")
    attachment_path = attachment_entry.get("1.0", "end-1c").strip()

    driver.get('https://web.whatsapp.com/')
    input("Scan the QR code and press Enter after logging in...")

    for recipient_name in recipient_names:
        if recipient_name:
            search_bar = driver.find_element_by_xpath('//div[contains(@class, "copyable-text")]')
            search_bar.click()
            search_bar.send_keys(recipient_name)
            search_bar.send_keys(Keys.ENTER)

            time.sleep(2)

            # Check if a manual message is provided, if not, generate an AI message
            if manual_message.strip():
                message_text = manual_message
            else:
                # Generate a message using AI
                message_text = generate_message(recipient_name)

            message_input = driver.find_element_by_xpath('//div[contains(@class, "copyable-text")]')
            message_input.send_keys(message_text)

            if attachment_path:
                # Attach the file using pyautogui
                message_input.click()
                time.sleep(2)
                pyautogui.write(attachment_path)
                time.sleep(1)
                pyautogui.press('enter')

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

# Attachment Entry
attachment_label = tk.Label(root, text="Attachment (optional):")
attachment_label.pack()
attachment_entry = tk.Text(root, height=1, width=40)
attachment_entry.pack()

# Attach File Button
attach_button = tk.Button(root, text="Attach File", command=lambda: filedialog.askopenfilename())
attach_button.pack()

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

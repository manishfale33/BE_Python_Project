import tkinter as tk
from tkinter import ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import openai
import pyautogui
import re
from fbchat import Client
from fbchat.models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up your OpenAI API key
openai.api_key = 'Authorization: Bearer OPENAI_API_KEY'  # Replace with your actual API key

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
            
            # Use regular expressions to filter out mobile numbers (numeric entries)
            mobile_numbers = [number for number in numbers if re.match(r'^\d+$', number)]
            
            recipients_text.delete("1.0", tk.END)
            for number in mobile_numbers:
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
            search_bar = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
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

            message_input = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div')
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

# Function to send Facebook messages
def send_facebook_messages(username, password, recipients, message_text):
    # Initialize the Facebook client
    client = Client(username, password)

    try:
        for recipient in recipients:
            # Search for the recipient (by name or user ID)
            users = client.searchForUsers(recipient)
            if users:
                recipient_user = users[0]  # Assuming the first search result is the correct recipient
                message_id = client.send(Message(text=message_text), thread_id=recipient_user.uid, thread_type=ThreadType.USER)
                print(f"Message sent to {recipient_user.name} with ID: {message_id}")
            else:
                print(f"Recipient {recipient} not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Logout and close the client
    client.logout()

# Function to send Gmail messages
def send_gmail_messages(sender_email, sender_password, recipients, subject, message_text):
    try:
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to your Gmail account
        server.login(sender_email, sender_password)

        for recipient in recipients:
            # Create the email message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(message_text, "plain"))

            # Send the email
            server.sendmail(sender_email, recipient, message.as_string())
            print(f"Message sent to {recipient}")

        # Quit the server
        server.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to automate posting on Instagram
def post_on_instagram():
    username = username_entry.get()
    password = password_entry.get()
    image_path = image_path_entry.get()
    caption_text = caption_entry.get()

    # Set the path to your Chrome WebDriver executable
    webdriver_path = 'chromedriver.exe'  # Replace with the actual path

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(executable_path=webdriver_path)

    # Open Instagram
    driver.get('https://www.instagram.com/')

    # Wait for the page to load
    time.sleep(2)

    # Enter username and password
    username_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Log in
    login_button = driver.find_element_by_css_selector('button[type="submit"]')
    login_button.click()
    time.sleep(5)

    # Close the "Turn on Notifications" pop-up (if it appears)
    try:
        not_now_button = driver.find_element_by_css_selector('button[class="aOOlW   HoLwm "]')
        not_now_button.click()
    except:
        pass

    # Click the "New Post" button (camera icon)
    new_post_button = driver.find_element_by_css_selector('div[data-testid="new-post-button"]')
    new_post_button.click()
    time.sleep(2)

    # Upload the image
    image_input = driver.find_element_by_css_selector('input[type="file"]')
    image_input.send_keys(image_path)
    time.sleep(5)

    # Add caption (including hashtags)
    caption_input = driver.find_element_by_css_selector('textarea[aria-label="Write a caption…"]')
    caption_input.send_keys(caption_text)

    # Click the "Share" button
    share_button = driver.find_element_by_css_selector('button[type="submit"]')
    share_button.click()
    time.sleep(10)

    # Close the browser
    driver.quit()
    result_label.config(text="Post uploaded successfully.")

# Create the main window
root = tk.Tk()
root.title("Social Media Automation")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# WhatsApp Blaster Tab
whatsapp_tab = ttk.Frame(notebook)
notebook.add(whatsapp_tab, text="WhatsApp Blaster")

# Recipients Entry (loaded from CSV)
recipients_label = tk.Label(whatsapp_tab, text="Recipients:")
recipients_label.pack()
recipients_text = tk.Text(whatsapp_tab, height=10, width=40)
recipients_text.pack()

# Load Numbers Button
load_button = tk.Button(whatsapp_tab, text="Load Numbers", command=load_numbers)
load_button.pack()

# Message Entry
message_label = tk.Label(whatsapp_tab, text="Message:")
message_label.pack()
message_entry = tk.Text(whatsapp_tab, height=5, width=40)
message_entry.pack()

# Attachment Entry
attachment_label = tk.Label(whatsapp_tab, text="Attachment (optional):")
attachment_label.pack()
attachment_entry = tk.Text(whatsapp_tab, height=1, width=40)
attachment_entry.pack()

# Attach File Button
attach_button = tk.Button(whatsapp_tab, text="Attach File", command=lambda: filedialog.askopenfilename())
attach_button.pack()

# Send Messages Button
send_button = tk.Button(whatsapp_tab, text="Send Messages", command=lambda: threading.Thread(target=send_messages).start())
send_button.pack()

# Facebook Blaster Tab
facebook_tab = ttk.Frame(notebook)
notebook.add(facebook_tab, text="Facebook Blaster")

# Recipients Entry (for Facebook)
facebook_recipients_label = tk.Label(facebook_tab, text="Facebook Recipients:")
facebook_recipients_label.pack()
facebook_recipients_text = tk.Text(facebook_tab, height=10, width=40)
facebook_recipients_text.pack()

# Facebook Message Entry
facebook_message_label = tk.Label(facebook_tab, text="Facebook Message:")
facebook_message_label.pack()
facebook_message_entry = tk.Text(facebook_tab, height=5, width=40)
facebook_message_entry.pack()

# Send Facebook Messages Button
facebook_send_button = tk.Button(facebook_tab, text="Send Facebook Messages", command=lambda: threading.Thread(target=send_facebook_messages, args=(
    "your_facebook_username",
    "your_facebook_password",
    facebook_recipients_text.get("1.0", "end-1c").split('\n'),
    facebook_message_entry.get("1.0", "end-1c")
)).start())
facebook_send_button.pack()

# Gmail Blaster Tab
gmail_tab = ttk.Frame(notebook)
notebook.add(gmail_tab, text="Gmail Blaster")

# Recipients Entry (for Gmail)
gmail_recipients_label = tk.Label(gmail_tab, text="Gmail Recipients:")
gmail_recipients_label.pack()
gmail_recipients_text = tk.Text(gmail_tab, height=10, width=40)
gmail_recipients_text.pack()

# Gmail Subject Entry
gmail_subject_label = tk.Label(gmail_tab, text="Gmail Subject:")
gmail_subject_label.pack()
gmail_subject_entry = tk.Entry(gmail_tab)
gmail_subject_entry.pack()

# Gmail Message Entry
gmail_message_label = tk.Label(gmail_tab, text="Gmail Message:")
gmail_message_label.pack()
gmail_message_entry = tk.Text(gmail_tab, height=5, width=40)
gmail_message_entry.pack()

# Send Gmail Messages Button
gmail_send_button = tk.Button(gmail_tab, text="Send Gmail Messages", command=lambda: threading.Thread(target=send_gmail_messages, args=(
    "your@gmail.com",
    "your_password",
    gmail_recipients_text.get("1.0", "end-1c").split('\n'),
    gmail_subject_entry.get(),
    gmail_message_entry.get("1.0", "end-1c")
)).start())
gmail_send_button.pack()

# Instagram Tab
instagram_tab = ttk.Frame(notebook)
notebook.add(instagram_tab, text="Instagram Automation")

# Instagram Options
username_label = tk.Label(instagram_tab, text="Instagram Username:")
username_label.pack()
username_entry = tk.Entry(instagram_tab)
username_entry.pack()

password_label = tk.Label(instagram_tab, text="Instagram Password:")
password_label.pack()
password_entry = tk.Entry(instagram_tab, show='*')
password_entry.pack()

image_path_label = tk.Label(instagram_tab, text="Image Path:")
image_path_label.pack()
image_path_entry = tk.Entry(instagram_tab)
image_path_entry.pack()

caption_label = tk.Label(instagram_tab, text="Caption (optional):")
caption_label.pack()
caption_entry = tk.Entry(instagram_tab)
caption_entry.pack()

# Post on Instagram Button
post_button = tk.Button(instagram_tab, text="Post on Instagram", command=post_on_instagram)
post_button.pack()

# Result Label
result_label = tk.Label(root, text="")
result_label.pack()

# Function to close the browser and destroy the GUI window
def close_browser_and_exit():
    driver.quit()
    root.destroy()

# Bind the window close event to the close_browser_and_exit function
root.protocol("WM_DELETE_WINDOW", close_browser_and_exit)

# Start the GUI event loop
root.mainloop()

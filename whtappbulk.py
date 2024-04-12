import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl
import csv
import random

# Function to send a message using Selenium WebDriver
def send_message(driver, phone_number, message, attachment_path=None):
    driver.get("https://web.whatsapp.com")
    input("Scan the QR code and press Enter after logging in.")

    driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
    message_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="1"]')

    message_box.send_keys(message)
    
    if attachment_path:
        attachment_button = driver.find_element_by_xpath('//div[@title="Attach"]')
        attachment_button.click()
        
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN).perform()
        action.send_keys(Keys.ARROW_DOWN).perform()
        action.send_keys(Keys.ENTER).perform()
        
        file_input = driver.find_element_by_xpath('//input[@type="file"]')
        file_input.send_keys(attachment_path)
    
    message_box.send_keys(Keys.ENTER)
    print("Message sent successfully!")

# Function to generate a random message
def generate_random_message():
    messages = ["Hello!", "How are you?", "Good morning!", "Happy to connect!"]
    random_message = random.choice(messages)
    print(f"Generated random message: {random_message}")
    return random_message

# Function to handle button click
def send_message_button():
    selected_item = phone_tree.selection()
    message = message_entry.get()
    attachment_path = attachment_entry.get()
    
    if not message:
        message = generate_random_message()

    if selected_item:
        item = phone_tree.item(selected_item)
        phone_number = item['values'][1]
        send_message(driver, phone_number, message, attachment_path)

# Function to fetch phone numbers and contact names from CSV
def fetch_phone_contacts_from_csv(file_path):
    phone_contacts = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row:
                if len(row) == 2:
                    phone_contacts.append([row[0], row[1]])
                elif len(row) == 1:
                    phone_contacts.append(["", row[0]])
    print("Phone contacts fetched from CSV successfully!")
    return phone_contacts

# Function to fetch phone numbers and contact names from Excel
def fetch_phone_contacts_from_excel(file_path):
    phone_contacts = []
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        if row:
            if len(row) == 2:
                phone_contacts.append([row[0], row[1]])
            elif len(row) == 1:
                phone_contacts.append(["", str(row[0])])
    print("Phone contacts fetched from Excel successfully!")
    return phone_contacts

# Function to handle file selection and phone number fetching
def select_file_and_fetch_numbers():
    file_path = filedialog.askopenfilename()
    phone_tree.delete(*phone_tree.get_children())

    if file_path.endswith('.csv'):
        phone_contacts = fetch_phone_contacts_from_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        phone_contacts = fetch_phone_contacts_from_excel(file_path)

    for contact in phone_contacts:
        phone_tree.insert('', 'end', values=contact)
    print("File selected and phone numbers fetched successfully!")

# Function to handle attachment selection
def select_attachment():
    file_path = filedialog.askopenfilename()
    attachment_entry.delete(0, tk.END)
    attachment_entry.insert(0, file_path)
    print("Attachment selected successfully!")

# Create a Tkinter window
window = tk.Tk()
window.title("WhatsApp Auto Sender")

# Create a custom ttk style for the black and white theme
custom_style = ttk.Style()
custom_style.configure("Custom.TButton", foreground="white", background="black")
custom_style.configure("Custom.TEntry", foreground="black", background="white")
custom_style.configure("Custom.TLabel", foreground="black", background="white")
custom_style.configure("Custom.Treeview", foreground="black", background="white")

# Create and place GUI elements using the custom style
message_label = ttk.Label(window, text="Message (leave blank for random):", style="Custom.TLabel")
message_label.pack()
message_entry = ttk.Entry(window, style="Custom.TEntry")
message_entry.pack()

attachment_label = ttk.Label(window, text="Attachment Path:", style="Custom.TLabel")
attachment_label.pack()
attachment_entry = ttk.Entry(window, style="Custom.TEntry")
attachment_entry.pack()

select_attachment_button = ttk.Button(window, text="Select Attachment", command=select_attachment, style="Custom.TButton")
select_attachment_button.pack()

select_file_button = ttk.Button(window, text="Select CSV/Excel File", command=select_file_and_fetch_numbers, style="Custom.TButton")
select_file_button.pack()

phone_tree = ttk.Treeview(window, columns=("Name", "Phone"), style="Custom.Treeview")
phone_tree.heading("#1", text="Name")
phone_tree.heading("#2", text="Phone")
phone_tree.pack()

send_button = ttk.Button(window, text="Send Message", command=send_message_button, style="Custom.TButton")
send_button.pack()

# Initialize the WebDriver
driver = webdriver.Chrome()
print("WebDriver initialized successfully!")

# Start the Tkinter main loop
window.mainloop()

# Close the WebDriver when the GUI is closed
driver.quit()
print("WebDriver closed successfully!")

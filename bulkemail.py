import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_email():
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()
    recipients = recipients_text.get("1.0", "end-1c").split('\n')
    subject = subject_entry.get()
    message_text = message_entry.get("1.0", "end-1c")

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open Gmail login page
        driver.get("https://mail.google.com")

        # Wait for the login form to load
        email_field = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_field.send_keys(sender_email)
        email_field.send_keys(Keys.RETURN)

        # Wait for the password field to appear
        password_field = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(sender_password)
        password_field.send_keys(Keys.RETURN)

        # Compose an email
        compose_button = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='button'][gh='cm']"))
        )
        compose_button.click()

        # Wait for the email composition form to load
        to_field = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "to"))
        )
        to_field.send_keys(", ".join(recipients))
        to_field.send_keys(Keys.RETURN)

        subject_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "subjectbox"))
        )
        subject_field.send_keys(subject)

        message_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        message_field.send_keys(message_text)

        # Send the email
        send_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Send ‪(Ctrl-Enter)‬']"))
        )
        send_button.click()

        print("Email sent successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Create the main window
root = tk.Tk()
root.title("Gmail Automation")

# Create a custom style for ttk
custom_style = ttk.Style()

# Define custom colors (black and blue theme)
custom_style.configure("Custom.TButton", foreground="white", background="blue")
custom_style.configure("Custom.TEntry", foreground="black", background="white")
custom_style.configure("Custom.TLabel", foreground="white", background="black")

# Gmail Tab
gmail_tab = ttk.Frame(root)
gmail_tab.pack()

# Sender Email Entry
sender_email_label = ttk.Label(gmail_tab, text="Your Email:", style="Custom.TLabel")
sender_email_label.pack()
sender_email_entry = ttk.Entry(gmail_tab, style="Custom.TEntry")
sender_email_entry.pack()

# Sender Password Entry
sender_password_label = ttk.Label(gmail_tab, text="Your Password:", style="Custom.TLabel")
sender_password_label.pack()
sender_password_entry = ttk.Entry(gmail_tab, show='*', style="Custom.TEntry")
sender_password_entry.pack()

# Recipients Entry
recipients_label = ttk.Label(gmail_tab, text="Recipients (One per line):", style="Custom.TLabel")
recipients_label.pack()
recipients_text = tk.Text(gmail_tab, height=10, width=40)
recipients_text.pack()

# Subject Entry
subject_label = ttk.Label(gmail_tab, text="Email Subject:", style="Custom.TLabel")
subject_label.pack()
subject_entry = ttk.Entry(gmail_tab, style="Custom.TEntry")
subject_entry.pack()

# Message Entry
message_label = ttk.Label(gmail_tab, text="Email Message:", style="Custom.TLabel")
message_label.pack()
message_entry = tk.Text(gmail_tab, height=5, width=40, bg="white", fg="black")
message_entry.pack()

# Send Email Button
send_button = ttk.Button(gmail_tab, text="Send Email", command=send_email, style="Custom.TButton")
send_button.pack()

# Start the GUI event loop
root.mainloop()

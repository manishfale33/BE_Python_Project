import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

        # Find and interact with the email and password fields
        email_field = driver.find_element(By.ID,"identifierId")
        email_field.send_keys(sender_email)
        email_field.send_keys(Keys.RETURN)

        # Wait for the password field to appear
        driver.implicitly_wait(10)
        password_field = driver.find_element(By.NAME,"password")
        password_field.send_keys(sender_password)
        password_field.send_keys(Keys.RETURN)

        # Compose an email
        compose_button = driver.find_element(By.CSS_SELECTOR,"div[role='button'][gh='cm']")
        compose_button.click()
        driver.implicitly_wait(5)

        to_field = driver.find_element_by_name("to")
        to_field.send_keys(", ".join(recipients))
        to_field.send_keys(Keys.RETURN)

        subject_field = driver.find_element(By.NAME,"subjectbox")
        subject_field.send_keys(subject)

        message_field = driver.find_element(By.CSS_SELECTOR,"div[role='textbox']")
        message_field.send_keys(message_text)

        # Send the email
        send_button = driver.find_element(By.CSS_SELECTOR,"div[aria-label='Send ‪(Ctrl-Enter)‬']")
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

# Gmail Tab
gmail_tab = ttk.Frame(root)
gmail_tab.pack()

# Sender Email Entry
sender_email_label = tk.Label(gmail_tab, text="Your Email:")
sender_email_label.pack()
sender_email_entry = tk.Entry(gmail_tab)
sender_email_entry.pack()

# Sender Password Entry
sender_password_label = tk.Label(gmail_tab, text="Your Password:")
sender_password_label.pack()
sender_password_entry = tk.Entry(gmail_tab, show='*')
sender_password_entry.pack()

# Recipients Entry
recipients_label = tk.Label(gmail_tab, text="Recipients (One per line):")
recipients_label.pack()
recipients_text = tk.Text(gmail_tab, height=10, width=40)
recipients_text.pack()

# Subject Entry
subject_label = tk.Label(gmail_tab, text="Email Subject:")
subject_label.pack()
subject_entry = tk.Entry(gmail_tab)
subject_entry.pack()

# Message Entry
message_label = tk.Label(gmail_tab, text="Email Message:")
message_label.pack()
message_entry = tk.Text(gmail_tab, height=5, width=40)
message_entry.pack()

# Send Email Button
send_button = tk.Button(gmail_tab, text="Send Email", command=send_email)
send_button.pack()

# Start the GUI event loop
root.mainloop()

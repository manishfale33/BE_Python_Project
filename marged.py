import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        email_field = driver.find_element(By.ID, "identifierId")
        email_field.send_keys(sender_email)
        email_field.send_keys(Keys.RETURN)

        # Wait for the password field to appear
        driver.implicitly_wait(10)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(sender_password)
        password_field.send_keys(Keys.RETURN)

        # Compose an email
        compose_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][gh='cm']")
        compose_button.click()
        driver.implicitly_wait(5)

        to_field = driver.find_element_by_name("to")
        to_field.send_keys(", ".join(recipients))
        to_field.send_keys(Keys.RETURN)

        subject_field = driver.find_element(By.NAME, "subjectbox")
        subject_field.send_keys(subject)

        message_field = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
        message_field.send_keys(message_text)

        # Send the email
        send_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Send ‪(Ctrl-Enter)‬']")
        send_button.click()

        print("Email sent successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

def send_facebook_message_with_attachment():
    username = username_entry.get()
    password = password_entry.get()
    recipient = recipient_entry.get()
    message_text = message_entry.get("1.0", tk.END)
    attachment_path = attachment_entry.get()

    driver = webdriver.Chrome()

    try:
        driver.get("https://www.facebook.com")

        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pass")))
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        login_button.click()

        WebDriverWait(driver, 50).until(EC.url_contains("https://www.facebook.com/"))

        if "login" in driver.current_url:
            print("Login failed. Please check your credentials.")
            return

        # Search for the recipient by name
        search_box = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        search_box.send_keys(recipient)
        search_box.send_keys(Keys.RETURN)

        # Handle any popups (if they appear)
        try:
            popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
            # You can add code here to close the popup (e.g., by clicking the cancel icon)
            cancel_icon = WebDriverWait(popup, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[@aria-label='Cancel']")))
            cancel_icon.click()
        except Exception as e:
            # Handle the case when no popup is present
            pass

        # Click on the message button
        message_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@aria-label, 'Message')]")))
        message_button.click()

        # Enter the message
        message_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
        message_input.send_keys(message_text)

        # Attach a file if specified
        if attachment_path:
            attachment_input = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            attachment_input.send_keys(attachment_path)

        # Send the message
        message_input.send_keys(Keys.RETURN)

        print("Message sent successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

# Create the main window
root = tk.Tk()
root.title("Messaging Automation")

# Create a tab control to switch between Gmail and Facebook
tab_control = ttk.Notebook(root)
tab_control.pack()

# Gmail Tab
gmail_tab = ttk.Frame(tab_control)
tab_control.add(gmail_tab, text="Gmail")

# Gmail UI components
sender_email_label = tk.Label(gmail_tab, text="Your Email:")
sender_email_label.pack()
sender_email_entry = tk.Entry(gmail_tab)
sender_email_entry.pack()

sender_password_label = tk.Label(gmail_tab, text="Your Password:")
sender_password_label.pack()
sender_password_entry = tk.Entry(gmail_tab, show='*')
sender_password_entry.pack()

recipients_label = tk.Label(gmail_tab, text="Recipients (One per line):")
recipients_label.pack()
recipients_text = tk.Text(gmail_tab, height=10, width=40)
recipients_text.pack()

subject_label = tk.Label(gmail_tab, text="Email Subject:")
subject_label.pack()
subject_entry = tk.Entry(gmail_tab)
subject_entry.pack()

message_label = tk.Label(gmail_tab, text="Email Message:")
message_label.pack()
message_entry = tk.Text(gmail_tab, height=5, width=40)
message_entry.pack()

send_gmail_button = tk.Button(gmail_tab, text="Send Email", command=send_email)
send_gmail_button.pack()

# Facebook Tab
facebook_tab = ttk.Frame(tab_control)
tab_control.add(facebook_tab, text="Facebook")

# Facebook UI components
username_label = tk.Label(facebook_tab, text="Facebook Email/Phone:")
username_label.pack()
username_entry = tk.Entry(facebook_tab)
username_entry.pack()

password_label = tk.Label(facebook_tab, text="Facebook Password:")
password_label.pack()
password_entry = tk.Entry(facebook_tab, show='*')
password_entry.pack()

recipient_label = tk.Label(facebook_tab, text="Recipient's Facebook Name:")
recipient_label.pack()
recipient_entry = tk.Entry(facebook_tab)
recipient_entry.pack()

message_label = tk.Label(facebook_tab, text="Message:")
message_label.pack()
message_entry = tk.Text(facebook_tab, height=5, width=40)
message_entry.pack()

attachment_label = tk.Label(facebook_tab, text="Attachment Path (optional):")
attachment_label.pack()
attachment_entry = tk.Entry(facebook_tab)
attachment_entry.pack()

send_facebook_button = tk.Button(facebook_tab, text="Send Facebook Message with Attachment", command=send_facebook_message_with_attachment)
send_facebook_button.pack()

# Start the GUI event loop
root.mainloop()

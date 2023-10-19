import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

        # Handle site notifications (if they appear)
        handle_notifications(driver)

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

def handle_notifications(driver):
    try:
        # Wait for the notification dialog to appear
        notification_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
        
        # You can add code here to block or dismiss the notification
        # For example, clicking the "Block" button
        block_button = WebDriverWait(notification_dialog, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Block')]")))
        block_button.click()
        
    except Exception as e:
        # Handle the case when no notification dialog is present
        pass

root = tk.Tk()
root.title("Facebook Message Sender")

facebook_tab = ttk.Frame(root)
facebook_tab.pack()

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

send_button = tk.Button(facebook_tab, text="Send Facebook Message with Attachment", command=send_facebook_message_with_attachment)
send_button.pack()

root.mainloop()

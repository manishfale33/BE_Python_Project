import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def send_facebook_messages():
    username = username_entry.get()
    password = password_entry.get()
    recipient = recipient_entry.get()
    message_text = message_entry.get("1.0", tk.END) 

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open Facebook login page
        driver.get("https://www.facebook.com")

        # Find and interact with the email/phone and password fields
        email_field = driver.find_element_by_id("email")
        email_field.send_keys(username)

        password_field = driver.find_element_by_id("pass")
        password_field.send_keys(password)

        login_button = driver.find_element_by_id("loginbutton")
        login_button.click()

        # Wait for login to complete
        driver.implicitly_wait(10)

        # Go to the recipient's profile (replace with the recipient's profile URL)
        driver.get(f"https://www.facebook.com/{recipient}")

        # Click on the message button
        message_button = driver.find_element_by_css_selector("a[data-testid='chat_sidebar']")
        message_button.click()

        # Enter the message and send
        message_input = driver.find_element_by_css_selector("div[role='combobox']")
        message_input.send_keys(message_text)
        message_input.send_keys(Keys.RETURN)

        print("Message sent successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Create the main window
root = tk.Tk()
root.title("Facebook Message Sender")

# Facebook Tab
facebook_tab = ttk.Frame(root)
facebook_tab.pack()

# Username Entry
username_label = tk.Label(facebook_tab, text="Facebook Email/Phone:")
username_label.pack()
username_entry = tk.Entry(facebook_tab)
username_entry.pack()

# Password Entry
password_label = tk.Label(facebook_tab, text="Facebook Password:")
password_label.pack()
password_entry = tk.Entry(facebook_tab, show='*')
password_entry.pack()

# Recipient Entry
recipient_label = tk.Label(facebook_tab, text="Recipient's Facebook Profile (Username or ID):")
recipient_label.pack()
recipient_entry = tk.Entry(facebook_tab)
recipient_entry.pack()

# Message Entry
message_label = tk.Label(facebook_tab, text="Message:")
message_label.pack()
message_entry = tk.Text(facebook_tab, height=5, width=40)
message_entry.pack()

# Send Facebook Message Button
send_button = tk.Button(facebook_tab, text="Send Facebook Message", command=send_facebook_messages)
send_button.pack()

# Start the GUI event loop
root.mainloop()

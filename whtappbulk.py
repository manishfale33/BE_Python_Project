import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# Function to send bulk messages
def send_bulk_messages():
    # Load the chrome driver
    driver = webdriver.Chrome()
    count = 0

    # Open WhatsApp URL in chrome browser
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 20)

    # Get input values from the user
    excel_file_path = excel_path_entry.get()
    contact_message = message_entry.get()

    try:
        excel_data = pd.read_excel(excel_file_path, sheet_name='Customers')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read Excel file: {str(e)}")
        driver.quit()
        return

    # Iterate through Excel rows
    for column in excel_data['Name'].tolist():
        # Assign customized message
        message = contact_message.replace('{customer_name}', column)

        # Locate search box through x_path
        search_box = '//*[@id="side"]/div[1]/div/label/div/div[2]'
        person_title = wait.until(lambda driver: driver.find_element_by_xpath(search_box))

        # Clear search box if any contact number is written in it
        person_title.clear()

        # Send contact number in search box
        person_title.send_keys(str(excel_data['Contact'][count]))
        count = count + 1

        # Wait for 2 seconds to search contact number
        time.sleep(2)

        try:
            # Load error message in case of unavailability of contact number
            element = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/span')
        except NoSuchElementException:
            person_title.send_keys(Keys.ENTER)
            actions = ActionChains(driver)
            actions.send_keys(message)
            actions.send_keys(Keys.ENTER)
            actions.perform()

    # Close chrome browser
    driver.quit()

# Create the main window
root = tk.Tk()
root.title("WhatsApp Bulk Messenger")

# Create and place entry fields and labels for user input
excel_path_label = tk.Label(root, text="Excel File Path:")
excel_path_label.pack(pady=5)
excel_path_entry = tk.Entry(root)
excel_path_entry.pack(pady=5)

message_label = tk.Label(root, text="Customized Message (Use '{customer_name}' to insert customer names):")
message_label.pack(pady=5)
message_entry = tk.Entry(root)
message_entry.pack(pady=5)

# Create and place a button to send bulk messages
send_button = tk.Button(root, text="Send Bulk Messages", command=send_bulk_messages)
send_button.pack(pady=10)

# Run the Tkinter main event loop
root.mainloop()

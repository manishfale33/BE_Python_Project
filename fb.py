import time
from tkinter import *
from tkinter import ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class FacebookMessageSender:
    def __init__(self, root):
        self.root = root
        root.title("Facebook Message Sender")

        # Apply your custom black and blue theme
        root.tk_setPalette(background="#000000", foreground="#00A0E6")  # Black background, blue foreground
        root.option_add("*TButton*highlightColor", "blue")  # Customize button highlight color

        # Define custom colors
        dark_background = "#000000"
        text_color = "#00A0E6"

        self.username_label = Label(root, text="Facebook Email/Phone:", fg=text_color, bg=dark_background)
        self.username_label.grid(row=0, column=0, sticky=W)
        self.username_entry = ttk.Entry(root, style="Custom.TEntry")  # Use themed entry widget
        self.username_entry.grid(row=0, column=1, sticky=W)

        self.password_label = Label(root, text="Facebook Password:", fg=text_color, bg=dark_background)
        self.password_label.grid(row=1, column=0, sticky=W)
        self.password_entry = ttk.Entry(root, show="*", style="Custom.TEntry")  # Use themed entry widget
        self.password_entry.grid(row=1, column=1, sticky=W)

        self.recipient_label = Label(root, text="Recipient's Facebook Name:", fg=text_color, bg=dark_background)
        self.recipient_label.grid(row=2, column=0, sticky=W)
        self.recipient_entry = ttk.Entry(root, style="Custom.TEntry")  # Use themed entry widget
        self.recipient_entry.grid(row=2, column=1, sticky=W)

        self.message_label = Label(root, text="Message:", fg=text_color, bg=dark_background)
        self.message_label.grid(row=3, column=0, sticky=W)
        self.message_entry = Text(root, height=5, width=40, bg=dark_background, fg=text_color)
        self.message_entry.grid(row=3, column=1, columnspan=2, sticky=W)

        self.attachment_label = Label(root, text="Attachment Path (optional):", fg=text_color, bg=dark_background)
        self.attachment_label.grid(row=4, column=0, sticky=W)
        self.attachment_entry = ttk.Entry(root, style="Custom.TEntry")  # Use themed entry widget
        self.attachment_entry.grid(row=4, column=1, sticky=W)

        self.attach_label = Label(root, text="Attachment:", fg=text_color, bg=dark_background)
        self.attach_label.grid(row=5, column=0, sticky=W)

        self.attachment_button = PhotoImage(file="Images/search.png").subsample(10)  # Resized image
        self.browse_button = Button(root, image=self.attachment_button, command=self.browse_for_attachment, borderwidth=0, bg=dark_background)
        self.browse_button.grid(row=5, column=1, sticky=E)

        self.send_image = PhotoImage(file="Images/send.png").subsample(10)  # Resized image
        self.send_button = Button(root, image=self.send_image, command=self.send_message_or_friend_request, borderwidth=0, bg=dark_background)
        self.send_button.grid(row=5, column=2, sticky=W)

        # Create a custom style for themed entry widgets
        self.custom_style = ttk.Style()
        self.custom_style.configure("Custom.TEntry", foreground=text_color, background=dark_background)

        # Make the application responsive
        for i in range(6):
            root.rowconfigure(i, weight=1)
        for i in range(3):
            root.columnconfigure(i, weight=1)

        # Set the initial window size
        root.geometry("600x400")

    def browse_for_attachment(self):
        file_path = filedialog.askopenfilename()
        self.attachment_entry.delete(0, END)
        self.attachment_entry.insert(0, file_path)

    def send_message_or_friend_request(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        recipient = self.recipient_entry.get()
        message_text = self.message_entry.get("1.0", END).strip()
        attachment_path = self.attachment_entry.get()

        # Chrome WebDriver options with --disable-notifications argument
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

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
            search_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            search_box.send_keys(recipient)
            time.sleep(2)  # Adding a delay for search results to load
            search_box.send_keys(Keys.RETURN)

            # Handle site notifications (if they appear)
            self.handle_notifications(driver)

            # Check if the recipient is a friend
            try:
                friend_button_xpath = "//div[@data-click='profile_icon']//span[text()='Friends']"
                friend_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, friend_button_xpath)))
                # If the recipient is already a friend, send a message
                self.send_message(driver, message_text, attachment_path)
            except:
                # If the recipient is not a friend, send a friend request first
                friend_request_button_xpath = "//button[text()='Add Friend']"
                friend_request_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, friend_request_button_xpath)))
                friend_request_button.click()
                print("Friend request sent.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            driver.quit()

    def send_message(self, driver, message_text, attachment_path):
        try:
            # Wait for the "Message" button to be clickable
            message_button_xpath = "//a[contains(@href, 'messages')]"
            message_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, message_button_xpath)))
            message_button.click()

            # Enter the message
            message_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            message_input.send_keys(message_text)

            # Attach a file if specified
            if attachment_path:
                attachment_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                attachment_input.send_keys(attachment_path)

            # Send the message
            send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Send']")))
            send_button.click()

            print("Message sent successfully")

        except Exception as e:
            print(f"An error occurred while sending the message: {str(e)}")

    def handle_notifications(self, driver):
        try:
            # Wait for the notification dialog to appear
            notification_dialog = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
            
            # You can add code here to block or dismiss the notification
            # For example, clicking the "Block" button
            block_button = WebDriverWait(notification_dialog, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Block')]")))
            block_button.click()
            
        except Exception as e:
            print(f"An error occurred while handling notifications: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = FacebookMessageSender(root)
    root.mainloop()

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

        # Create labels and entry fields for username, password, recipient, message, and attachment
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

        # Create browse button for attachment
        self.attachment_button = PhotoImage(file="Images/search.png").subsample(10)  # Resized image
        self.browse_button = Button(root, image=self.attachment_button, command=self.browse_for_attachment, borderwidth=0, bg=dark_background)
        self.browse_button.grid(row=5, column=1, sticky=E)

        # Create send button for sending message or friend request
        self.send_image = PhotoImage(file="Images/send.png").subsample(10)  # Resized image
        self.send_button = Button(root, image=self.send_image, command=self.send_message, borderwidth=0, bg=dark_background)
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
        # Function to browse and select a file for attachment
        file_path = filedialog.askopenfilename()
        self.attachment_entry.delete(0, END)
        self.attachment_entry.insert(0, file_path)

    def send_message(self):
        # Function to send a message on Facebook
        username = self.username_entry.get()
        password = self.password_entry.get()
        recipient = self.recipient_entry.get()
        message_text = self.message_entry.get("1.0", END).strip()
        attachment_path = self.attachment_entry.get()

        print("Starting the message sending process...")

        # Chrome WebDriver options with --disable-notifications argument
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            print("Opening Facebook login page...")
            driver.get("https://www.facebook.com")

            print("Entering username...")
            email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.send_keys(username)

            print("Entering password...")
            password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pass")))
            password_field.send_keys(password)

            print("Logging in...")
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
            login_button.click()

            WebDriverWait(driver, 50).until(EC.url_contains("https://www.facebook.com/"))

            if "login" in driver.current_url:
                print("Login failed. Please check your credentials.")
                return

            print("Logged in successfully.")

            # Search for the recipient by name
            print(f"Searching for '{recipient}'...")
            search_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            search_box.send_keys(recipient)
            time.sleep(2)  # Adding a delay for search results to load
            search_box.send_keys(Keys.RETURN)

            # Handle site notifications (if they appear)
            self.handle_notifications(driver)

            # Click on the profile icon of the searched person
            profile_icon_xpath = "//body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/h2[1]/span[1]/span[1]/span[1]/a[1]/span[1]"
            profile_icon = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, profile_icon_xpath)))
            profile_icon.click()

# Click the message button
            message_button_xpath = "//span[contains(text(),'Message')]"
            message_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, message_button_xpath)))
            message_button.click()

            # Wait for the message box to load
            message_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body._6s5d._71pn.system-fonts--body.segoe:nth-child(2) div.x9f619.x1n2onr6.x1ja2u2z div.x1ey2m1c.xds687c.xixxii4:nth-child(1) div.xuk3077.x78zum5.xc8icb0:nth-child(1) div.x1ey2m1c.x78zum5.x164qtfw.xixxii4.x1vjfegm:nth-child(1) div.x9f619.x1n2onr6.x1ja2u2z.__fb-light-mode.x78zum5.xdt5ytf.x1iyjqo2.xs83m0k.x193iq5w div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj div.x5yr21d.x1uvtmcs div.xcrg951.xgqcy7u.x1lq5wgf.x78zum5.x6prxxf.xvq8zen.x17adc0v.xi55695.x1rgmuzj.xbbk1sx.x6l8u58 div.x78zum5.xdt5ytf.x1iyjqo2.x193iq5w.x2lwn1j.x1n2onr6:nth-child(2) div.xuk3077.x57kliw.x78zum5.x6prxxf.xz9dl7a.xsag5q8 div.x1iyjqo2.xw2csxc.x1n2onr6:nth-child(2) div.x78zum5.x1iyjqo2.x6q2ic0:nth-child(4) div.x16sw7j7.x107yiy2.xv8uw2v.x1tfwpuw.x2g32xy.x9f619.xlai7qp.x1iyjqo2.xeuugli div.x78zum5.x13a6bvl div.x78zum5.x1iyjqo2.xq8finb.x16n37ib.x1xmf6yo.x1e56ztr.xeuugli.x1n2onr6 div.xzsf02u.x1a2a7pz.x1n2onr6.x14wi4xw.x1iyjqo2.x1gh3ibb.xisnujt.xeuugli.x1odjw0f.notranslate > p.xat24cr.xdj266r")))

            # Enter the message directly into the message box
            print("Typing message...")
            message_box.send_keys(message_text)

            # Attach a file if specified
            if attachment_path:
                attachment_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                attachment_input.send_keys(attachment_path)
                time.sleep(2)  # Adding a delay for the attachment to upload

            # Click the send button
            print("Sending the message...")
            send_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body._6s5d._71pn.system-fonts--body.segoe:nth-child(3) div.x9f619.x1n2onr6.x1ja2u2z div.x1ey2m1c.xds687c.xixxii4:nth-child(1) div.xuk3077.x78zum5.xc8icb0:nth-child(1) div.x1ey2m1c.x78zum5.x164qtfw.xixxii4.x1vjfegm:nth-child(1) div.x9f619.x1n2onr6.x1ja2u2z.__fb-light-mode.x78zum5.xdt5ytf.x1iyjqo2.xs83m0k.x193iq5w div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj div.x5yr21d.x1uvtmcs div.xcrg951.xgqcy7u.x1lq5wgf.x78zum5.xdt5ytf.x6prxxf.xvq8zen.x17adc0v.xi55695.x1rgmuzj.xbbk1sx.x6l8u58 div.x78zum5.xdt5ytf.x1iyjqo2.x193iq5w.x2lwn1j.x1n2onr6:nth-child(2) div:nth-child(2) div:nth-child(1) div.xuk3077.x57kliw.x78zum5.x6prxxf.xz9dl7a.xsag5q8 span.x4k7w5x.x1h91t0o.x1h9r5lt.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j.x3nfvp2:nth-child(3) > div.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.xe8uvvx.xdj266r.xat24cr.x2lwn1j.xeuugli.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x3nfvp2.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1c4vz4f.x2lah0s.xsgj6o6.xw3qccf.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha")))
            send_button.click()
            print("Message sent successfully")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            driver.quit()

    def handle_notifications(self, driver):
        # Function to handle Facebook site notifications
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Not Now')]"))).click()
        except:
            pass

root = Tk()
app = FacebookMessageSender(root)
root.mainloop()
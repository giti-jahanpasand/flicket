import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", None)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", None)


class WebsiteBot:
    def __init__(self, bsse_url, login_page, headless=True):
        self.bsse_url = bsse_url
        self.login_page = bsse_url + login_page
        options = Options()
        if headless:
            options.add_argument("--headless")  # Enables headless mode
            options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")  # Set Chrome log level to ERROR
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Set wait time to 10 seconds

    def run(self):
        try:
            self.driver.get(self.login_page)

            # Wait for username and password fields to be visible
            username = self.wait.until(EC.visibility_of_element_located((By.ID, 'username')))
            password = self.wait.until(EC.visibility_of_element_located((By.ID, 'password')))
            username.send_keys(ADMIN_EMAIL)
            password.send_keys(ADMIN_PASSWORD)

            login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "login")))
            login_btn.click()

            tickets_link = self.wait.until(EC.element_to_be_clickable((By.ID, "ticketsLink")))
            tickets_link.click()
            ticket_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.row .border')))
            tickets_to_reply = []
            for ticket in ticket_elements:
                # Extract the ticket link
                link = ticket.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                # Extract the ticket status
                status = ticket.find_element(By.XPATH,
                                             ".//div[contains(text(), 'status')]//following-sibling::div").text
                if status == 'Open':
                    tickets_to_reply.append(link)
            for link in tickets_to_reply:
                self.driver.get(link)
                attachment_links = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.flicket-tickets-title')))

                for att in attachment_links:
                    # Get the href attribute of the link
                    file_link = att.get_attribute('href')

                    # Open the file link in a new tab
                    self.driver.execute_script("window.open(arguments[0]);", file_link)

                    # Switch to the new tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    # Wait for the file to load (add specific waiting logic if needed)
                    time.sleep(2)  # Adjust as needed depending on the file type and load time
d
                    # Close the current tab after viewing the file
                    self.driver.close()

                    # Switch back to the main ticket tab
                    self.driver.switch_to.window(self.driver.window_handles[0])
                # Wait for the text area to be visible
                text_area = self.wait.until(EC.visibility_of_element_located((By.ID, 'flask-pagedown-content')))
                text_area.send_keys('we are working on it')

                # Wait for the select element to be visible
                select_element = self.wait.until(EC.visibility_of_element_located((By.ID, 'status')))
                select = Select(select_element)
                select.select_by_value('3')

                # Wait for the submit button to be clickable
                submit_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                submit_button.click()
        finally:
            self.driver.quit()  # Close the browser at the end of the run method
    
if __name__ == "__main__":

    print("The bot is running. Press Ctrl+C to stop.")
    try:
        while True:
            bot = WebsiteBot("http://127.0.0.1:5000/", 'login', False)
            bot.run()  # Run the bot logic
            time.sleep(300)  # Wait for 5 minutes (300 seconds)
    except KeyboardInterrupt:
        print("Stopping the bot...")
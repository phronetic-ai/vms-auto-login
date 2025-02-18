import sys
import json
import os
import time
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

COMMON_FILE = "a.txt"

def setup_browser():
    """Sets up the Selenium WebDriver using WebDriver Manager."""
    browser_options = Options()
    browser_options.add_argument("--start-maximized")  # Ensure the browser opens in full-screen mode
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options)
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=browser_options)
    return driver

def login(driver, vms_data):
    """Automates the login process."""
    driver.get(vms_data['url'])

    time.sleep(90)

    # Locate the username field and enter the username
    username_field = driver.find_element(By.ID, "loginUsername-inputEl")
    username_field.send_keys(vms_data['username'])

    # Locate the password field and enter the password
    password_field = driver.find_element(By.ID, "loginPassword-inputEl")
    password_field.send_keys(vms_data['password'])

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    time.sleep(50)

    # Perform additional actions after login
    menu_selection = driver.find_element(By.XPATH, '//*[@id="dataview-1044"]/div/div[1]')
    menu_selection.click()

    time.sleep(50)

    d1_selection = driver.find_element(By.ID, 'splitbutton-1286-btnInnerEl')
    d1_selection.click()

    time.sleep(2)

    d3_selection = driver.find_element(By.ID, 'splitbutton-1288-btnInnerEl')
    d3_selection.click()

    time.sleep(2)

    d5_selection = driver.find_element(By.ID, 'splitbutton-1290-btnInnerEl')
    d5_selection.click()

    time.sleep(2)

    d4_selection = driver.find_element(By.ID, 'splitbutton-1289-btnInnerEl')
    d4_selection.click()

    time.sleep(2)

    pyautogui.press('f11')

    time.sleep(2)

    full_screen_selection = driver.find_element(By.ID, 'button-1239-btnIconEl')
    full_screen_selection.click()

def main():
    driver = setup_browser()
    vms_data = json.loads(sys.argv[1])
    try:
        login(driver, vms_data)
        print("Child script completed. Browser will remain open.")
        while os.path.exists(COMMON_FILE):
            time.sleep(5)  # Keep the browser running indefinitely
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
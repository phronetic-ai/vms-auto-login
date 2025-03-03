import sys
import json
import os
import time
import pyautogui
import io
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

COMMON_FILE = "a.txt"
UGROUND_URL = "http://164.52.217.202/uground/get_coordinates"

def get_coordinates(image, description):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    files = {
        'image': ('image.png', img_byte_arr, 'image/png')
    }
    data = {
        'description': description
    }
    response = requests.post(UGROUND_URL, files=files, data=data)
    coordinates = response.json()['coordinates']
    return coordinates['x'], coordinates['y']

def setup_browser(browser):
    """Sets up the Selenium WebDriver using WebDriver Manager."""
    driver = None
    if browser == 'chrome':
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        browser_options = Options()
        browser_options.add_argument("--start-maximized") # Ensure the browser opens in full-screen mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options)
    elif browser == 'edge':
        from selenium.webdriver.edge.service import Service
        from selenium.webdriver.edge.options import Options
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        browser_options = Options()
        browser_options.add_argument("--start-maximized") # Ensure the browser opens in full-screen mode
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=browser_options)
    else:
        print(f"[ERROR] Invalid browser - {browser}")
    return driver

def login(driver):
    """Automates the login process."""
    url = "https://abm.phronetic.ai/video-meet/signin"
    driver.get(url)

    time.sleep(10)

    username = "jd"
    email = "johndoe@gmail.com"
    password = "johndoe123*"
    webroom_id = "66b22393ddb4db826b928bc1"

    email_field = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[1]/div/div[2]/form/div/div[1]/input')
    email_field.send_keys(email)

    time.sleep(10)

    password_field = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[1]/div/div[2]/form/div/div[2]/input')
    password_field.send_keys(password)

    time.sleep(10)

    password_field.send_keys(Keys.RETURN)

    time.sleep(10)

    meeting_field = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/form/input')
    meeting_field.send_keys(webroom_id)

    time.sleep(10)

    join_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/form/button[1]')
    join_btn.click()

    time.sleep(10)

    username_field = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/form/div[1]/div[2]/div[1]/input')
    username_field.send_keys(username)

    time.sleep(10)

    join_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/form/div[2]/button[2]')
    join_btn.click()

    time.sleep(10)

    share_screen_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]')
    share_screen_btn.click()

    time.sleep(10)

    ref_img = pyautogui.screenshot()
    x, y = get_coordinates(ref_img, "Locate the 'Block' button")
    print(f"X-{x} && Y-{y}")
    pyautogui.click(x, y)

    time.sleep(5)
    pyautogui.click(x, y)

    time.sleep(5)

    x, y = get_coordinates(ref_img, "Locate the 'Entire screen' tab option")
    print(f"X-{x} && Y-{y}")
    pyautogui.click(x, y)

    time.sleep(5)

    ref_img = pyautogui.screenshot()
    x, y = get_coordinates(ref_img, "Locate the 'Entire screen' text that is below the image block around the centre")
    print(f"X-{x} && Y-{y}")
    pyautogui.click(x, y)

    time.sleep(5)

    x, y = get_coordinates(ref_img, "Locate the 'Share' button")
    print(f"X-{x} && Y-{y}")
    pyautogui.click(x, y)

    time.sleep(50)

def test():
    image = pyautogui.screenshot()
    print(get_coordinates(image,"Locate the word 'system'"))
    # time.sleep(5)
    # pyautogui.moveTo(288,195)
    # pyautogui.moveTo(288,222)
    # pyautogui.moveTo(1152,178)
    # time.sleep(5)
    # pyautogui.moveTo(1152,203)
    # time.sleep(5)
    # pyautogui.moveTo(835, 451)
    # pyautogui.moveTo(1207, 608)

def main():
    # test()
    # return
    driver = setup_browser(browser="chrome")
    if driver:
        login(driver)
        # test()
        driver.quit()

if __name__ == "__main__":
    main()
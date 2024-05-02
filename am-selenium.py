from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keyboard = Controller()

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://chat.openai.com/")
driver.implicitly_wait(10)
#Login
# Get to Login Page
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div/nav/div[2]/div[2]/button[2]").click()
# Type Email and click "Continue" button
driver.find_element(By.ID, "email-input") # Add your ChatGPT Account Email Address in "send_keys"
ActionChains(driver)\
  .send_keys("")\
  .perform()
driver.find_element(By.CLASS_NAME, "continue-btn").click()
# Type Password and Submit Form
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "password")))
driver.find_element(By.ID, "password") # Add your ChatGPT Account Password in "send_keys"
ActionChains(driver)\
  .send_keys("")\
  .perform()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/div/div/div/form/div[2]/button"))).click()
# Get to ChatGPT-4
#  Wait for element to be displayed to bypass "Are you a robot?" Prompt
revealed = driver.find_element(By.XPATH, "//*[@id=\"prompt-textarea\"]")
WebDriverWait(driver, 50).until(lambda d: revealed.is_displayed())
driver.get("https://chat.openai.com/?model=gpt-4")

#Begin File Upload
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/form/div/div[2]/div/div/div/div/button").click()
time.sleep(3)
keyboard.type("M:\\School\\San Jose State University\\ImgAug\\img1.webp")
keyboard.tap(Key.enter)

#Prompt the ChatGPT about image
revealed = driver.find_element(By.XPATH, "//*[@id=\"prompt-textarea\"]")
WebDriverWait(driver, 50).until(lambda d: revealed.is_displayed())
driver.find_element(By.XPATH, "//*[@id=\"prompt-textarea\"]").click()
ActionChains(driver)\
  .send_keys("What can you tell me about this image?")\
  .perform()

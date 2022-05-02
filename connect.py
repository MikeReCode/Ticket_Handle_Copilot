from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from action import Action
import time
import os
import dotenv
dotenv.load_dotenv()


action = Action()

options = webdriver.ChromeOptions()

ser = Service(os.getenv('chromedriver_path'))

options.add_argument("user-data-dir=" + os.getenv('google_chrome_profile_path'))
driver = webdriver.Chrome(service=ser, options=options)

executor_url = driver.command_executor._url
session_id = driver.session_id
action.save_session_in_file(executor_url, session_id)

print(executor_url)
print(session_id)


driver.get("https://www.google.com/")
time.sleep(1)


driver.execute_script("window.open('about:blank', 'zendesk');")
driver.switch_to.window("zendesk")
driver.get(os.getenv('zendesk_link'))
zendesk = driver.current_window_handle
time.sleep(1)

driver.execute_script("window.open('about:blank', 'datatool');")
driver.switch_to.window("datatool")
driver.get(os.getenv('datatool_link'))
datatool = driver.current_window_handle
time.sleep(1)

driver.execute_script("window.open('about:blank', 'cint');")
driver.switch_to.window("cint")
driver.get(os.getenv('cint_link'))
cint = driver.current_window_handle
time.sleep(1)

action.save_browser_tabas(zendesk, datatool, cint)

driver.switch_to.window(driver.window_handles[0])
driver.close()

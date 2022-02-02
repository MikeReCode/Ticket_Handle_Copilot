from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from action import Action
import time


#if __name__ == '__main__':
action = Action()

options = webdriver.ChromeOptions()
ser = Service("C:\\*************\\chromedriver") # Path to chrmoedriver
options.add_argument("user-data-dir=C:\\Users\\******\\AppData\\Local\\Google\\Chrome\\User Data") # Path to your chrome profile
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
driver.get("Zendesk Link")
zendesk = driver.current_window_handle
time.sleep(1)

driver.execute_script("window.open('about:blank', 'datatool');")
driver.switch_to.window("datatool")
driver.get("Datatool link")
datatool = driver.current_window_handle
time.sleep(1)

driver.execute_script("window.open('about:blank', 'cint');")
driver.switch_to.window("cint")
driver.get("Cint link")
cint = driver.current_window_handle
time.sleep(1)

action.save_browser_tabas(zendesk, datatool, cint)

driver.switch_to.window(driver.window_handles[0])
driver.close()
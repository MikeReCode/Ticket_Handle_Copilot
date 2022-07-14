import time
import os
import dotenv
dotenv.load_dotenv()


def reconnect(action):

    executor_url, session_id = action.open_session_file()
    driver = action.attach_to_session(executor_url, session_id)
    driver.implicitly_wait(10)
    print("-****************  Reconnecting...  *******************-")

    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script('''window.open();''')
    driver.switch_to.window(driver.window_handles[-1])
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

    print("-****************  Reconnected!!  *******************-")
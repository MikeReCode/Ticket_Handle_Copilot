import time


def reconnect(action):

    executor_url, session_id = action.open_session_file()
    driver = action.attach_to_session(executor_url, session_id)
    driver.implicitly_wait(10)
    print("-****************  Reconnecting...  *******************-")

    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script('''window.open();''')
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("Zendesk link")
    zendesk = driver.current_window_handle
    time.sleep(1)

    driver.execute_script("window.open('about:blank', 'datatool');")
    driver.switch_to.window("datatool")
    driver.get("Datatool link")
    datatool = driver.current_window_handle
    time.sleep(1)

    driver.execute_script("window.open('about:blank', 'cint');")
    driver.switch_to.window("cint")
    driver.get("Cint Link")
    cint = driver.current_window_handle
    time.sleep(1)

    action.save_browser_tabas(zendesk, datatool, cint)
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    print("-****************  Reconnected!!  *******************-")
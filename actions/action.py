from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver


class Action:

    def save_session_in_file(self, url, id):
        fhand = open('session.txt', 'w')
        fhand.write(url + ' ' + id)
        fhand.close()

    def open_session_file(self):
        f = open('session.txt', 'r')
        text = f.read().split()
        return text[0], text[1]

    def save_browser_tabas(self, zendesk, datatool, cint):
        fhand = open('tabs.txt', 'w')
        fhand.write(zendesk + ' ' + datatool + ' ' + cint)
        fhand.close()

    def open_browser_tabas(self):
        f = open('tabs.txt', 'r')
        text = f.read().split()
        return text[0], text[1], text[2]

    def attach_to_session(self, executor_url, session_id):
        ''' First get the "executor_url" "and session_id" , onece you got that info keep the browser session opened
            than you can attach to that session while the browser session is opened.
            
            executor_url = driver.command_executor._url 
            session_id = driver.session_id  '''

        original_execute = WebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)

        # Patch the function before creating the driver object
        WebDriver.execute = new_command_execute
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id
        # Replace the patched function with original function
        WebDriver.execute = original_execute
        return driver


if __name__ == "__main__":
    print("sardina")
    ac = Action()
    print(ac.open_session_file())
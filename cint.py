import time
class Cint():

    def __init__(self, driver):
        self.driver = driver


    def search_with_email(self, email):

        k = self.driver.find_element_by_xpath("//*[@placeholder='Email address']")
        k.clear()
        k.send_keys(email)
        self.driver.find_element_by_xpath("//*[@value='List']").click()

        try:
            id = self.driver.find_elements_by_xpath("//*[@data-bind='foreach: panelists']//a")[-1].text
            status = self.driver.find_elements_by_xpath("//*[@data-bind='text: status']")[-1].text
            panel = self.driver.find_elements_by_xpath("//*[@data-bind='text: panelName']")[-1].text.split("Lifepoints - ")[-1]
            panel.strip()
            return id, status, panel
        
        except Exception as e:
            print(e)
            print( "*** No account was found with thise email address!!!! ***\n")
            id = None
            status = None
            panel = None
            return id, status, panel


    def update_status(self):

        self.driver.find_element_by_xpath("//option[contains (text(), 'Active')]").click()
        self.driver.find_element_by_xpath('//*[@type="submit" and @value="Update"]').click()
        
        
    def panelist_account(self):

        self.driver.find_elements_by_xpath("//*[@data-bind='foreach: panelists']//a")[-1].click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
    def click_points_transaction(self):

        self.driver.find_element_by_link_text("Point transactions").click()
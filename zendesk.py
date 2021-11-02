import time
from selenium.webdriver.common.keys import Keys


class Zendesk():

    def __init__(self, driver):
        self.driver = driver
        
    
    def search_in_zendesk(self, search):
        ''' search -> string you want to search in zendesk Ex: ticket number '''

        self.driver.find_element_by_xpath('//*[@data-garden-id="forms.faux_input"]').click()
        search_bar = self.driver.find_element_by_xpath('//*[@id="1val-field_1.3.7--input"]')
        search_bar.send_keys(search)
        time.sleep(1)
        search_bar.send_keys(Keys.ENTER)
    
    
    def left_side_bar(self, view):
        ''' You can choose between "ticket" view ot "customer" view '''

        if view == "ticket":
            self.driver.find_element_by_xpath('//*[@data-test-id="customer-context-tab-ticket"]').click()
        elif view == "customer":
            self.driver.find_element_by_xpath('//*[@data-test-id="customer-context-tab-customer"]').click()
        else:
            print("incorrect zendesk left side bar button!!!")
        
        
    def extract_current_ticket_number(self):
        
        k = self.driver.find_elements_by_xpath('//*[@class="ember-view btn active"]')
        for i in k:
            if i.text != "":
                return i.text.split("#")[1]
            
    
    def get_email_address(self):
        ''' Get email address from zendesk ticket '''

        return self.driver.find_element_by_xpath('//*[@class="email"]').text
        
        
    def get_ticket_sunject(self):
        return self.driver.find_element_by_xpath('//*[@data-test-id="ticket-pane-subject"]').get_attribute("value")
        
        
    def change_ticket_form(self, form):
        ''' form -> form you want to change to '''
        
        k = self.driver.find_elements_by_xpath("//div[@class='ember-view form_field']//div[@role='button']")
        for i in k:
            if i.text != "":
                i.click()
        forms = self.driver.find_elements_by_xpath('//*[@data-garden-id="dropdowns.item"]')
        if form == "membership":
            forms[4].click()
            
            
        elif form == "registration":
            forms[5].click()
            
        elif form == "unsubscribe":
            forms[6].click()
    
    
    def change_ticket_category(self, category):
        ''' category -> category you want to change to '''

        if category == "inavtive-invalid":
            keys = "cancelled"
        elif category == "how does my membership work":
            keys = "how does my membership work"
            
        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Category')]//following::input[1]")
        k.send_keys(keys)
        k.send_keys(Keys.ENTER)
    
    
    def change_ticket_status(self, status):
        ''' status -> status you want to change to '''

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Cint Panelist Status')]//following::input[1]")
        k.send_keys(status)
        k.send_keys(Keys.ENTER)
        
     
    def change_ticket_psReason(self, psReason):
        ''' psReason -> psReason you want to change to '''

        k = self.driver.find_elements_by_xpath("//label[contains (text(), 'psReason')]//following::input[1]")
        for i in k:
            try:
                self.driver.implicitly_wait(0.1)
                i.send_keys(psReason)
                i.send_keys(Keys.ENTER)
                self.driver.implicitly_wait(10)
                break
            except:  # if element is not interactive, go to the next element
                pass
                
                
    def change_ticket_issue_traker(self, issue):
        ''' issue ->  issue you want to track'''
            
        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Issue Tracker')]//following::input[1]")
        k.send_keys(issue)
        k.send_keys(Keys.ENTER)
    
    
    def select_SA(self, sa):
        ''' sa -> Standard answer you want '''

        k = self.driver.find_element_by_xpath("//*[@data-test-id='ticket-footer-macro-menu-autocomplete-input']//following::input[1]")
        k.send_keys(sa)
        #k.send_keys(Keys.ENTER)
        
            
    def close_tab(self):
        ''' Close current zendesk tab '''

        self.driver.find_element_by_xpath('//*[@data-test-id="close-button"]').click()
        try:
            self.driver.implicitly_wait(0.2)
            self.driver.find_element_by_xpath("//button[contains (text(), 'Close Tab')]").click()
            self.driver.implicitly_wait(10)
        except:
            self.driver.implicitly_wait(10)


    def get_first_comment_in_ticket(self):
        return self.driver.find_elements_by_xpath('//*[@class="zd-comment"]')[-1].text
        
        
    def get_date_hour_of_first_comment(self):
        return self.driver.find_elements_by_xpath('//div[@class="actor"]//time')[-1].get_attribute("title")
    
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Zendesk:

    def __init__(self, driver):
        self.driver = driver

    def search_in_zendesk(self, search):
        ''' search -> string you want to search in zendesk Ex: ticket number '''

        self.driver.find_element_by_xpath('//*[@data-garden-id="forms.faux_input"]').click()
        search_bar = self.driver.find_element_by_xpath('//*[@data-garden-id="forms.media_input"]')
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

    def get_ticket_subject(self):
        return self.driver.find_element_by_xpath('//*[@data-test-id="ticket-pane-subject"]').get_attribute("value")

    def change_ticket_form(self, form):
        ''' form -> form you want to change to '''

        k = self.driver.find_elements_by_xpath("//div[@class='ember-view form_field']//div[@role='button']")
        for i in k:
            if i.text != "":
                i.click()
        forms = self.driver.find_elements_by_xpath('//*[@data-garden-id="dropdowns.item"]')
        if form == "membership":
            forms[5].click()

        elif form == "registration":
            forms[6].click()

        elif form == "unsubscribe":
            forms[7].click()

        elif form == "rewards":
            forms[8].click()

    def change_ticket_category(self, category):
        ''' category -> category you want to change to '''

        if category == "inactive-invalid":
            keys = "cancelled"
        elif category == "how does my membership work":
            keys = "how does my membership work"
        else:
            keys = category
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

    def change_quality_escalation(self, escalation):
        ''' Change status of the quality team escalation '''

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Quality Escalation')]//following::input[1]")
        k.send_keys(escalation)
        k.send_keys(Keys.ENTER)

    def change_panelist_ID(self, id):

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Panelist ID')]//following::input[1]")
        k.send_keys(id)
        k.send_keys(Keys.ENTER)

    def select_SA(self, sa):
        ''' sa -> Standard answer you want '''

        k = self.driver.find_element_by_xpath(
            "//*[@data-test-id='ticket-footer-macro-menu-autocomplete-input']//following::input[1]")
        k.send_keys(Keys.CONTROL, 'a')
        k.send_keys(Keys.BACKSPACE)
        k.send_keys(sa)
        # k.send_keys(Keys.ENTER)

    def submit_ticket(self, status):
        time.sleep(1)
        m = self.driver.find_element(By.XPATH, "//*[@data-test-id='submit_button-menu-button']")
        # time.sleep(1)
        m.click()

        # time.sleep(5)
        if status == "pending":
            k = self.driver.find_element(By.XPATH, "//*[@data-action-id='submit_button-menu-pending']")
            k.click()
        elif status == "solved":
            k = self.driver.find_element(By.XPATH, "//*[@data-action-id='submit_button-menu-solved']")
            k.click()
        elif status == "hold":
            k = self.driver.find_element(By.XPATH, "//*[@data-action-id='submit_button-menu-hold']")
            k.click()

    def reset_sa(self):

        k = self.driver.find_element_by_xpath(
            "//*[@data-test-id='ticket-footer-macro-menu-autocomplete-input']//following::input[1]")
        k.send_keys(Keys.CONTROL, 'a')
        k.send_keys(Keys.BACKSPACE)

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

    def create_new_ticket(self):
        k = self.driver.find_element_by_xpath("//*[@data-test-id='header-toolbar-add-menu-button']")
        k.click()
        self.driver.find_elements_by_xpath("//*[@data-garden-id='dropdowns.item']")[0].click()

    def change_ticket_brand(self):
        self.driver.find_element_by_xpath("//*[@data-test-id='ticket-system-field-brand-select']").click()
        self.driver.find_elements_by_xpath('//*[@data-garden-id="dropdowns.media_item"]')[7].click()

    def change_ticket_requester(self, email):
        # k = self.driver.find_element_by_xpath("//label[contains (text(), 'Requester')]//following::input[1]")
        k = self.driver.find_elements_by_xpath(
            "//*[@class='zd-searchmenu zd-searchmenu-root zd-state-default']/input[ @placeholder='search name or contact info']")
        for i in k:
            try:
                self.driver.implicitly_wait(0.1)
                # i.click()
                i.send_keys(email)
                self.driver.implicitly_wait(5)
                time.sleep(1)
                break
            except:  # if element is not interactive, go to the next element
                pass
        # k.send_keys("men")
        ls = self.driver.find_elements_by_xpath('//*[@class="zd-menu-item zd-leaf"]//a')
        print(f"longitud de la lista {len(ls)}")
        print(ls)
        if len(ls) == 1:
            ls[0].click()
        else:
            input("Press Enter to continue ")

    def change_ticket_assignee(self, panel):

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Assignee')]//following::input[1]")
        k.send_keys(panel)
        time.sleep(1)
        k.send_keys(Keys.ENTER)
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//*[@data-test-id='assignee-field-take-it-button']").click()

    def change_ticket_redemption_item(self, redemption_item):

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Redemption Item')]//following::input[1]")
        k.send_keys(redemption_item)
        k.send_keys(Keys.ENTER)

    def change_ticket_fulfillment_status(self, status):

        k = self.driver.find_element_by_xpath("//label[contains (text(), 'Fulfillment status')]//following::input[1]")
        k.send_keys(status)
        k.send_keys(Keys.ENTER)

    def change_ticket_subject(self, subject):

        k = self.driver.find_element_by_xpath("//*[@data-test-id='new-ticket-subject']")
        k.send_keys(subject)
        k.send_keys(Keys.ENTER)

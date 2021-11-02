from cint import Cint
from datatool import Datatool
from action import Action
from zendesk import Zendesk
import time


class HandleTicket():

    def __init__(self, driver):
        self.driver = driver
        self.action = Action()
        self.tab_zendesk, self.tab_datatool, self.tab_cint = self.action.open_browser_tabas()
        self.datatool = Datatool(self.driver)
        self.cint = Cint(self.driver)
        self.zendesk = Zendesk(self.driver)
        
        
    def reactivate_panelist(self):

        self.driver.switch_to.window(self.tab_datatool)
        self.datatool.edit_psReason()
        self.driver.switch_to.window(self.tab_cint)
        self.driver.find_element_by_xpath("//*[@data-bind='foreach: panelists']//a").click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.cint.update_status()
        time.sleep(0.5)
        self.driver.close()
        
        
    def handle_do_not_reactivate(self, psReason):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("sleep")
        self.zendesk.change_ticket_psReason(psReason)
        self.zendesk.left_side_bar("customer")
        if psReason == "701":
            self.zendesk.select_SA("3030")
        elif psReason == "702":
            self.zendesk.select_SA("3018")
        elif psReason == "703":
            self.zendesk.select_SA("3030")
        else:
            self.zendesk.select_SA("4009")
            
            
    def handle_direct_reactivation(self, psReason):
    
        self.reactivate_panelist()
        print("Panelis reactivated !!!") 
        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("sleep")
        self.zendesk.change_ticket_psReason(psReason)
        self.zendesk.left_side_bar("customer")
        if psReason == "400":
            self.zendesk.select_SA("3080")
        elif psReason == "602":
                self.zendesk.select_SA("3084")
        else:
            self.zendesk.select_SA("3020")
            
            
    def handle_serie_600(self, psReason):

        reactivated = False
        
        if psReason == "603":
            self.datatool.edit_psReason(psReason="599")
        elif psReason == "604":
            pass
        else:
        
            while True:
                inp = input(" Reactivate panelist ?  y / n : ")
                print("")
                if inp == "y":
                    self.reactivate_panelist()
                    reactivated = True
                    print("Panelis reactivated !!!\n")
                    break
                elif inp == "n":
                    break
                else:
                    print("Please incert correct input!\n")
            
        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("sleep")
        self.zendesk.change_ticket_psReason(psReason)
        self.zendesk.left_side_bar("customer")
        if reactivated == True:
            if psReason == "601": 
                self.zendesk.select_SA("3082")
            elif psReason == "699":
                self.zendesk.select_SA("3053")
            else:
                self.zendesk.select_SA("3020")
        else:
            if psReason == "601" or psReason == "699": 
                self.zendesk.select_SA("3030")
            elif psReason == "603":
                self.zendesk.select_SA("3060")
            elif psReason == "604":
                self.zendesk.select_SA("3055")
            elif psReason == "605":
                self.zendesk.select_SA("3057")
            else:
                self.zendesk.select_SA("4009")
                
                
    def handle_no_psReason(self):
    
        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("sleep")
        self.zendesk.change_ticket_issue_traker("Email Found in CINT but Not in RIL Admin")
        self.zendesk.left_side_bar("customer")
        self.zendesk.select_SA("2011")
        
        
    def handle_no_account_found(self):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("how does my membership work")
        self.zendesk.change_ticket_status("not found")
        self.zendesk.left_side_bar("customer")
        self.zendesk.select_SA("4011")
        
        
    def handle_unsubscribed(self):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("unsubscribed")
        self.zendesk.change_ticket_psReason("901")
        self.zendesk.select_SA("5007")
        
        
    def handle_bad_email(self):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inavtive-invalid")
        self.zendesk.change_ticket_status("bad email")
        self.zendesk.change_ticket_psReason("201")
        self.zendesk.select_SA("3024")
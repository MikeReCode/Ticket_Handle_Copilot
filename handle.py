from cint import Cint
from datatool import Datatool
from action import Action
from zendesk import Zendesk
import time
import pandas as pd


class HandleTicket:

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
        self.driver.find_elements_by_xpath("//*[@data-bind='foreach: panelists']//a")[-1].click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(0.5)
        self.cint.update_status()
        time.sleep(0.5)
        self.driver.close()

    def handle_do_not_reactivate(self, psReason, status, id):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status(status)
        self.zendesk.change_ticket_psReason(psReason)
        if psReason in ["702", "704"]: self.zendesk.change_panelist_ID(id)
        self.zendesk.left_side_bar("customer")

        if psReason in ["701", "707"]:
            self.zendesk.select_SA("3030")
        elif psReason in ["702", "704"]:
            self.zendesk.select_SA("3018")
        elif psReason == "703":
            self.zendesk.select_SA("3061")
        elif psReason == "713":
            self.zendesk.select_SA("3069")
        else:
            self.zendesk.select_SA("4009")

    def handle_direct_reactivation(self, psReason, status):

        self.reactivate_panelist()
        print("Panelist reactivated !!!")
        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status(status)
        self.zendesk.change_ticket_psReason(psReason)
        self.zendesk.left_side_bar("customer")

        if psReason == "400":
            self.zendesk.select_SA("3080")
        elif psReason == "602":
            self.zendesk.select_SA("3084")
        else:
            self.zendesk.select_SA("3020")

    def handle_serie_600(self, psReason, id, status):

        reactivated = None

        if psReason == "603":
            self.datatool.edit_psReason(psReason="599")
            reactivated = False
        elif psReason == "604":
            reactivated = False
            pass
        elif psReason == "699":
            df = pd.read_excel("check\psReason_699_Accounts_that_can_NOT_be_reactivated.xlsx")

            baned = list(df['PanelistId2'])
            id_int = int(id)
            if id_int in baned:
                print("DO NOT REACTIVATE !!!!    ---- Panelist in list")
                reactivated = False

        while True:
            if reactivated == False:
                break
            inp = input(" Reactivate panelist ?  y / n : ")
            print("")
            if inp == "y":
                self.reactivate_panelist()
                reactivated = True
                print("Panelist reactivated !!!\n")
                break
            elif inp == "n":
                reactivated = False
                break
            else:
                print("Please insert correct input!\n")

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status(status)
        self.zendesk.change_ticket_psReason(psReason)
        if psReason in ["699", "610"]: self.zendesk.change_panelist_ID(id)

        self.zendesk.left_side_bar("customer")
        if reactivated:
            if psReason == "601":
                self.zendesk.select_SA("3082")
            elif psReason == "699":
                self.zendesk.select_SA("3053")
            elif psReason == "605":
                self.zendesk.select_SA("3057")
            else:
                self.zendesk.select_SA("3020")
        else:
            if psReason in ["601", "699", "605", "799"]:
                self.zendesk.select_SA("3030")
            elif psReason == "603":
                self.zendesk.select_SA("3060")
            elif psReason == "604":
                self.zendesk.select_SA("3055")
            else:
                self.zendesk.select_SA("4009")

    def handle_handle_711(self, psReason, id, status):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status(status)
        self.zendesk.change_ticket_psReason(psReason)
        self.zendesk.change_quality_escalation("Escalate to Quality")
        self.zendesk.change_panelist_ID(id)
        self.zendesk.left_side_bar("customer")
        self.zendesk.select_SA("2011")

    def handle_no_psReason(self, status):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
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
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status("unsubscribed")
        self.zendesk.change_ticket_psReason("901")
        self.zendesk.select_SA("5007")

    def handle_bad_email(self):

        self.driver.switch_to.window(self.tab_zendesk)
        self.zendesk.left_side_bar("ticket")
        self.zendesk.change_ticket_form("membership")
        self.zendesk.change_ticket_category("inactive-invalid")
        self.zendesk.change_ticket_status("bad email")
        self.zendesk.change_ticket_psReason("201")
        self.zendesk.select_SA("3024")

import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def select_SA(driver, sa):
    ''' sa -> Standard answer you want '''

    k = driver.find_element(By.XPATH,
                            "//*[@data-test-id='ticket-footer-macro-menu-autocomplete-input']//following::input[1]")
    k.send_keys(Keys.CONTROL, 'a')
    k.send_keys(Keys.BACKSPACE)
    k.send_keys(sa)
    k.send_keys(Keys.ENTER)


def responses():
    df = pd.read_excel("check\lol.xlsx")

    tickets = list(df['PanelistId2'])
    task = list(df['Task'])
    # print(tickets)
    # print(task)
    responses_list = zip(tickets, task)
    return responses_list


def process_responses(driver, zendesk, cint, datatool, handle_membership, tab_zendesk, tab_datatool, tab_cint):
    while True:
        options = ["y", "n", "quit"]
        handle = input("Process tickets from file ? y / n or quit: ")
        print("")
        if handle in options:
            if handle == "n":
                print("OK")
                continue

            elif handle == "quit":
                print("See you next time beautiful !!\n")
                using = False
                return

            else:
                break

        print("Please insert correct input!\n")

    start_time = time.time()  # process counter

    for ticket, task in responses():

        time.sleep(1)
        id = None
        status = None
        panel = None

        driver.switch_to.window(tab_zendesk)
        zendesk.search_in_zendesk(ticket)
        email = zendesk.get_email_address()
        driver.switch_to.window(tab_cint)
        id, status, panel = cint.search_with_email(email)
        if id is None:
            print("cint account not found on ticket:  ", ticket)
            continue
        else:
            driver.switch_to.window(tab_datatool)
            psReason = datatool.search_with_panelist_id(id)
            if psReason == "711":
                if task.startswith("do not"):

                    driver.switch_to.window(tab_zendesk)
                    zendesk.left_side_bar("ticket")
                    zendesk.change_quality_escalation("Do Not Reactivate")
                    select_SA(driver, "3030")
                    zendesk.left_side_bar("ticket")
                    zendesk.submit_ticket("solved")
                    print(f"Solved ticket {ticket}  NOT reactivated")

                else:
                    handle_membership.reactivate_panelist()
                    driver.switch_to.window(tab_zendesk)
                    zendesk.left_side_bar("ticket")
                    zendesk.change_quality_escalation("Account Reactivated")
                    select_SA(driver, "3020")
                    zendesk.left_side_bar("ticket")
                    zendesk.submit_ticket("solved")
                    print(f"Solved ticket {ticket} reactivated")

            elif psReason in ["610"]:

                if task.startswith("do not"):

                    driver.switch_to.window(tab_zendesk)
                    zendesk.left_side_bar("ticket")
                    zendesk.change_quality_escalation("Do Not Reactivate")
                    select_SA(driver, "4009A")
                    zendesk.left_side_bar("ticket")
                    zendesk.submit_ticket("solved")
                    print(f"Solved ticket {ticket}  NOT reactivated")

                else:
                    handle_membership.reactivate_panelist()
                    driver.switch_to.window(tab_zendesk)
                    zendesk.left_side_bar("ticket")
                    zendesk.change_quality_escalation("Account Reactivated")
                    select_SA(driver, "3020")
                    zendesk.left_side_bar("ticket")
                    zendesk.submit_ticket("solved")
                    print(f"Solved ticket {ticket} reactivated")
            else:
                print(f"Ticket {ticket}, have psReason {psReason} , Not processed")

    print("")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("")

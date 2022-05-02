from handle import HandleTicket
from datatool import Datatool
from zendesk import Zendesk
from action import Action
from cint import Cint
from quality_responses import process_responses
import membership
import reconnect
import escalation
import paypal_denied
import os

from prettytable import PrettyTable

try:
    action = Action()
    tab_zendesk, tab_datatool, tab_cint = action.open_browser_tabas()
    executor_url, session_id = action.open_session_file()

    driver = action.attach_to_session(executor_url, session_id)
    driver.implicitly_wait(10)
except:
    print("\n" + "*" * 50 + "\n")
    print(" You are not connected!!!\n")

while True:

    datatool = Datatool(driver)
    zendesk = Zendesk(driver)
    cint = Cint(driver)
    handle_membership = HandleTicket(driver)

    options = ["1", "2", "3", "4", "5", "6", "7"]
    print("*" * 50 + "\n")
    # Menu
    menu = PrettyTable()
    menu.field_names = ["Actions", ""]
    # menu.hrules = 1
    menu.add_row(["1", "Membership"])
    menu.add_row(["2", "Connect"])
    menu.add_row(["3", "Reconnect"])
    menu.add_row(["4", "Escalate"])
    menu.add_row(["5", "PayPal Denied"])
    menu.add_row(["6", "Quality Responses"])
    menu.add_row(["7", "Quit"])

    menu.align[""] = "l"
    print(menu)
    print()

    # Alternative menu from input message
    # handle = input(" Actions :\n\n 1 - Membership\n 2 - Connect\n 3 - Reconnect\n 4 - Escalate\n 5 - PayPal Denied \n 6 - Quit\n\nChoose your action: ")
    handle = input("Choose your action: ")
    # handle = handle.lower()

    print("")
    print("*" * 50 + "\n")

    if handle in options:
        if handle == "1":
            membership.membership_procedure(driver, zendesk, cint, datatool, handle_membership, tab_zendesk,
                                            tab_datatool, tab_cint)
            continue

        elif handle == "7":
            print("See you next time beautiful !!")
            break

        elif handle == "2":
            os.system('python connect.py')
            executor_url, session_id = action.open_session_file()

            driver = action.attach_to_session(executor_url, session_id)
            driver.implicitly_wait(10)
            tab_zendesk, tab_datatool, tab_cint = action.open_browser_tabas()

            continue

        elif handle == "3":
            reconnect.reconnect(action)
            tab_zendesk, tab_datatool, tab_cint = action.open_browser_tabas()
            continue

        elif handle == "4":
            escalation.escalation(driver, zendesk, cint, tab_zendesk, tab_cint)
            continue

        elif handle == "5":
            paypal_denied.paypal_denied(driver, zendesk, cint, tab_zendesk, tab_cint)

        elif handle == "6":
            process_responses(driver, zendesk, cint, datatool, handle_membership, tab_zendesk, tab_datatool, tab_cint)
    else:
        print("Please insert correct input!")
        continue

print("Adios!!")

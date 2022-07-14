import time
from prettytable import PrettyTable

do_not_reactivate = ["301", "302", "304", "305", "306", "307", "308", "309", "310", "311", "312", "400", "401", "701",
                     "702", "703", "704", "707", "608", "713", "714", "607"]
serie_600 = ["601", "609", "610", "611", "699", "603", "604", "605", "799"]
direct_reactivation = ["602"]
not_handle = ["708"]
handle_711 = ["711"]


def membership_procedure(driver, zendesk, cint, datatool, handle_membership, tab_zendesk, tab_datatool, tab_cint):
    using = True
    while using:

        id = "0"
        status = "0"
        ticket_nr = "0"
        email = "0"
        psReason = "0"
        while True:
            options = ["y", "n", "quit", "i"]
            handle = input("Handle this Ticket ? y / n or quit: ")
            print("")
            if handle in options:
                if handle == "n":
                    print("OK")
                    continue

                break

            print("Please insert correct input!\n")

        if handle == "quit":
            print("See you next time beautiful !!\n")
            using = False
            break

        start_time = time.time()  # process counter

        driver.switch_to.window(tab_zendesk)
        ticket_nr = zendesk.extract_current_ticket_number()
        email = zendesk.get_email_address()

        # Reser SA
        # zendesk.reset_sa()

        if email == "":
            print("--- No email found --- Probably more than 1 ticket open !! ")
            print("")
            continue

        driver.switch_to.window(tab_cint)

        id, status, panel = cint.search_with_email(email)

        if id is None:
            handle_membership.handle_no_account_found()
            continue

        elif status == "Unsubscribed":
            print("*", f"Status: {status}", "*")
            handle_membership.handle_unsubscribed()
            continue

        elif handle == "i":

            cint.panelist_account()
            continue

        driver.switch_to.window(tab_datatool)

        psReason = datatool.search_with_panelist_id(id)

        # info table
        panelist_info = PrettyTable()
        panelist_info.hrules = 1
        panelist_info.header = False
        panelist_info.field_names = ["Panelist", "Info"]
        panelist_info.add_row(["Ticket#", ticket_nr])
        panelist_info.add_row(["Panel", panel])
        panelist_info.add_row(["ID", id])
        panelist_info.add_row(["Status", status])
        panelist_info.add_row(["psReason", psReason])

        panelist_info.align["Panelist"] = "r"
        panelist_info.align["Info"] = "l"
        print(panelist_info)
        print()

        if status == "Bad email":
            handle_membership.handle_bad_email()

        else:

            if psReason in not_handle:
                driver.switch_to.window(tab_zendesk)
                print("Skip this ticket!!!")

            elif psReason == "":
                handle_membership.handle_no_psReason(status)

            elif psReason in do_not_reactivate:
                handle_membership.handle_do_not_reactivate(psReason, status, id)

            elif psReason in direct_reactivation:
                handle_membership.handle_direct_reactivation(psReason, status)

            elif psReason in serie_600:
                handle_membership.handle_serie_600(psReason, id, status)

            elif psReason in handle_711:
                handle_membership.handle_handle_711(psReason, id, status)

            else:
                driver.switch_to.window(tab_zendesk)
                print("I don't know what to do with this ticket !!\n")

        print("")
        print("--- %s seconds ---" % (time.time() - start_time))
        print("")

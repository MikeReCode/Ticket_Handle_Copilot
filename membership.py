import time


do_not_reactivate = ["301", "302", "304", "305", "306", "307", "308", "309", "310", "311", "312", "701", "702", "703"]
serie_600 = ["601", "609", "610", "611", "699", "603", "604", "605"]
direct_reactivation = ["713", "400", "602"]
not_handle = ["708", "711"]

def membership_procedure(driver, zendesk, cint, datatool, handle_membership, tab_zendesk, tab_datatool, tab_cint):

    using = True
    while using:
        driver.switch_to.window(tab_zendesk)
        id = "0"
        status = "0"
        ticket_nr = "0"
        email = "0"
        psReason = "0"
        while True:
            options = ["y", "n", "quit"]
            handle = input("Handle thise Ticket ? y / n or quit: ")
            print("")
            if handle in options:
                if handle == "n":
                    print("OK")
                    continue
                    
                break
                
            print("Please incert correct input!\n")
            
        if handle == "quit":
            print("See you next time beautiful !!\n")
            using = False
            break
        
        start_time = time.time() # process counter 
        
        ticket_nr = zendesk.extract_current_ticket_number()  
        email = zendesk.get_email_address()

        if email == "":
            print("--- No email found --- Probably more than 1 ticket open !! ")
            print("")
            continue

        driver.switch_to.window(tab_cint)
        
        id, status, panel= cint.search_with_email(email)
            
        if id == None:
            handle_membership.handle_no_account_found()
            continue
            
        if status == "Unsubscribed":
            print("*", f"Status: {status}", "*")
            handle_membership.handle_unsubscribed()
            continue
            
        driver.switch_to.window(tab_datatool)
        
        psReason = datatool.search_with_panelist_id(id)

        # info table

        print("*" * 19)
        print("*" + " " * 17 + "*")
        print("*", f"Ticket# {ticket_nr}", "*")
        print("*" + " " * 17 + "*")
        print("*", f"Panel: {panel}"," " * 5, "*")
        print("*" + " " * 17 + "*")
        print("*", f"ID: {id}", "  *")
        print("*" + " " * 17 + "*")
        print("*", f"Status: {status}", "*")
        print("*" + " " * 17 + "*")
        print("*", f"psReason: {psReason}", "  *")
        print("*" + " " * 17 + "*")
        print("*" * 19 + "\n")

        
        if status == "Bad email":
            handle_membership.handle_bad_email()
        
        else:
        
            if psReason in not_handle:
                driver.switch_to.window(tab_zendesk)
                print("Skip this ticket!!!")
                continue
                
            elif psReason == "":
                handle_membership.handle_no_psReason()
                
            elif psReason in do_not_reactivate:
                handle_membership.handle_do_not_reactivate(psReason)
                
            elif psReason in direct_reactivation:
                handle_membership.handle_direct_reactivation(psReason)
                
            elif psReason in serie_600:
                handle_membership.handle_serie_600(psReason)
                
            else:
                print("I don't know what to do with this ticket !!\n")
        
        print("")
        print("--- %s seconds ---" % (time.time() - start_time))
        print("")
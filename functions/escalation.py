import time
from openpyxl import load_workbook


def escalation(driver, zendesk, cint, tab_zendesk, tab_cint):
    start_time = time.time()

    while True:
        options = ["y", "n", "quit"]
        handle = input("Start Escalation File ? y / n or quit: ")
        handle = handle.lower()
        print("")
        if handle in options:
            if handle == "n":
                print("OK")
                continue

            elif handle == "quit":
                print("See you next time beautiful !!\n")
                break
            else:
                print("Great !!")

        else:
            print("Please insert correct input!\n")
            continue

        driver.switch_to.window(tab_zendesk)
        checks = driver.find_elements_by_xpath('//*[@data-test-id="search-tables-results-ckeckbox"]//input')
        ticket_nr = driver.find_elements_by_xpath(
            '//*[@data-test-id="search-tables-results-ckeckbox"]//following::td[3]')

        x = zip(checks, ticket_nr)

        ticket_ls = [tk_nr.text.strip("#") for checkbox, tk_nr in x if checkbox.is_selected()]

        print(ticket_ls)
        if len(ticket_ls) == 10:
            print("great")

        elif len(ticket_ls) < 10:
            print("You need to choose 10 tickets!!")
            continue
        else:
            print("You need to choose ONLY 10 tickets!!")
            continue

        survey = input("Please insert Survey Number:  ")
        print("")
        nr_complaints = input("Please insert Total Number of complaints received for this survey:  ")
        print("")
        countries_afected = input("Please insert countries affected in format ES, RU, TH, FR....  :  ")

        zendesk.close_tab()
        print("ticket ls :", ticket_ls)
        info = []
        for ticket in ticket_ls:
            zendesk.search_in_zendesk(ticket)

            subject = zendesk.get_ticket_subject()
            email = zendesk.get_email_address()
            driver.switch_to.window(tab_cint)
            id, _, _ = cint.search_with_email(email)
            driver.switch_to.window(tab_zendesk)

            if subject.startswith("Re: ") or subject.startswith("Chat "):
                comment = input("Please enter panelist comment:  ")
                print("")
            else:
                comment = zendesk.get_first_comment_in_ticket()

            date = zendesk.get_date_hour_of_first_comment()
            info.append((ticket, id, date, comment))
            zendesk.close_tab()

        # load excel file
        workbook = load_workbook(filename="escalations/template.xlsx")

        # open workbook
        sheet = workbook.active

        # modify the desired cell
        sheet[
            "A3"] = f"Member Services have received inquiries from our LifePoints members regarding Survey  {survey} ."
        sheet["A6"] = f"Total # of Tickets Received: {nr_complaints}"
        sheet["A7"] = f"Countries affected:  {countries_afected}"

        sheet["A17"] = f"Ticket #: {info[0][0]}"
        sheet["A18"] = f"Panelist ID {info[0][1]} wrote  {info[0][2]}"
        sheet["A19"] = info[0][3]

        sheet["A22"] = f"Ticket #: {info[1][0]}"
        sheet["A23"] = f"Panelist ID {info[1][1]} wrote  {info[1][2]}"
        sheet["A24"] = info[1][3]

        sheet["A27"] = f"Ticket #: {info[2][0]}"
        sheet["A28"] = f"Panelist ID {info[2][1]} wrote  {info[2][2]}"
        sheet["A29"] = info[2][3]

        sheet["A32"] = f"Ticket #: {info[3][0]}"
        sheet["A33"] = f"Panelist ID {info[3][1]} wrote  {info[3][2]}"
        sheet["A34"] = info[3][3]

        sheet["A37"] = f"Ticket #: {info[4][0]}"
        sheet["A38"] = f"Panelist ID {info[4][1]} wrote  {info[4][2]}"
        sheet["A39"] = info[4][3]

        sheet["A42"] = f"Ticket #: {info[5][0]}"
        sheet["A43"] = f"Panelist ID {info[5][1]} wrote  {info[5][2]}"
        sheet["A44"] = info[5][3]

        sheet["A47"] = f"Ticket #: {info[6][0]}"
        sheet["A48"] = f"Panelist ID {info[6][1]} wrote  {info[6][2]}"
        sheet["A49"] = info[6][3]

        sheet["A52"] = f"Ticket #: {info[7][0]}"
        sheet["A53"] = f"Panelist ID {info[7][1]} wrote  {info[7][2]}"
        sheet["A54"] = info[7][3]

        sheet["A57"] = f"Ticket #: {info[8][0]}"
        sheet["A58"] = f"Panelist ID {info[8][1]} wrote  {info[8][2]}"
        sheet["A59"] = info[8][3]

        sheet["A62"] = f"Ticket #: {info[9][0]}"
        sheet["A63"] = f"Panelist ID {info[9][1]} wrote  {info[9][2]}"
        sheet["A64"] = info[9][3]

        # save the file
        workbook.save(filename=f"escalations/Panelist_Complaint_Lifepoints_{countries_afected}_{survey}.xlsx")

        print("--- %s seconds ---" % (time.time() - start_time))

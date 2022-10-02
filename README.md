# Ticket_Handle_Copilot
## Ticket Handle Copilot - v 1.3

I automated my work by creating a "ticket handle copilot" using Python and Selenium.

This application can perform various tasks such as check user information in external databases, autocomplete all the necessary fields of a ticket and suggest an answer depending on the user's account status, it can create Excel files necessary to escalate cases to another department or receive an Excel file as input to answer and autocomplete specific tickets, etc.

### Necessary libraries:

- Selenium
- openpyxl
- prettytable
- pandas
- python-dotenv

### How it works:
#### - Ticket Handle

To start de automation we need to run the file `main.py`, after that we see the main menu.
To initiate the automation wee need to type "2", then a Chrome Browser will open with all the websites necessaries to work correctly. 

![](img/1.png)

To activate the "ticket handle" we need to type "1", then the automation will ask us permission to handle the current ticket we're working on. 

![](img/2.png)

If we press "y", the automation takes the person's email address from the ticket and go to the first database, makes the search and gets some information.

![](img/6.png)

Depending on the "Status" the automation will take different actions. For example, if the status is "Active" or "Sleeping", the automation takes the "ID" found in the first database and will search in a second database. 

![](img/7.png)

After all the information is collected will show us a summary.

![](img/3.png)

Depending on the psReason it may ask us if we want to reactivate the account and that triggers different actions. 

At the end of the process the automation completes all the necessary fields and  offers a proposal for an answer.

![](img/4.png)

#### - Reconnect

If you close by accident one of the necessary tabs for the automation to work, you have to close all the remaining tabs except one, type "3" and will open again all the necessary tabs. 

![](img/5.png)

#### - Escalation

For the escalation process you need to choose 10 ticket with a particular issue than type "4" and the automation will create the Excel file necessary for the escalation. 

![](img/8.png)

#### - PayPal Denied

Creates a ticket from scratch by completing all the necessary information to notify the user that their paypal order has been canceled.

#### - Quality Responses

Receives as input an Excel file with the tickets that need to be updated and the responses for each ticket then answers and autocompletes all the tickets from the file automatically.

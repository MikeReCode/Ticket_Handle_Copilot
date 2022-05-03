import time 
language = {
"BR": ["Brazil", "LifePoints - Pedido de recompensa PayPal cancelado - "],
"PT": ["Portugal", "LifePoints - Pedido de recompensa PayPal cancelado - "],
"ES": ["Spain", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"CL": ["Chile", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"MX": ["Mexico", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"AR": ["Argentina", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"CO": ["Colombia", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"PE": ["Peru", "LifePoints - Pedido de recompensa de PayPal cancelado - "],
"US - EN": ["USA - English", "LifePoints - PayPal Reward Order Canceled - "],
"DE": ["Germany", "LifePoints - PayPal-Prämienbestellung storniert - "],
"AT": ["Austria", "LifePoints - PayPal-Prämienbestellung storniert - "],
"TH": ["Thailand", "LifePoints - คำสั่งซื้อรางวัล PayPal ถูกยกเลิก - "],
"FR": ["France", "LifePoints - Commande de récompense PayPal annulée - "],
"BE - fr": ["Belgium - French", "LifePoints - Commande de récompense PayPal annulée - "],
"RU": ["Russia", "LifePoints - Заказ на вознаграждение PayPal отменен - "],
"IT": ["Italy", "LifePoints - Ordine premio PayPal annullato - "],
"NL": ["Netherlands", "LifePoints - PayPal-beloningsopdracht geannuleerd - "],
"BE - nl": ["Belgium - Dutch", "LifePoints - PayPal-beloningsopdracht geannuleerd - "],
"PL": ["Poland", "LifePoints — Anulowano zamówienie nagrody PayPal — "],
"VN": ["Vietnam", "LifePoints - Đơn đặt hàng phần thưởng PayPal đã bị hủy — "],
"JP": ["Japan", "LifePoints-PayPalリワード注文がキャンセルされました - "],
"GR": ["Greece", "LifePoints - Η παραγγελία ανταμοιβής PayPal ακυρώθηκε - "],
"TW": ["Taiwan", "LifePoints - PayPal 奖励订单已取消 - "],
}


def paypal_denied(driver, zendesk, cint, tab_zendesk, tab_cint):

    while True:
        
        id = "0"
        ticket_nr = "0"
        email = "0"
        while True:
            options = ["y", "n", "quit"]
            handle = input("Create Paypal Denied ticket ? y / n or quit: ")
            print("")
            if handle in options:
                if handle == "n":
                    print("OK")
                    continue
                    
                break
                
            print("Please insert correct input!\n")
            
        if handle == "quit":
            print("See you next time beautiful !!\n")
            break
        start_time = time.time() # process counter 
        
        email = input("\n Please insert Email address:  ")
        email.strip()
        
        driver.switch_to.window(tab_cint)
        _, _, panel = cint.search_with_email(email)
        
        if panel is None:
            print("\n****  Account not found *****\n")
            continue
        
        try:
            language[panel][0]
        except:
            print(f"\n Language not added to the list: {panel} \n")
            continue
        
        cint.panelist_account()
        cint.click_points_transaction()
        
        order_num = input("\n Please insert Order Number:   ")
        order_num.strip()
        if order_num == "":
            print("\n No order number inserted , canceling operation...\n ")
            continue
        driver.close()
        driver.switch_to.window(tab_zendesk)
        zendesk.create_new_ticket()
        zendesk.change_ticket_form("rewards")
        #zendesk.left_side_bar("ticket")
        zendesk.change_ticket_requester(email)
        zendesk.change_ticket_brand()
        
        
        zendesk.change_ticket_assignee("lLifePoints " + language[panel][0])

        #zendesk.change_ticket_form("rewards")
        zendesk.change_ticket_category("Cancel order")
        zendesk.change_ticket_redemption_item("paypal")
        zendesk.change_ticket_fulfillment_status("order cancelled")
        zendesk.change_ticket_subject(language[panel][1] + order_num)
        zendesk.select_SA("6051")
        
        print("")
        print("--- %s seconds ---" % (time.time() - start_time))
        print("")
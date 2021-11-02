import time

class Datatool():

    def __init__(self, driver):
        self.driver = driver


    def search_with_panelist_id(self, id):
    
        inp = self.driver.find_element_by_id("txt_RIL_search")
        inp.clear()
        inp.send_keys(id)
        self.driver.find_element_by_id("btn_RIL_search").click()
        
        try:
            loading = True
            while loading:
                time.sleep(0.5)
                if self.driver.find_element_by_xpath('//*[@id="btn_RIL_search"]').text == "Get Panelist Details":
                    loading = False
            ps = self.driver.find_element_by_class_name("RIL_psReason").text
            return ps
        except Exception as e:
            print(e)
            print("function search_with_panelist_id   --- Error !!!!")
        
        
    def edit_psReason(self, psReason="202"):

        self.driver.find_element_by_id("btn_attr_edit_psReason").click()
        inp = self.driver.find_element_by_xpath('//*[@id="txt_attrValue"]')
        inp.clear()
        inp.send_keys(psReason)
        self.driver.find_element_by_xpath('//*[@id="RILAdminDetail_Modal"]/div/div/div[3]/button[1]').click()
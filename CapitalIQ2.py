import pandas
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



driver = Chrome()
driver.get('https://www.capitaliq.com/')

driver.find_element_by_css_selector("input#username").clear()
driver.find_element_by_css_selector("input#username").send_keys(username')

driver.find_element_by_css_selector("input#password").clear()
driver.find_element_by_css_selector("input#password").send_keys(password)

driver.find_element_by_css_selector("input#myLoginButton").click()
delay = 10

myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '_headerTbl')))
print('get in')

def getCorp(corpname):
    driver.find_element_by_css_selector("input#SearchTopBar").clear()
    driver.find_element_by_css_selector("input#SearchTopBar").send_keys(corpname)
    driver.find_element_by_xpath("//input[@type='submit']").click()

    try:
        driver.find_element_by_css_selector("div#CompanyHeaderInfo")
    except:
        print('list')
        driver.find_element_by_xpath("//a[contains(@href,'pid=')]").click()

    name = driver.find_element_by_xpath('//div[@id="CompanyHeaderInfo"]//span[text()][1]').text
    try:
        sales =  driver.find_element_by_xpath('//td[contains(text(),"Revenue")]/following::td[1]').text
    except:
        sales = ''
    try:
        emp = driver.find_element_by_xpath('//td[contains(text(),"Employee")]/following::td[1]').text
    except:
        emp=''
    try:
        website = driver.find_element_by_xpath('//b[contains(text(),"Website")]/following::td[1]').text
    except:
        website=''
    try:
        address = driver.find_element_by_xpath('//td/*[contains(text(),"Location")]/following::tr[1]/td[1]').text
    except:
        address=''
    return {"name":name,"sales":sales,"employees":emp,"address":address,"website":website}

corpname = "ZURICH COMPAGNIE D'ASSURANCES SA"
getCorp(corpname)

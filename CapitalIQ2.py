from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def initbrowerser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path='/home/zdai/.wdm/drivers/chromedriver/linux64/81.0.4044.138/chromedriver',chrome_options=chrome_options)

    driver.get('https://www.capitaliq.com/')

    driver.find_element_by_css_selector("input#username").clear()
    driver.find_element_by_css_selector("input#username").send_keys('zd15ku@brocku.ca')

    driver.find_element_by_css_selector("input#password").clear()
    driver.find_element_by_css_selector("input#password").send_keys('Rel8edto')

    driver.find_element_by_css_selector("input#myLoginButton").click()
    delay = 10

    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '_headerTbl')))
    print('get in')
    return driver

def getCorp(corpname, driver):
    driver.find_element_by_css_selector("input#SearchTopBar").clear()
    driver.find_element_by_css_selector("input#SearchTopBar").send_keys(corpname)
    driver.find_element_by_xpath("//input[@type='submit']").click()

    try:
        driver.find_element_by_css_selector("div#CompanyHeaderInfo")
    except:
        print('list')
        driver.find_element_by_xpath("//a[contains(@href,'pid=')]").click()
    url = driver.current_url
    capitalID = (re.findall(r'Id=(\d+)',url)+[''])[0]
    name = driver.find_element_by_xpath('//div[@id="CompanyHeaderInfo"]//span[text()][1]').text
    try:
        sales =  driver.find_element_by_xpath('//*[contains(text(),"Revenue")]/following::td[1]/*').text
    except:
        sales = ''
    try:
        emp = driver.find_element_by_xpath('//*[contains(text(),"Employees")]/following::td[1]').text
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
    return {"name":name,"capitalID":capitalID,"sales":sales,"employees":emp,"address":address,"website":website,"capitalURL":url}

driver = initbrowerser()


corpname = 'JONES BROWN, INC.'
data = getCorp(corpname, driver)
print(data)

driver.close()

from selenium.webdriver import Chrome
import time,re, json

driver = Chrome()
# login
driver.get('https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx')
driver.find_element_by_xpath('//input[@name="username"]').clear()
driver.find_element_by_xpath('//input[@name="username"]').send_keys('zdai@brocku.ca')
driver.find_element_by_xpath('//input[@name="password"]').clear()
driver.find_element_by_xpath('//input[@name="password"]').send_keys('Rel8ed.to')
driver.find_element_by_xpath('//input[@name="myLoginButton"]').click()
time.sleep(5)

with open('corpnames.csv', encoding='utf8') as f:
    corpnames = f.read().split('\n')

corpnames = [c for c in corpnames if not re.findall(r'^\d+', c)]
corpnames = list(set(corpnames))
len(corpnames)
def getCorpInfo(searchname):
    driver.find_element_by_id('SearchTopBar').send_keys(searchname)
    driver.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(3)

    try:
        driver.find_element_by_xpath('//td[@class="NameCell"][1]//a[@href]').click() 
    except:
        try:
            driver.find_element_by_xpath("//a[@id='_profileHelp_Displaysection1__suggestedResults__suggestedResultsRepeater_HyperLink2_0']").click()
        except:
            pass
    time.sleep(3)

    corpinfo = {}
    corpinfo['capitaliqID'] = (re.findall(r'\d+$',driver.current_url)+[''])[0]
    corpinfo['corpname'] = driver.find_element_by_xpath("//*[@id='CompanyHeaderInfo']/span/span[1]").text
    corpinfo['website'] = driver.find_element_by_id('webSite').text
    try:
        corpinfo['numOfEmployees'] = driver.find_element_by_id('numOfEmployees').text
    except:
        corpinfo['numOfEmployees'] = ''
    corpinfo['yearFounded'] = driver.find_element_by_id('yearFounded').text
    corpinfo['address'] = driver.find_element_by_xpath("//span[text()='Primary Office Location']/following::td[3]").text

    person = driver.find_elements_by_xpath("//td/*[contains(text(),'Key Professionals')]/ancestor::tbody[1]//a[@href and not(contains(text(), 'View All'))]")
    title = driver.find_elements_by_xpath("//td/*[contains(text(),'Key Professionals')]/ancestor::tbody[1]//span[not(contains(text(),'Key '))]")

    corpinfo['directors'] = ';'.join([p.text.strip()+":"+t.text.strip() for p,t in list(zip(person, title))])
    try:
        corpinfo['industry'] = driver.find_element_by_xpath("//span[text()='Primary Industry Classification']/following::td[3]").text
    except:
        corpinfo['industry'] = ''

    corpinfo['revenue'] = driver.find_element_by_xpath("//td//*[text()='Total Revenue'][1]/following::*[self::a or self::span][1]").text

    corpinfo['Net Income'] = driver.find_element_by_xpath("//td//*[text()='Net Income'][1]/following::*[self::a or self::span][1]").text
    print(corpinfo)

    return corpinfo

results = []
len(results)
for name in corpnames[:700]:
    try:
        results.append(getCorpInfo(name))
    except Exception as e:
        print('error ', name, '\n',e)
        continue


with open('topcorps.json', 'w') as f:
    f.write(json.dumps(results))

len(results)

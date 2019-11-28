from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors
driver = webdriver.Chrome(executable_path='/usr/lib/python3.6/chromedriver', chrome_options=chrome_options)
driver.get('https://python.org')
print(driver.title)

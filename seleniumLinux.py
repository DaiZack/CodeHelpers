
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors
driver = webdriver.Chrome(executable_path='/home/zdai/chromedriver', chrome_options=chrome_options)

#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.get('https://python.org')
print(driver.title)

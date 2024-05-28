
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.unihomes.co.uk/property/1412023209/birmingham/harborne/5-bedroom-student-house/hilldrop-grove')
script_elements = driver.find_elements(By.TAG_NAME,'script')

target_script = next((s for s in script_elements if 'var property = ' in s.get_attribute('innerHTML')), None)

if target_script:
    scriptContent = target_script.get_attribute('innerText')
    print(scriptContent)
else:
    print('Script element not found')

driver.quit()
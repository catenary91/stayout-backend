import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException

def validate(student_id, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.set_capability('browserName', 'chrome')
    driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
    
    driver.get('https://gonzaga.sogang.ac.kr/home/login/login.jsp')
    driver.find_element(By.ID, 'std_no').send_keys(student_id)
    driver.find_element(By.ID, 'pwd').send_keys(student_id)
    driver.execute_script('login()')
    
    cnt = 0
    while True:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            driver.quit()
            return False
        
        except NoAlertPresentException:
            if driver.current_url == 'https://gonzaga.sogang.ac.kr/home/sub06/sub06_01.jsp':
                driver.quit()
                return True
            
            cnt += 1
            if cnt > 10:
                return False
            
        time.sleep(0.05)
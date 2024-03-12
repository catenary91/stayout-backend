import time
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException

def login(student_id, password) -> webdriver.Remote:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.set_capability('browserName', 'chrome')
    driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
    
    driver.get('https://gonzaga.sogang.ac.kr/home/login/login.jsp')
    driver.find_element(By.ID, 'std_no').send_keys(student_id)
    driver.find_element(By.ID, 'pwd').send_keys(password)
    driver.execute_script('login()')

    return driver

def validate(student_id, password):
    driver = login(student_id, password)
    
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
                driver.quit()
                return False
            
        time.sleep(0.05)

def get_history(student_id: str, password: str) -> None:
    driver = login(student_id, password)

    s_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    e_date = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    driver.get(f'https://gonzaga.sogang.ac.kr/home/sub06/sub06_03_.jsp?s_date={s_date}&e_date={e_date}')

    history_table = driver.find_element(By.CLASS_NAME, 'user_Board').find_elements(By.CSS_SELECTOR, 'tr')[1:]

    history_list = []

    for history in history_table:
        h = history.find_elements(By.CSS_SELECTOR, 'td')
        register_date = h[0].text
        period = h[1].text
        reason = h[3].text
        history_list.append((register_date, period, reason))

    driver.quit()

    return history_list
    

def apply(student_id: str, password: str, start_date: date, end_date: date) -> None:
    driver = login(student_id, password)
    driver.get('https://gonzaga.sogang.ac.kr/home/sub06/sub06_02.jsp')

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    driver.execute_script('document.getElementById("sdate").value = "2024-03-11"')
    driver.execute_script('document.getElementById("edate").value = "2024-03-15"')

    driver.quit()
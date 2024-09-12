import logging
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import config
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import socket
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium_part



logging.basicConfig(level=config.logging_level, filename='log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')



def get_followed_list_apiless():
    global followed_list
    
    options = webdriver.ChromeOptions()
    
    if selenium_part.is_port_in_use(9222):
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    else:
        options.add_experimental_option('detach', True)
    
    options.add_argument(f'--user-data-dir={config.path_to_your_chrome_profile_config}')
    options.add_argument(f'--profile-directory={config.chrome_profile_name}')
    #options.add_argument("--mute-audio")
    
    service = Service(executable_path=config.chromedriver_path)
    driver =  webdriver.Chrome(service=service, options=options)
    
    if selenium_part.is_port_in_use(9222):
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 'n')
        driver.execute_script("window.open('');")
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
    else:
        options.add_experimental_option('--headless=new', True)
    
    driver.get('https://www.twitch.tv/')
    time.sleep(5)
    
    show_more_xpath = '//*[@id="side-nav"]/div/div[1]/div[2]/div[3]/button'
    
    '''minimized = driver.find_element(By.CSS_SELECTOR,'div.InjectLayout-sc-1i43xsx-0.kBtJDm')
    print(minimized)
    if minimized is None:'''
    driver.maximize_window()
    time.sleep(1)
        
        
    if driver.find_element(By.CSS_SELECTOR, 'button.ScCoreButton-sc-ocjdkq-0.ljgEdo.ScButtonIcon-sc-9yap0r-0.eSFFfM').get_attribute('aria-label') not in ('Свернуть боковую навигацию'):
        try:
            expand = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div/div/div[1]/div/button'))
            )
            while expand.is_enabled() and expand.is_displayed():
                expand.click()
                print('expand button clicked')
                break
        except TimeoutException:
            logging.exception(f'Expand button wasnt found in 10s')
            print(f'Expand button wasnt found in 10s')
    
    try:
        show_more = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, show_more_xpath))
        )
        while show_more.is_enabled() and show_more.is_displayed():
            show_more.click()
            
        
    except TimeoutException:
        logging.warning(f"The 'show more' button wasn't found in 10s")
    except Exception as e:
        logging.exception(f"Error occurred while trying to press the 'show more' button: {e}")
    
      
    followed_list = []    
    for i in range(1,config.max_range):
        x = driver.find_element(By.XPATH,f'//*[@id="side-nav"]/div/div[1]/div[2]/div[2]/div[{i}]/div/div/a').get_attribute('href')[22:]
        followed_list.append(x)
    print(followed_list)
            
                
get_followed_list_apiless()
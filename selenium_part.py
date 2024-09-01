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

logging.basicConfig(level=config.logging_level, filename='log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

initial_handles = []

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('127.0.0.1', port)) == 0

def create_driver(detach=False):
    global options
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={config.path_to_your_chrome_profile_config}')
    options.add_argument(f'--profile-directory={config.chrome_profile_name}')
    
    if detach:
        options.add_experimental_option('detach', True)
    else:
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
    if config.mute:
        options.add_argument("--mute-audio")

    service = Service(executable_path=config.chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def refresh_user_token():
    global refreshed_token, driver, initial_handles
    
    if is_port_in_use(9222):
        driver = create_driver(detach=False)
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 'n')
        driver.execute_script("window.open('');")
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
    else:
        driver = create_driver(detach=True)

    initial_handles = driver.window_handles
    driver.get(config.implicit_grant_link)
    refreshed_token = driver.current_url[32:62]
    driver.close()
    return refreshed_token

def open_twitch():
    global driver, initial_handles

    if is_port_in_use(9222):
        driver = create_driver(detach=False)
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 'n')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
    else:
        driver = create_driver(detach=True)

    initial_handles = driver.window_handles
    driver.get(f'https://www.twitch.tv/{config.channel_name}')

    if config.minimize:
        time.sleep(5)
        driver.minimize_window()
    if config.maximize:
        driver.maximize_window()

    reward_thread = threading.Thread(target=run_claim_reward_loop, args=(driver,))
    reward_thread.start()

def close_browser():
    global driver, initial_handles
    if driver is not None:
        try:
            current_handles = driver.window_handles
            if len(current_handles) > 1:
                for handle in current_handles:
                    driver.switch_to.window(handle)
                    if handle not in initial_handles:
                        driver.close()
                
                if initial_handles:
                    driver.switch_to.window(initial_handles[0])
            
            if len(driver.window_handles) == 1:
                driver.quit()
            
        except Exception as e:
            logging.exception(f"Error occurred while closing the browser: {e}")
        finally:
            driver = None
            logging.info("Browser closed successfully")

def claim_reward(driver):
    logging.debug('Trying to find and press the button')

    xpaths = {
        "7tv_xpath": '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/seventv-container/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div/div/button',
        "no7tv_xpath": '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button'
    }

    while True:
        button = None
        for key, xpath in xpaths.items():
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if button.is_enabled() and button.is_displayed():
                    button.click()
                    logging.info(f"Claimed reward using {key}")
                    print(f"Claimed reward using {key}")
                    return
                else:
                    logging.info(f"The button was found using {key}, but it's inactive")

            except TimeoutException:
                logging.warning(f"The button wasn't found using {key} in 10s, trying next XPath")
            except Exception as e:
                logging.exception(f"Error occurred while trying to press the button using {key}: {e}")

        logging.info("Retrying in 240 seconds...")
        time.sleep(240)

def run_claim_reward_loop(driver):
    logging.info('Start checking for reward')
    while True:
        claim_reward(driver)
        time.sleep(240)

import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By as by
import config
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir={config.path_to_your_chrome_profile_config}')
options.add_argument(f'--profile-directory={config.chrome_profile_name}')
options.add_experimental_option('detach', True)

driver = None

def refresh_user_token():
    global refreshed_token
    service = Service(executable_path=config.chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(config.implicit_grant_link)
    refreshed_token = driver.current_url[32:62]
    driver.close()
    return refreshed_token

def open_twitch():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={config.path_to_your_chrome_profile_config}')
    options.add_argument(f'--profile-directory={config.chrome_profile_name}')
    options.add_experimental_option('detach', True)

    if config.mute == True:
        options.add_argument("--mute-audio")

    service = Service(executable_path=config.chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f'https://www.twitch.tv/{config.channel_name}')

    if config.minimize == True:
        time.sleep(5)
        driver.minimize_window()
    if config.maximize == True:
        driver.maximize_window()

    reward_thread = threading.Thread(target=run_claim_reward_loop, args=(driver,))
    reward_thread.start()

def close_browser():
    global driver
    if driver is not None:
        driver.close()
        driver = None
        logging.info("Browser closed successfully")

def claim_reward(driver):
    logging.debug('Trying to find and press the button')
    
    if config.extension == True:
        button_xpath = '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/seventv-container/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div/div/button'
    else:
        button_xpath = '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button'
    
    while True:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by.XPATH, button_xpath))
            )

            if button.is_enabled() and button.is_displayed():
                button.click()
                print("Claimed reward")
                logging.info("Claimed reward")
                break
            else:
                logging.info("The button was found, but it's inactive")

                
        except TimeoutException:
            logging.warning("The button wasn't found in 10s, retrying")
        except Exception as e:
            logging.exception(f"Error occurred while trying to press the button: {e}")

        time.sleep(240)

def run_claim_reward_loop(driver):
    logging.info('Start checking for reward')
    while True:
        claim_reward(driver)
        time.sleep(240)
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
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(level=config.logging_level, filename='log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


browser_closed = False


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

    service = Service(executable_path=config.chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def refresh_user_token():
    global refreshed_token, driver
    
    if is_port_in_use(9222):
        driver = create_driver(detach=False)
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 'n')
        driver.execute_script("window.open('');")
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
    else:
        driver = create_driver(detach=True)
        
    driver.get(config.implicit_grant_link)
    refreshed_token = driver.current_url[32:62]
    driver.close()
    return refreshed_token

def open_twitch():
    global driver

    if is_port_in_use(9222):
        driver = create_driver(detach=False)
        driver.find_element('tag name', 'body').send_keys(Keys.CONTROL + 'n')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
    else:
        driver = create_driver(detach=True)

    driver.get(f'https://www.twitch.tv/{config.channel_name}')

    if config.mute:
        actions = ActionChains(driver) 
        actions.send_keys("m")
        actions.perform()
        
    time.sleep(3)
    
    try:
        chat_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-labelledby="chat-room-header-label"]'))
        )
        if not chat_element.is_displayed():
            logging.info("Chat element is present but not visible.")
            actions = ActionChains(driver)
            actions.key_down(Keys.ALT).send_keys('r').perform()
            logging.info("Alt + R pressed to open chat.")
            print("Alt + R pressed to open chat.")
    except Exception as e:
        logging.exception(f"Error locating chat element: {e}")
        print(f"Error locating chat element: {e}")
    else:
        logging.info("Chat element is visible and accessible.")
        print("Chat element is visible.")
        

    if config.minimize:
        driver.minimize_window()
    if config.maximize:
        driver.maximize_window()

    reward_thread = threading.Thread(target=run_claim_reward_loop, args=(driver,))
    reward_thread.start()

def close_browser():
    global driver
    
    try:
        print(len(driver.window_handles))
        logging.info(f"Number of opened tabs = {len(driver.window_handles)}")
        if len(driver.window_handles) > 1:
            driver.close()
            logging.info("Twitch tab closed. Other tabs still open.")
        else:
            driver.quit()
            logging.info("Twitch tab closed. No other tabs open. Browser closed.")

    except Exception as e:
        logging.exception(f"Error occurred while closing the Twitch tab: {e}")
    finally:
        driver = None


def claim_reward(driver):
    logging.debug('Trying to find and press the button')
    
    xpaths = {
        "7tv_xpath": '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/seventv-container/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div/div/button',
        "no7tv_xpath": '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/div[6]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button',
        "error_button": '//*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[5]/div/div[3]/button'
    }

    while True:
        button = None
        for key, xpath in xpaths.items():
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if button.is_enabled() and button.is_displayed() and key != 'error_button':
                    button.click()
                    logging.info(f"Claimed reward using {key}")
                    print(f"Claimed reward using {key}")
                    return
                elif button.is_enabled() and button.is_displayed() and key == 'error_button':
                    button.click()
                    logging.info("Error button found, triggering error handling.")
                    print("Error button found, triggering error handling.")
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
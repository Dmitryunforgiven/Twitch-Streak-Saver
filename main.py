import requests
import time
import logging
import threading
import selenium_part
from selenium_part import refresh_user_token, close_browser
import config
from selenium_part import browser_closed
clientId = config.client_id
userId = config.userId

logging.basicConfig(level=config.logging_level, filename='log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def get_followed_list():
    global headers, data, counter, previous_channels, oAuth
    logging.info("Starting get_followed_list")
    logging.info('Trying to refresh user token')
    time.sleep(10)
    selenium_part.refresh_user_token()
    
    oAuth = selenium_part.refreshed_token
    print(oAuth)
    
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Authorization': 'Bearer ' + oAuth,
        'Client-ID': clientId,
    }
    
    try:
        response = requests.get(f'https://api.twitch.tv/helix/streams/followed?user_id={userId}', headers=headers)
        data = response.json()
        numStreams = len(data["data"])
        
    except (KeyError, ValueError) as e:
        logging.error(f'Unable to get user token automatically: {e}. Retrying...')
        get_followed_list()
        return

    z = {
        'Authorization': f'OAuth {oAuth}'
    }
    validation = requests.get('https://id.twitch.tv/oauth2/validate', headers=z)
    validation = validation.json()
    logging.debug(f'Token details: {validation}')

    print("\nCHANNEL " + ' '*13 + "GAME" + ' '*37 + "VIEWERS" + '  ' + "STATUS" + ' '*8 + "\n" + '-'*80)
    logging.info("CHANNEL " + ' '*13 + "GAME" + ' '*37 + "VIEWERS" + '  ' + "STATUS" + ' '*8 + "\n" + '-'*80)
    
    for i in range(numStreams):
        channelName = data["data"][i]["user_name"]
        channelGame = data["data"][i]["game_name"]
        channelViewers = str(data["data"][i]["viewer_count"])
        streamType = data["data"][i]["type"]
        
        if streamType != 'live':
            streamType = '(vodcast)'

        if len(channelName) > 18:
            channelName = channelName[:18] + '..'
        if len(channelGame) > 38:
            channelGame = channelGame[:38] + '..'

        print(f'{channelName.ljust(20)} {channelGame.ljust(40)} {channelViewers.ljust(8)} {streamType}')
        logging.info(f'{channelName.ljust(20)} {channelGame.ljust(40)} {channelViewers.ljust(8)} {streamType}')
    
    print('-'*80)
    logging.info('-'*80)
    
    previous_channels = {stream['user_name']: stream['type'] for stream in data['data']}
    counter = 1
    
    status_thread = threading.Thread(target=check_selected_channels_status, daemon=True)
    status_thread.start()

    for stream in data['data']:
        if stream['user_name'] == config.channel_name and stream['type'] == 'live':
            selenium_part.open_twitch()
            return

    
    status_thread.join()

def check_selected_channels_status():
    global counter, even_iter_status, uneven_iter_status, previous_channels
    error_is_thrown = False

    while True:
        try:
            response = requests.get(f'https://api.twitch.tv/helix/streams/followed?user_id={userId}', headers=headers, timeout=10)
            updated_data = response.json()
            counter += 1

            if counter % 2 == 0:
                even_iter_status = updated_data
            else:
                uneven_iter_status = updated_data

            if counter > 1:
                if counter % 2 == 0:
                    compare_statuses(even_iter_status, previous_channels, error_is_thrown)
                else:
                    compare_statuses(uneven_iter_status, previous_channels, error_is_thrown)

            previous_channels = {stream['user_name']: stream['type'] for stream in updated_data['data']}

            time.sleep(config.delay)

        except requests.RequestException as e:
            logging.error(f"Error fetching stream data: {e}. Retrying...")
            time.sleep(config.delay)

def compare_statuses(current_status, previous_status, error_is_thrown):
    global current_channel_status

    previous_channel_status = previous_status.get(config.channel_name, 'offline')

    for stream in current_status['data']:
        if stream['user_name'] == config.channel_name:
            current_channel_status = stream['type']
            break
    else:
        current_channel_status = 'offline'
        
    if error_is_thrown:
        previous_channel_status = 'live'
        current_channel_status  = 'offline'
        error_is_thrown = False

    if previous_channel_status == 'offline' and current_channel_status == 'live':
        print(f"{config.channel_name} is now online. Opening Twitch.")
        logging.info(f"{config.channel_name} is now online. Opening Twitch.")
        selenium_part.open_twitch()

    elif previous_channel_status == 'live' and current_channel_status == 'offline':
        if not selenium_part.browser_closed:
            print(f"{config.channel_name} went offline. Closing browser.")
            logging.info(f"{config.channel_name} went offline. Closing browser.")
            selenium_part.close_browser()

    print(f"{config.channel_name} status change from {previous_channel_status} to {current_channel_status}")
    logging.info(f"{config.channel_name} status change from {previous_channel_status} to {current_channel_status}")
    previous_status[config.channel_name] = current_channel_status


if __name__ == '__main__':
    even_iter_status = None
    uneven_iter_status = None

    get_followed_list()

    while True:
        time.sleep(1)
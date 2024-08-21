import requests
import config


def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'client_id={config.client_id}&client_secret={config.client_secret}&grant_type=authorization_code'
    z = f'https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={config.client_id}&redirect_uri=https://localhost&scope=user&read&follows'
    response_token = requests.post(z, headers=headers)
    global token
    token = response_token.json()['access_token']
    print(token)
    return token
    
#get_token()

def get_userinfo():
    get_token()
    headers = {
    'Authorization': f'Bearer {token}',
    'Client-Id': config.client_id
    }
    
    response_userinfo = requests.get('https://api.twitch.tv/helix/users?login=twitchdev', headers=headers)
    global userid
    userid = response_userinfo.json()['data'][0]['user_name']
    print(token, userid)
    return userid



def validate_token():
    
    headers = {
        
        #'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'OAuth h866kf5r8t4dtt418pvqsamhvqn6gd'
    }
    
    #data = f'grant_type=refresh_token&refresh_token=nbvhfioo2tzxnde7xm656lrln0rop1&client_id={config.client_id}&client_secret={config.client_secret}'
    validation = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
    #refreshed_token_fr = refreshed_token_fr.json()
    validation = validation.json()
    print(validation)

validate_token()
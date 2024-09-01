# Twitch API stuff
client_secret = "insert your app's client secret"
client_id = "Insert your app's client id"
redirect_uri = "Insert your app's redirect uri"


# Chrome profile config
# This is needed in order to use cookies from your chosen chrome profile so the everytime login isn't needed
windows_username = 'insert your windows username'
path_to_your_chrome_profile_config = f'C:/Users/{windows_username}/AppData/Local/Google/Chrome/User Data'
chrome_profile_name = 'insert your profile name'


# Path to the chromedriver, which is required for selenium, i just put in the working directory
chromedriver_path = r'.\chromedriver.exe'


# User OAuth link to get the list of followed channels
implicit_grant_link = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=token&scope=user:read:follows"


# https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
userId = 'insert your userId'


# Specify the needed twitch channel
channel_name = 'insert your chosen twitch channel'


# Status check frequency (sec)
delay = 300


# Opened window settings
# Mute works only if there were no windows opened by a user
mute = False
maximize = False
minimize = False


#Use either INFO or DEBUG
logging_level = 'INFO'

# TTV Streak Saver

TTV Streak Saver is a simple tool that uses Selenium Chromedriver and the Twitch Helix API to address a specific need: maintaining your view streak on a particular Twitch channel when you're not at home. This tool monitors the status of a selected Twitch channel and automatically opens a Chrome window with specified settings from the configuration file when the channel goes live. It collects points and streak rewards by clicking the relevant button. The window will close, and the tool will resume monitoring when the channel goes offline, reconnecting if the stream goes live again.

## Requirements

- A registered app on [Twitch Developer](https://dev.twitch.tv/)
- For initial setup, manually open the `implicit_grant_link` from the config file to connect your app and retrieve the `userId`
- A populated config file with your data
- Google Chrome browser (required for Chromedriver):
- Chromedriver that matches your browser version, placed in the working directory:
    - [Download Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads)
- Chromedriver path added to your Windows PATH
    - [Chromedriver Setup Guide](https://www.youtube.com/watch?v=W4bHb1BsbnU)

## How to Run the App

1. Activate your Python virtual environment.
2. Install the required packages listed in `requirements.txt`.
3. Run the `.bat` file or execute the main script directly.


    
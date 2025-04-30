# No longer works with the latest chrome versions (29.05.2025 update, 136. versions)
```
https://developer.chrome.com/blog/remote-debugging-port
```


# TTV Streak Saver

TTV Streak Saver is a tool that uses Selenium WebDriver and the Twitch Helix API to maintain your view streak on a Twitch channel when you're not at home. It monitors the status of a selected Twitch channel and automatically opens a Chrome window with specified settings from the configuration file when the channel goes live. The tool collects points and streak rewards by clicking the relevant button. The window will close, and the tool will resume monitoring when the channel goes offline, reconnecting if the stream goes live again.

## Requirements

- Severe autism
- A registered app on [Twitch Developer](https://dev.twitch.tv/)
- For initial setup, manually open the `implicit_grant_link` from the config file to connect your app to your twitch account
- A config file populated with your data
- Google Chrome browser (required for Chromedriver):
- Chromedriver that matches your browser version, placed in the working directory:
    - [Download Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads)
- Chromedriver path added to your Windows PATH
    - [Chromedriver Setup Guide](https://www.youtube.com/watch?v=W4bHb1BsbnU)

## Modifying Chrome Shortcut for Selenium

To ensure that Selenium WebDriver can connect to Chrome, you need to modify the Chrome shortcut on your desktop to include specific flags. These flags enable remote debugging, which is essential for Selenium to control Chrome effectively.


### Steps to Modify Chrome Shortcut:

1. **Locate the Chrome Shortcut:**
   - Find the Google Chrome shortcut on your desktop or in the Start menu.

2. **Open Shortcut Properties:**
   - Right-click the shortcut and select `Properties`.

3. **Modify Target Path:**
   - In the `Shortcut` tab, find the `Target` field. It will look something like this:
     ```
     "C:\Program Files\Google\Chrome\Application\chrome.exe"
     ```
   - Add the following flags to the end of the target path:
     ```
     --remote-debugging-port=9222 --user-data-dir="C:\Path\To\Your\Chrome\User\Data"
     ```
   - Ensure the entire path is enclosed in quotes. The modified `Target` field should look like this:
     ```
     "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Path\To\Your\Chrome\User\Data"
     ```
   - Adjust the path to `user-data-dir` to point to your actual Chrome user data directory.

4. **Apply Changes:**
   - Click `Apply` and then `OK` to save the changes.

### Why Modify the Shortcut?

**1. Enable Remote Debugging:**
   - Adding `--remote-debugging-port=9222` allows Chrome to accept remote debugging connections on port 9222. This is required for Selenium WebDriver to connect to and control the Chrome instance.

**2. Use a Specific User Profile:**
   - The `--user-data-dir` flag specifies the directory where Chrome stores user profile data. This ensures that Selenium interacts with the correct profile and preserves cookies and session information between browser restarts.

## How to Run the App

1. Activate your Python virtual environment.
2. Install the required packages listed in `requirements.txt`.
3. Run the `main.py` script directly using Python.
4. Or run the included `streak.bat` file.

## Monitor Logs

Logs are saved in `log.log` for tracking application actions and status changes.

## Configuration

Ensure that the `config.py` file is correctly set up with the following parameters:

- `client_id`: Your Twitch application client ID.
- `userId`: Your Twitch user ID.
- `redirect_uri`: Your Twitch application redirect URI.
- `channel_name`: The name of the Twitch channel to monitor.
- `path_to_your_chrome_profile_config`: Path to your Chrome user profile.
- `chrome_profile_name`: Name of your Chrome profile.
- `chromedriver_path`: Path to your ChromeDriver executable.
- `mute`: Mutes the opened window.
- `maximize`: Maximizes the opened window.
- `minimize`: Minimizes the opened window.

## Troubleshooting

- Ensure ChromeDriver is compatible with your installed version of Google Chrome.
- Verify that all paths and configuration settings are correct.
- Enable DEBUG logs and check log.log for detailed error messages and stack traces.

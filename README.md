# TheDailyPoster  
Script that checks for new [Thedaily](https://www.nytimes.com/column/the-daily) articles and makes a post to [r/Buckethead](https://www.reddit.com/r/Buckethead/) when a new article is found.

## Installation
- [Install Python](https://www.python.org/downloads/). Add to PATH during the installation.  
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Unzip the ZIP file.
- Open your command prompt and change your directory to that of the unzipped files ```cd unzippedfoldername```.  
- Install the required packages  :
  ```
  pip install -U praw feedparser lxml
  ```
## Configuration
- [Create a Reddit App](https://www.reddit.com/prefs/apps/)(script) and get your ```client_id``` and ```client_secret```.  
- Edit the ```config.ini``` file with your details and save:
  ```
  [REDDIT]
  CLIENT_ID = your_client_id
  CLIENT_SECRET = your_client_secret
  PASSWORD = your_reddit_password
  USERNAME = your_reddit_username
  ```

## Running the script
Replace '\path\to\the\main.py' with the actual path to the main.py script.  
The task can be triggered every six hours: 
- Windows:  
  ```
  schtasks /create /sc hourly /mo 6 /tn TheDailyPoster /tr "python C:\path\to\the\main.py"
  ```

- Linux:
  ```
  0 */6 * * * /path/to/python /path/to/the/main.py
  ```

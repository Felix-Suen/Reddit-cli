# Reddit Simple Command Line Interface

### Seemingly productive yet unproductive tool for redditors
Windows/MacOS/Linux supported. 


### Getting Started
Make sure all libraries are installed with pip
```python
import praw
from functools import partial
import platform
from colorama import Fore, Style
from PIL import Image
import urllib
```
Change login credentials to your own Reddit Developer App

```python
reddit = praw.Reddit(client_id= 'YOUR_CLIENT_ID',
                     client_secret= 'YOUR_CLIENT_SECRET',
                     username= 'YOUR_REDDIT_USERNAME',
                     password= 'YOUR_REDDIT_PASSWORD',
                     user_agent= 'anystring')
```
Run the program
```powershell
python readit.py
```
### Happy Browsing!
![alt text](https://github.com/Felix-Suen/Reddit-cli/blob/master/start.png)

### Commands
> -h h help         Get a list of commands
> lm                Display the all comments in the current post
> up                Upvote the current post
> down              Downvote the current post
> asc               View image as ASCII art
> v                 View the image without downloading
> b                 Back to the subreddit
> r                 Reset the program
> q quit            Quit the program

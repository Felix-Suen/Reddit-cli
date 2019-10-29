# Reddit Simple Command Line Interface

### Seemingly productive yet unproductive tool for redditors
Windows/MacOS/Linux supported. 

### Demo


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



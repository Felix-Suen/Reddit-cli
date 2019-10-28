import praw
from functools import partial
import os
import credentials
import platform
from colorama import Fore, Style
from PIL import Image
import urllib

####################### Credentials ##################################
reddit = praw.Reddit(client_id=credentials.login['client_id'],
                     client_secret=credentials.login['client_secret'],
                     username=credentials.login['username'],
                     password=credentials.login['password'],
                     user_agent=credentials.login['user_agent'])
######################################################################

continued = True
viewing = False
subred = None
vote = False

def get_posts():
    clear()
    global subred
    if subred == None:
        print('Subreddit: ')
        subred = input()
    print(90 * '-')
    subreddit = reddit.subreddit(subred)
    top_posts = subreddit.hot(limit=20)
    top = []
    for index, submission in enumerate(top_posts):
        print(str(index + 1) + '. ' + submission.title)
        top.append(submission)

    print(90 * '-')
    print('choose a post: ')
    number = input()
    try:
        number = int(number) - 1
    except ValueError:
        print("not a valid number \n")
        get_posts()

    print('\n' + 'Upvotes: ' + Fore.GREEN + str(top[number].score) + Style.RESET_ALL)
    print('\n' + top[number].selftext + '\n' + top[number].url)
    print('\n' + 40 * '-' + 'END OF POST' + 40 * '-' + '\n')

    return top[number]


def open_image(top_post):
    if top_post.url.endswith('jpg') or top_post.url.endswith('png'):
        urllib.request.urlretrieve(top_post.url, "img.jpg")
        path = "img.jpg"
        image = Image.open(path)
        image.show()
        global viewing
        viewing = True
    else:
        print(Fore.RED + '\n ***No image in the post*** \n' + Style.RESET_ALL)


def img_to_ascii(top_post):
    if top_post.url.endswith('jpg') or top_post.url.endswith('png'):
        urllib.request.urlretrieve(top_post.url, "img.jpg")
        path = "img.jpg"
        image = Image.open(path)
        # implement Ascii Converter
        global viewing
        viewing = True
    else:
        print(Fore.RED + '\n ***No image in the post*** \n' + Style.RESET_ALL)

def get_comment(top_post):
    top_post.comments.replace_more(limit=0)
    for comment in top_post.comments:
        print('{' + str(comment.score) + '} >> ' + comment.body)
    print('\n' + 40 * '-' + 'END OF Comments' + 40 * '-' + '\n')


###################### Bottom up sorting algorithm ######################
def all_comments(top_post):
    top_post.comments.replace_more(limit=0)
    comments = top_post.comments.list()
    d = {}
    for comment in comments:
        if comment.id not in d.keys():
            d[comment.id] = {'id': comment.id,
                             'parent_id': comment.parent().id,
                             'body': comment.body,
                             'upvote': comment.score,
                             'children': []}

    for c in list(d.keys())[::-1]:
        comment = d[c]
        if comment['parent_id'] != top_post.id:
            d[comment['parent_id']]['children'].append(comment)
            del d[c]

    p(list(d.values()), top_post.id)


#########################################################################

def upvote(top_post):
    global vote
    if vote is False:
        top_post.upvote()
        vote = True
        print('\n***Upvoted***\n')
    else:
        top_post.clear_vote()
        vote = False
        print('\n***Cleared Vote***\n')

def downvote(top_post):
    global vote
    if vote is False:
        top_post.downvote()
        vote = True
        print('\n***Downvoted***\n')
    else:
        top_post.clear_vote()
        vote = False
        print('\n***Cleared Vote***\n')

def p(coms, post_id, depth=0):
    for comobj in coms:
        if comobj['parent_id'] == post_id:
            print('-' * 90)
        print(depth * '>>>> ' + '[' + Fore.GREEN + str(comobj['upvote']) + Style.RESET_ALL + '] '
              + comobj['body'] + '\n')
        if len(comobj['children']) > 0:
            p(comobj['children'], post_id, depth=depth + 1)


def back():
    clear()
    global post_lst
    post_lst = get_posts()


def reset():
    clear()
    global post_lst, subred
    subred = None
    post_lst = get_posts()


def stop_browsing():
    global continued
    continued = False
    clear()


def help():
    print(
        "\n(m) Top comments for this post \n"
        "(lm) All comments for this post \n"
        "(b) Back to subreddit \n"
        "(r) Reset program"
        "(q or quit) Stop browsing \n"
    )
    looper()


def clear():
    windows = platform.system() == 'Windows'
    os.system('cls') if windows else os.system('clear')


#########################################################################
# Endless Browse

def looper():
    global viewing
    if viewing:
        os.remove('img.jpg')
        viewing = False
    print('options: ')
    try:
        num = input()
    except TypeError:
        print("\n \n")
        looper()

    switcher = {
        'm': partial(get_comment, post_lst),
        'lm': partial(all_comments, post_lst),
        'up': partial(upvote, post_lst),
        'down': partial(downvote, post_lst),
        'asc': partial(img_to_ascii, post_lst),
        'b': back,
        'back': back,
        'r': reset,
        'q': stop_browsing,
        'quit': stop_browsing,
        'v': partial(open_image, post_lst),
        '-h': help,
        'h': help,
        'help': help
    }
    func = switcher.get(num, lambda: "invalid option")
    func()


#########################################################################
# Run
post_lst = get_posts()
while continued:
    looper()
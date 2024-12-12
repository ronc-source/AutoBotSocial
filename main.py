import praw
from RedDownloader import RedDownloader
import yaml
from yaml import Loader

# Load YAML configuration
stream = open("configuration.yaml", 'r')
dictionary = yaml.load(stream, Loader=Loader)

# Reddit API credentials
CLIENT_ID = dictionary['client_id']
CLIENT_SECRET = dictionary['client_secret']
USER_AGENT = dictionary['user_agent']

# Directory to save videos from Reddit
DOWNLOAD_DIR = dictionary['download_dir']

# SubReddit for videos
SUBREDDIT = dictionary['subreddit']


def redditInstance():
    return praw.Reddit(client_id=CLIENT_ID, 
                       client_secret=CLIENT_SECRET, 
                       user_agent=USER_AGENT)

def findLatestVideoPost(redditAccess):
    subredditAccess = redditAccess.subreddit(SUBREDDIT)
    for post in subredditAccess.hot():
        if post.is_video:
            print(f"Found video titled: {post.title}")
            return post

def downloadVideoPost(post):
    RedDownloader.Download(post.url, output=post.title, destination=DOWNLOAD_DIR)

def main():
    redditAccess = redditInstance()
    post = findLatestVideoPost(redditAccess)
    downloadVideoPost(post)
    

if __name__ == "__main__":
    main()
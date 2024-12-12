import praw
import requests
import moviepy
import yaml
from yaml import Loader

# Reddit API credentials
stream = open("credentials.yaml", 'r')
dictionary = yaml.load(stream, Loader=Loader)
CLIENT_ID = dictionary['client_id']
CLIENT_SECRET = dictionary['client_secret']
USER_AGENT = dictionary['user_agent']

# Directory to save videos from Reddit
DOWNLOAD_DIR = "downloads"

# SubReddit for videos
SUBREDDIT = "discordVideos"


def redditInstance():
    return praw.Reddit(client_id=CLIENT_ID, 
                       client_secret=CLIENT_SECRET, 
                       user_agent=USER_AGENT)

def getLatestVideo(redditAccess):
    subredditAccess = redditAccess.subreddit(SUBREDDIT)
    for post in subredditAccess.hot():
        if post.is_video:
            print(f"Found video titled: {post.title}")
            return post

def main():
    redditAccess = redditInstance()
    video = getLatestVideo(redditAccess)
    

if __name__ == "__main__":
    main()
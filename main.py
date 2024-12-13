import http.server
import json
import praw
import requests
import socketserver
import threading
import time
from RedDownloader import RedDownloader
import yaml
from yaml import Loader

# Load YAML configuration
stream = open("configuration.yaml", 'r')
config = yaml.load(stream, Loader=Loader)

# Reddit API
REDDIT_CLIENT_ID = config['reddit']['client_id']
REDDIT_CLIENT_SECRET = config['reddit']['client_secret']
REDDIT_USER_AGENT = config['reddit']['user_agent']
SUBREDDIT = config['reddit']['subreddit']

# Instagram API
INSTA_API_VERSION = config['instagram']['api_version']
INSTA_USER_ID = config['instagram']['user_id']
INSTA_ACCESS_TOKEN = config['instagram']['access_token']
INSTA_URL = config['instagram']['url']

# Video management
DOWNLOAD_DIR = config['download_dir']
MAX_VID_DURATION = 60

# Setup localhost website for ngrok reverse proxy
PORT = config['localhost']['port']
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()
print(f"Localhost serving at port {PORT}")

NGROK_PROXY = config['agent']['ngrok_proxy_downloads']


def redditInstance():
    return praw.Reddit(client_id=REDDIT_CLIENT_ID, 
                       client_secret=REDDIT_CLIENT_SECRET, 
                       user_agent=REDDIT_USER_AGENT)

def findandDownloadLatestVideoPost(redditAccess):
    subredditAccess = redditAccess.subreddit(SUBREDDIT)
    for post in subredditAccess.hot(limit=10):
        if post.is_video and post.media:
            duration = post.media['reddit_video']['duration']
            if duration < MAX_VID_DURATION:
                # Remove special characters from post name
                filterPostTitle = ''.join(i for i in post.title if i.isalnum() or i == " ")
                print(f"Found video titled: {filterPostTitle}")
                print("Attempting video download")
                try:
                    RedDownloader.Download(post.url, output=filterPostTitle, destination=DOWNLOAD_DIR)
                except:
                    print("Video download failed... searching for new video")
                    continue
                return post
    return None

def uploadToInstagram(post):
    # Fetch ID
    APIVersion = INSTA_API_VERSION
    userID = INSTA_USER_ID
    accessToken = INSTA_ACCESS_TOKEN
    APIurl = INSTA_URL

    url = f"{APIurl}/{APIVersion}/{userID}?fields=id,username&access_token={accessToken}"
    response = requests.get(url)
    instagramUser = json.loads(response.content)['username']
    instagramID = json.loads(response.content)['id']

    # Create media container
    filterPostTitle = ''.join(i for i in post.title if i.isalnum() or i == " ")
    videoURL = NGROK_PROXY + filterPostTitle + ".mp4"
    videoURL = videoURL.replace(" ", "%20")
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "caption" : f'''{filterPostTitle}
                        .
                        .
                        .
                        {config['instagram']['hashtags']}''',
        "media_type" : "REELS",
        "video_url" : videoURL,
        "access_token" : accessToken
    }
    url = f"{APIurl}/{APIVersion}/{instagramID}/media"
    response = requests.post(url=url, headers=headers, data=data)
    containerID = json.loads(response.content)['id']

    #Check container status
    url = f"{APIurl}/{APIVersion}/{containerID}?fields=status&access_token={accessToken}"
    response = requests.get(url)
    containerStatus = json.loads(response.content)['status']
    print("Media Container Initial Status:", containerStatus)

    while containerStatus == "IN_PROGRESS":
        time.sleep(30)
        response = requests.get(url)
        containerStatus = json.loads(response.content)['status']
    
    print("Container Status Final Status:", containerStatus)

    # Publish media container
    url = f"{APIurl}/{instagramID}/media_publish"
    data = {
        "creation_id" : containerID,
        "access_token" : accessToken
    }
    response = requests.post(url=url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"Media Container Successfully Published to Instagram for Username: {instagramUser}")
    else:
        print(response.content)
        raise Exception("Media Container Failed to Publish")

def main():
    redditAccess = redditInstance()
    post = findandDownloadLatestVideoPost(redditAccess)
    if post != None:
        uploadToInstagram(post)
    httpd.shutdown()
    

if __name__ == "__main__":
    main()
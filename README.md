<a id="readme-top"></a>

<!-- PROJECT SHIELD -->
![Unlicense License][license-shield]



<!-- ABOUT THE PROJECT -->
## About The Project

This project automates the process of using the Reddit and Instagram API to download the latest trending video from a given subreddit and upload it to a specified Instagram account.

Since the Instagram API requires that you provide a public URL link to your media content we setup an ngrok public facing tunnel to our localhost machine. This allows us to generate a public link to our local download folder to which the API can access.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The major components used to setup the project:
* Python
* YAML
* ngrok
* RedDownloader
* requests
* socketserver
* praw

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The instructions below provide a reference to how set up and run the project locally.

### Prerequisites

You will need to setup the following accounts:
* Reddit
* Instagram
* Meta Developer
* ngrok

You will also need to create the following apps to get the required API credentials such as the client ID, client secret, user agent, access token and user ID:
* Reddit App
* Meta App

### Installation

_Please make sure to pip install all required libraries specified at the header of the main.py file._

1. Clone the repo
   ```sh
   git clone https://github.com/ronc-source/AutoBotSocial.git
   ```
2. Create a configuration.yaml file that follows this layout and fill it with your specifications. Save this in the same directory as main.py.
   ```sh
   ---
   download_dir:
   localhost:
     port:
   reddit:
     client_id:
     client_secret:
     subreddit:
     user_agent:
   agent:
     ngrok_proxy_downloads: <link to public facing ngrok tunnel>
   instagram:
     access_token:
     api_version:
     hashtags:
     user_id:
     url:
   ...
   ```
3. Go on your ngrok dashboard and create a tunnel. In the request header remove the warning banner. Start the tunnel and make sure the port used for the tunnnel matches your localhost port in the configuration.yaml file.
4. Create a folder named downloads in the same directory as the main.py script.
5. Run the main.py file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the Unlicense License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge

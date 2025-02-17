from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import time
import os
import psutil
from dotenv import load_dotenv

load_dotenv()

TARGET_CHHANNEL 'wearethevr'
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CUSTOM_MESSAGE = "A stream elkezdődött!"
TARGET_APPS = ["program1.exe", "program2.exe"]
USER_SCOPE = [AuthScope.USER_READ_STREAM_KEY]
REDIRECT_URI = 'http://localhost:17563'
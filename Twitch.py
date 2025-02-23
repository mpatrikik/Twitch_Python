from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
import time
import os
import psutil
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
import asyncio

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_SCOPE = [AuthScope.CHANNEL_READ_STREAM_KEY]
REDIRECT_URI = 'http://localhost:17563'


def close_app(app_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app_name:
            try:
                p = psutil.Process(proc.info['pid'])
                p.terminate()
                try:
                    p.wait(timeout=5)
                except psutil.TimeoutExpired:
                    p.kill()
                print(f"{app_name} closed.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


async def main():
    try:
        twitch = Twitch(CLIENT_ID, CLIENT_SECRET)
        print("Twitch object created.")
        await twitch.authenticate_app([])
        print("App authenticated.")
        auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False, url=REDIRECT_URI)
        token, refresh_token = await auth.authenticate()
        print("User authenticated.")
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        print("All authentication set.")
    except Exception as e:
        print(f"Error during Twitch API authentication: {e}")
        exit()

    channel_name = input("Please add the channel name: ")

    try:
        stream_data = []
        async for response in twitch.get_streams(user_login=[channel_name]):
            stream_data.append(response)
        if stream_data:
            print(f"The {channel_name} is streaming now.")
            streaming = True
        else:
            print(f"The {channel_name} is not streaming now.")
            streaming = False
    except Exception as e:
        print(f"Error while querying channel status: {e}")
        exit()


    while streaming:
        try:
            await asyncio.sleep(30)
            stream_data = []
            async for response in twitch.get_streams(user_login=[channel_name]):
                stream_data.append(response)

                if not stream_data:
                    print("The stream ended!")
                    streaming = False
                    close_app("chrome.exe")

                    root = tk.Tk()
                    root.withdraw()

                    result = messagebox.askyesno("End of stream", "Want to shut down the PC?")

                    if result:
                        print("Shutting down...")
                        os.system("shutdown /s /t 5")
                    else:
                        print("Script ends.")
                    root.destroy()
                    break
        except Exception as e:
            print(f"Error while checking: {e}")

if __name__ == '__main__':
    asyncio.run(main())
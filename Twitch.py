from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
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
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app_name:
            try:
                p = psutil.Process(proc.info['pid'])
                p.terminate()
                try:
                    p.wait(timeout=5)
                except psutil.TimeoutExpired:
                    p.kill()
                count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    if count > 0:
        print(f"{count} instances of {app_name} closed.")


async def show_chrome_dialog(message, title):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        result = await asyncio.to_thread(messagebox.askyesno, title, message)
        return result
    finally:
        root.destroy()

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

    while True:
        channel_name = input("\nPlease enter the channel name: ")
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

        if not streaming:
            while True:
                retry = input("Do you want to check another channel(Y/N): ").strip().upper()
                if retry == 'Y':
                    break
                elif retry == 'N':
                    print("Script ends.")
                    return
                else:
                    print("Invalid input. Please enter 'Y' or 'N'!")

        else:
            while streaming:
                try:
                    await asyncio.sleep(10)
                    stream_data = []
                    async for response in twitch.get_streams(user_login=[channel_name]):
                        stream_data.append(response)

                    if not stream_data:
                        print("The stream ended!")
                        streaming = False

                        try:
                            close_chrome = await asyncio.wait_for(show_chrome_dialog("Want to close Chrome?", "End of stream"), timeout=30)
                        except asyncio.TimeoutError:
                            print("Timeout while waiting for user input.")
                            close_chrome = True

                        if close_chrome:
                            close_app("chrome.exe")

                        try:
                            shutdown = await asyncio.wait_for(show_chrome_dialog("Want to shut down the PC?", "End of stream"), timeout=30)
                        except asyncio.TimeoutError:
                            shutdown = False
                            print("Timeout: Not shutting down.")

                        if shutdown:
                            print("Shutting down...")
                            os.system("shutdown /s /t 10")
                        else:
                            print("Script ends.")
                        break
                except Exception as e:
                    print(f"Error while checking: {e}")

if __name__ == '__main__':
    asyncio.run(main())
from pypresence import Presence
from settings import DISCORD_CLIENT_ID, JELLYFIN_SERVER_URL, JELLYFIN_API_KEY, JELLYFIN_USER_ID
import requests
import shutil
import time


def update():
    r_sessions = requests.get(f'{JELLYFIN_SERVER_URL}/Sessions?ControllableByUserId={JELLYFIN_USER_ID}&api_key={JELLYFIN_API_KEY}')
    sessions = r_sessions.json()
    if sessions:
        if 'NowPlayingItem' in sessions[0]:
            playing = sessions[0]['NowPlayingItem']
            if playing['Type'] == 'Audio':
                t = (int) (sessions[0]['PlayState']['PositionTicks'] / 10000000)
                RPC.update(details=playing['Name'], state=playing['Artists'][0], large_image='audio',
                           start=((int) (time.time() - t)), large_text=f'{JELLYFIN_SERVER_URL}/Audio/{playing["Id"]}/stream.mp3')
            else:
                print(f'{playing["Type"]} support not yet implemented')
    else:
        print('No session found :shrug:')


RPC = Presence(DISCORD_CLIENT_ID)
RPC.connect()

while True:
    update()
    time.sleep(15)

import requests
from discord.ext.commands import Bot, Cog, Context, command
from discord.ext import tasks
import asyncio
from util import kos_data
import settings
import roblox


async def get_all_thumbnails() -> dict[str, str]:
    data = await kos_data.get_all_ids()
    print(data)

    thumbnails = {}
    for user_id in data:
        url = f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false'
        response = requests.get(url)
        if response.status_code != 200:
            continue
        thumbnails[response.json()["data"][0]["imageUrl"]] = user_id
        await asyncio.sleep(0.1)

    return thumbnails


class ScanServerListTask(Cog):
    bot: Bot
    robloxClient: roblox.Client

    def __init__(self, bot: Bot):
        self.bot = bot
        self.robloxClient = roblox.Client()

        self.scan_server_list_task.start()

    async def scan_server_list(self):
        print("Start scanning")

        # Get the channel to send my information
        channel = self.bot.get_channel(settings.BOT_CHANNEL)

        await channel.send('開始掃描服務器 (未必可靠)')

        # Get all the thumbnail of KOS player
        all_thumbnails = await get_all_thumbnails()

        cursor = None
        index = 0
        servers = []
        while 1:
            # Make the URL
            url = f"https://games.roblox.com/v1/games/{settings.OHIO_GAME_ID}/servers/Public?sortOrder=Desc&limit=100"
            if cursor:
                url += f"&cursor={cursor}"

            # Get 100 servers
            data = requests.get(url).json()

            # Loop though every server
            for server in data["data"]:
                server_data = []
                # Get all player token
                for player_token in server["playerTokens"]:
                    server_data.append({
                        "token": player_token,
                        "type": "AvatarHeadshot",
                        "size": "150x150",
                        "requestId": server["id"]
                    })

                # Get all thumbnail from player tokens
                thumbnail_response = requests.post(
                    "https://thumbnails.roblox.com/v1/batch",
                    json=server_data,
                    headers={"Content-Type": "application/json"})

                # Get the data of thumbnails
                thumbnail_data = thumbnail_response.json()["data"]

                if not thumbnail_data:
                    continue

                for thumbnail in thumbnail_data:
                    user_id = all_thumbnails.get(thumbnail["imageUrl"])
                    if user_id:
                        user = await self.robloxClient.get_user(int(user_id))
                        await channel.send(
                            f":warning: 發現KOS :warning:\n用戶名: {user.name}\n顯示名: {user.display_name}\n[頭像]({thumbnail['imageUrl']})\n服務器: {thumbnail['requestId']}")

            if not cursor:
                break

        await channel.send('掃描結束')

    @command('scan-server-list')
    async def scan_server_list_command(self, ctx: Context):
        await self.scan_server_list()

    @tasks.loop(minutes=10)
    async def scan_server_list_task(self):
        await self.scan_server_list()


async def setup(bot: Bot):
    cog = ScanServerListTask(bot)
    await bot.add_cog(cog)

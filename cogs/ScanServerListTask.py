from discord.ext.commands import Bot, Cog, Context, command
from discord.ext import tasks
import asyncio
from util import kos_data
import settings
import roblox
import aiohttp


async def get_all_thumbnails() -> dict[str, str]:
    data = await kos_data.get_all_ids()
    print(data)

    thumbnails = {}
    async with aiohttp.ClientSession() as session:
        for user_id in data:
            url = f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false'
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    thumbnails[data["data"][0]["imageUrl"]] = user_id

            # Wait for a while until next request
            await asyncio.sleep(0.5)
    return thumbnails


class ScanServerListTask(Cog):
    bot: Bot
    robloxClient: roblox.Client

    def __init__(self, bot: Bot):
        self.bot = bot
        self.robloxClient = roblox.Client()

    async def scan_server_list(self):
        # Get the channel to send my information
        channel = self.bot.get_channel(settings.BOT_CHANNEL)

        await channel.send(settings.LANGUAGE.START_SCANNING_SERVER_MSG)

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

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    # Get 100 servers
                    data = await response.json()

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
                    async with session.post(
                            "https://thumbnails.roblox.com/v1/batch",
                            json=server_data,
                            headers={"Content-Type": "application/json"}
                    ) as response:
                        # Get the data of thumbnails
                        data = await response.json()
                        thumbnail_data = data.get('data')

                    if not thumbnail_data:
                        continue

                    for thumbnail in thumbnail_data:
                        user_id = all_thumbnails.get(thumbnail["imageUrl"])
                        if user_id:
                            user = await self.robloxClient.get_user(int(user_id))
                            await channel.send(settings.LANGUAGE.FOUND_TARGET_MSG.format(
                                username=user.name,
                                display_name=user.display_name,
                                serverid=thumbnail['requestId'],
                                userid=user.id
                            ))

                if not cursor:
                    break

        await channel.send(settings.LANGUAGE.SCAN_FINISHED_MSG)

    @command('scan-server-list')
    async def scan_server_list_command(self, ctx: Context):
        await self.scan_server_list()

    @tasks.loop(minutes=10.0)
    async def scan_server_list_task(self):
        await self.scan_server_list()

    @Cog.listener()
    async def on_ready(self):
        await self.scan_server_list_task.start()


async def setup(bot: Bot):
    cog = ScanServerListTask(bot)
    await bot.add_cog(cog)

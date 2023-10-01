from discord.ext.commands import Bot, Cog, command, Context

import settings
from util import kos_data
import time
import pytimeparse2
import roblox


class AddKOSCommand(Cog):
    bot: Bot
    robloxClient: roblox.Client

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.robloxClient = roblox.Client()

    @command("add-kos")
    async def add_kos(self, ctx: Context, kos: str, expire: str = None, reason: str = settings.LANGUAGE.NO_REASON_PROVIDED, *args) -> None:
        if expire is not None:
            expire = time.time() + pytimeparse2.parse(expire)

        kos_user = await self.robloxClient.get_user_by_username(kos)
        kos_id = str(kos_user.id)
        response: str = await kos_data.add_kos(kos_id, ctx.author.id, reason, expire)
        await ctx.reply(response)


async def setup(bot: Bot) -> None:
    await bot.add_cog(AddKOSCommand(bot))

from discord.ext.commands import Bot, Cog, command, Context
from util import kos_data
import time
import pytimeparse2


class AddKOSCommand(Cog):
    bot: Bot

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @command("add-kos")
    async def add_kos(self, ctx: Context, kos: str, expire: str = None, reason: str = "沒有提供原因", *args) -> None:
        if expire is not None:
            expire = time.time() + pytimeparse2.parse(expire)

        response: str = await kos_data.add_kos(kos, ctx.author.id, reason, expire)

        await ctx.reply(response)


async def setup(bot: Bot) -> None:
    await bot.add_cog(AddKOSCommand(bot))

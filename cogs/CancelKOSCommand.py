from discord.ext.commands import Bot, Cog, command, Context
from util import kos_data
import roblox

class CancelKOSCommand(Cog):
    bot: Bot
    robloxClient: roblox.Client
    def __init__(self, bot):
        self.bot = bot
        self.robloxClient = roblox.Client()

    @command("cancel-kos")
    async def cancel_kos(self, ctx: Context, user: str):
        user_data = await self.robloxClient.get_user_by_username(user)
        user_id = str(user_data.id)
        response = await kos_data.cancel_kos(user_id)

        await ctx.reply(response)


async def setup(bot: Bot):
    await bot.add_cog(CancelKOSCommand(bot))

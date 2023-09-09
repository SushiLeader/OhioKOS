from discord.ext.commands import Bot, Cog, Context, command
from util import kos_data
import roblox


class ListKOSCommand(Cog):
    bot: Bot
    client: roblox.Client

    def __init__(self, bot: Bot):
        self.bot = bot
        self.client = roblox.Client()

    @command('list-kos')
    async def list_kos(self, ctx: Context):
        all_id = await kos_data.get_all_ids()
        print(all_id)

        usernames = ''
        for id in all_id:
            user = await self.client.get_user(id)
            usernames += f'{user.display_name} (@{user.name})\n'

        await ctx.reply(usernames)

async def setup(bot: Bot):
    await bot.add_cog(ListKOSCommand(bot))


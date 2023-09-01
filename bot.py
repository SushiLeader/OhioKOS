from discord.ext import commands
import discord
import os
import settings
import asyncio


bot: commands.Bot = commands.Bot(command_prefix=":", intents=discord.Intents.all())


# Loads all the extension
async def load_all_extension():
    cogs: list[str] = os.listdir("cogs")
    cogs = list(filter(lambda filename: filename.endswith('.py'), cogs))

    for cog in cogs:
        await bot.load_extension(f'cogs.{cog.split(".")[0]}')


# Runs the load_all_extension() function
asyncio.get_event_loop().run_until_complete(load_all_extension())


bot.run(settings.BOT_TOKEN)

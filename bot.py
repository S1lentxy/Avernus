import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.getenv('TOKEN') # Railway te lo pasa solo

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} CONECTADO 24/7')

async def main():
    async with bot:
        await bot.load_extension("cogs.moderation") 
        await bot.start(TOKEN)

asyncio.run(main())
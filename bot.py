import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} CONECTADO')

async def main():
    async with bot:
        await bot.load_extension("cogs.moderation") # <- Acá carga tu HTML
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} CONECTADO 24/7')
    # Sync instantáneo para tu servidor Avernus
    await bot.tree.sync(guild=discord.Object(id=1522055657589833779))
    print("Slash commands sincronizados")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Cargado: {filename}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if _name_ == "_main_":
    asyncio.run(main())

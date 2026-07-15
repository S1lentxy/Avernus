import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} CONECTADO 24/7")
    
    # Sincronizar comandos (esto es importante)
    try:
        # Sincronización global (puede tardar hasta 1 hora)
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comandos sincronizados globalmente")
    except Exception as e:
        print(f"❌ Error global: {e}")
    
    try:
        # Sincronización rápida en tu servidor (recomendado)
        guild = discord.Object(id=1522055657589833779)  # Cambia si es otro servidor
        await bot.tree.sync(guild=guild)
        print("✅ Comandos sincronizados en el servidor")
    except Exception as e:
        print(f"❌ Error en guild sync: {e}")

async def load_cogs():
    print("📂 Cargando extensiones...")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cargado: {filename}")
            except Exception as e:
                print(f"❌ Error al cargar {filename}: {e}")

@bot.event
async def setup_hook():
    await load_cogs()

bot.run(TOKEN)

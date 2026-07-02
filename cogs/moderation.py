import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio

class Moderation(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @app_commands.command(name="meteorite", description="Banea a todos los que entraron en los ultimos X minutos")
    @app_commands.describe(minutes="Minutos hacia atras. Ej: 5")
    @app_commands.default_permissions(ban_members=True)
    async def meteorite(self, interaction: discord.Interaction, minutes: int = 5):
        await interaction.response.defer(thinking=True, ephemeral=True)
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        members_to_ban = [m for m in interaction.guild.members if m.joined_at > cutoff and not m.bot]
        if not members_to_ban:
            return await interaction.followup.send("No hay miembros nuevos.")
        count = 0
        for member in members_to_ban:
            try:
                await member.ban(reason=f"Meteorite")
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await interaction.followup.send(f"⭐ {count} baneados.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
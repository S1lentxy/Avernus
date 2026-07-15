import discord
from discord.ext import commands
from discord import app_commands, ui
from db import get_db

class StaffView(ui.View):
    def __init__(self, msg_id: int, type: str):
        super().__init__(timeout=None)
        self.msg_id = msg_id
        self.type = type

    async def check_staff(self, interaction: discord.Interaction) -> bool:
        db = get_db()
        role_id = db.execute("SELECT staff_role_id FROM suggest_report_config WHERE guild_id = ?", 
                            (str(interaction.guild.id),)).fetchone()
        if not role_id or interaction.guild.get_role(int(role_id['staff_role_id'])) not in interaction.user.roles:
            await interaction.response.send_message("❌ No sos staff.", ephemeral=True)
            return False
        return True

    @ui.button(label="✅ Aceptar", style=discord.ButtonStyle.green, custom_id="sr_accept")
    async def accept(self, interaction: discord.Interaction, button: ui.Button):
        if not await self.check_staff(interaction): return
        embed = interaction.message.embeds[0]
        embed.color = 0x57F287
        embed.set_footer(text=f"Aceptado por {interaction.user.display_name}")
        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("✅ Aceptado.", ephemeral=True)

    @ui.button(label="❌ Denegar", style=discord.ButtonStyle.red, custom_id="sr_deny")
    async def deny(self, interaction: discord.Interaction, button: ui.Button):
        if not await self.check_staff(interaction): return
        embed = interaction.message.embeds[0]
        embed.color = 0xED4245
        embed.set_footer(text=f"Denegado por {interaction.user.display_name}")
        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message("❌ Denegado.", ephemeral=True)

class SuggestReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggest_setup", description="Setear canales de sugerencias/reportes")
    @app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, suggest_channel: discord.TextChannel, report_channel: discord.TextChannel, staff_role: discord.Role):
        db = get_db()
        db.execute("INSERT OR REPLACE INTO suggest_report_config (guild_id, suggest_channel_id, report_channel_id, staff_role_id) VALUES (?, ?, ?, ?)",
                   (str(interaction.guild.id), str(suggest_channel.id), str(report_channel.id), str(staff_role.id)))
        db.commit()
        await interaction.response.send_message(f"✅ Seteado. Sugerencias: {suggest_channel.mention} | Reportes: {report_channel.mention}", ephemeral=True)

    @app_commands.command(name="suggest", description="Enviar una sugerencia")
    async def suggest(self, interaction: discord.Interaction, *, text: str):
        db = get_db()
        channel_id = db.execute("SELECT suggest_channel_id FROM suggest_report_config WHERE guild_id = ?", 
                               (str(interaction.guild.id),)).fetchone()
        if not channel_id:
            return await interaction.response.send_message("❌ No hay canal seteado.", ephemeral=True)

        channel = interaction.guild.get_channel(int(channel_id['suggest_channel_id']))
        embed = discord.Embed(title="💡 NUEVA SUGERENCIA", description=text, color=0x5865F2)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        msg = await channel.send(embed=embed, view=StaffView(msg.id, "suggest"))
        await interaction.response.send_message(f"✅ Sugerencia enviada en {channel.mention}", ephemeral=True)

    @app_commands.command(name="report", description="Reportar un usuario")
    async def report(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        db = get_db()
        channel_id = db.execute("SELECT report_channel_id FROM suggest_report_config WHERE guild_id = ?", 
                               (str(interaction.guild.id),)).fetchone()
        if not channel_id:
            return await interaction.response.send_message("❌ No hay canal seteado.", ephemeral=True)

        channel = interaction.guild.get_channel(int(channel_id['report_channel_id']))
        embed = discord.Embed(title="❌ NUEVO REPORTE", color=0xFF0000)
        embed.add_field(name="Reportado", value=user.mention)
        embed.add_field(name="Por", value=interaction.user.mention)
        embed.add_field(name="Razón", value=reason, inline=False)
        msg = await channel.send(embed=embed, view=StaffView(msg.id, "report"))
        await interaction.response.send_message(f"✅ Reporte enviado a staff.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SuggestReport(bot))
    print("✅ Cog SuggestReport cargado correctamente")

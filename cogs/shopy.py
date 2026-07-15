import discord
from discord.ext import commands
from discord import app_commands
from db import get_db

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    shop_group = app_commands.Group(name="shop", description="Tienda V9.3")

    @shop_group.command(name="add", description="Agregar item a la tienda. Solo Admin")
    @app_commands.default_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, name: str, price: int, role: discord.Role):
        db = get_db()
        db.execute("INSERT INTO shop_items (guild_id, name, price, role_id) VALUES (?, ?, ?, ?)",
                   (str(interaction.guild.id), name, price, str(role.id)))
        db.commit()
        await interaction.response.send_message(f"✅ Item **{name}** por **{price}** coins agregado. Da rol {role.name}", ephemeral=True)

    @shop_group.command(name="list", description="Ver la tienda")
    async def list(self, interaction: discord.Interaction):
        db = get_db()
        rows = db.execute("SELECT id, name, price FROM shop_items WHERE guild_id=?", 
                         (str(interaction.guild.id),)).fetchall()
        
        if not rows:
            return await interaction.response.send_message("🛒 La tienda está vacía.", ephemeral=True)

        embed = discord.Embed(title="🛒 TIENDA AVERNUS", color=0xFFEE75C)
        for row in rows:
            embed.add_field(name=f"ID: {row['id']} | {row['name']}", 
                           value=f"Precio: **{row['price']}** coins", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @shop_group.command(name="buy", description="Comprar un item por ID")
    async def buy(self, interaction: discord.Interaction, item_id: int):
        db = get_db()
        item = db.execute("SELECT * FROM shop_items WHERE id = ? AND guild_id=?", 
                         (item_id, str(interaction.guild.id))).fetchone()

        if not item:
            return await interaction.response.send_message("❌ Item no existe.", ephemeral=True)

        user_row = db.execute("SELECT coins FROM economy WHERE guild_id = ? AND user_id = ?", 
                             (str(interaction.guild.id), str(interaction.user.id))).fetchone()

        if not user_row or user_row['coins'] < item['price']:
            return await interaction.response.send_message("❌ No tenés coins suficientes.", ephemeral=True)

        inv = db.execute("SELECT * FROM inventory WHERE guild_id = ? AND user_id = ? AND item_id = ?", 
                        (str(interaction.guild.id), str(interaction.user.id), item_id)).fetchone()

        if inv:
            return await interaction.response.send_message("❌ Ya compraste ese item.", ephemeral=True)

        role = interaction.guild.get_role(int(item['role_id']))
        if role:
            await interaction.user.add_roles(role, reason="Compra Tienda V9.3")

        db.execute("UPDATE economy SET coins = coins - ? WHERE guild_id = ? AND user_id = ?", 
                  (item['price'], str(interaction.guild.id), str(interaction.user.id)))

        db.execute("INSERT INTO inventory (guild_id, user_id, item_id) VALUES (?, ?, ?)", 
                  (str(interaction.guild.id), str(interaction.user.id), item_id))

        db.commit()
        await interaction.response.send_message(f"✅ Compraste **{item['name']}** por **{item['price']}** coins. Rol dado!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("✅ Cog Shop cargado correctamente")

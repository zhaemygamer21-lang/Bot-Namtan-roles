import os, time, requests, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer
import discord
from discord.ext import commands

TOKEN = os.environ.get("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot de Bautizo Jochis Activo")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("0.0.0.0", port), Servidor).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

class MenuPaises(discord.ui.Select):
    def __init__(self):
        opciones = [
            discord.SelectOption(label="México", emoji="🇲🇽", description="Rol para las jochis de México"),
            discord.SelectOption(label="Colombia", emoji="🇨🇴", description="Rol para las jochis de Colombia"),
            discord.SelectOption(label="Venezuela", emoji="🇻🇪", description="Rol para las jochis de Venezuela"),
            discord.SelectOption(label="Argentina", emoji="🇦🇷", description="Rol para las jochis de Argentina"),
            discord.SelectOption(label="Chile", emoji="🇨🇱", description="Rol para las jochis de Chile"),
            discord.SelectOption(label="Perú", emoji="🇵🇪", description="Rol para las jochis de Perú"),
            discord.SelectOption(label="Ecuador", emoji="🇪🇨", description="Rol para las jochis de Ecuador"),
            discord.SelectOption(label="España", emoji="🇪🇸", description="Rol para las jochis de España"),
            discord.SelectOption(label="Estados Unidos", emoji="🇺🇸", description="Rol para las jochis de USA"),
            discord.SelectOption(label="República Dominicana", emoji="🇩🇴", description="Rol para las jochis de RD"),
            discord.SelectOption(label="Puerto Rico", emoji="🇵🇷", description="Rol para las jochis de Puerto Rico"),
            discord.SelectOption(label="Guatemala", emoji="🇬🇹", description="Rol para las jochis de Guatemala"),
            discord.SelectOption(label="Costa Rica", emoji="🇨🇷", description="Rol para las jochis de Costa Rica"),
            discord.SelectOption(label="Panamá", emoji="🇵🇦", description="Rol para las jochis de Panamá"),
            discord.SelectOption(label="Honduras", emoji="🇭🇳", description="Rol para las jochis de Honduras"),
            discord.SelectOption(label="El Salvador", emoji="🇸🇻", description="Rol para las jochis de El Salvador"),
            discord.SelectOption(label="Bolivia", emoji="🇧🇴", description="Rol para las jochis de Bolivia"),
            discord.SelectOption(label="Uruguay", emoji="🇺🇾", description="Rol para las jochis de Uruguay"),
        ]
        super().__init__(placeholder="👉 Elige tu bandera aquí...", min_values=1, max_values=1, options=opciones, custom_id="menu_jochis_paises")

    async def callback(self, interaction: discord.Interaction):
        nombre_rol = self.values[0]
        rol = discord.utils.get(interaction.guild.roles, name=nombre_rol)
        
        if rol is None:
            await interaction.response.send_message(f"❌ Error técnico: El rol llamado '{nombre_rol}' no existe en los ajustes de Discord. ¡Créalo para que pueda asignarlo!", ephemeral=True)
            return

        if rol in interaction.user.roles:
            await interaction.user.remove_roles(rol)
            await interaction.response.send_message(f"🗑️ Te he quitado el rol de **{nombre_rol}**.", ephemeral=True)
        else:
            await interaction.user.add_roles(rol)
            await interaction.response.send_message(f"✨ ¡Bautizada con éxito! Ahora tienes tu rol de **{nombre_rol}**.", ephemeral=True)

class VistaJochis(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MenuPaises())

@bot.event
async def on_ready():
    print(f"Bot de Bautizo conectado como {bot.user}")
    bot.add_view(VistaJochis())

@bot.command()
@commands.has_permissions(administrator=True)
async def enviar_bautizo(ctx):
    await ctx.message.delete()
    
    embed = discord.Embed(
        title="👑 ¡EL ALTAR DE LAS JOCHIS PROMEDIO! 👑",
        description="✨ **¡Otra jochis más!** ✨\n\n"
                    "📍 Indica tu país abajo en el menú desplegable, toma este rol y **sé oficialmente bautizada por mí como una jochis promedio**.\n\n"
                    "¡Presiona el menú de abajo, busca tu bandera y reclama tu corona! 💅👑",
        color=15418782
    )
    embed.set_footer(text="Ceremonia Oficial de Bautizo Jochis • Sistema Automatizado")
    
    await ctx.send(embed=embed, view=VistaJochis())

bot.run(TOKEN)

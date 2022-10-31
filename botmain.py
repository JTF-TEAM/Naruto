#!/usr/bin/env python3
import os
import nextcord
from nextcord.ext import  commands
from dotenv import token, mongo #(dotenv.py -> token:str, mongo:str)

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

load_symbol = '▮'
load_progress = 1
print(load_symbol*load_progress, end='\r'); load_progress+=1
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(load_symbol*load_progress, end='\r');load_progress+=1


####################### geting cock ##################################
# dev guilds for cogs management
guilds = [786255515570667541] # <- jtf

@bot.event
async def on_ready():
    print(f"{load_symbol*(load_progress+1)} Logged in as {bot.user}")
    await bot.change_presence(activity=nextcord.Activity(name=f'-', type=nextcord.ActivityType.listening))


######################################################################
# default cogs commands

@bot.slash_command(guild_ids=guilds)
async def load(interaction: nextcord.Interaction, модуль: str):
    bot.load_extension(f"cogs.{модуль}")
    await interaction.send(f'✅ Загружен модуль {модуль}', ephemeral=True)

@bot.slash_command(guild_ids=guilds)
async def reload(interaction: nextcord.Interaction, модуль: str):
    bot.reload_extension(f"cogs.{модуль}")
    await interaction.send(f'✅ Рестарт модуль {модуль} перезагружен', ephemeral=True)

@bot.slash_command(guild_ids=guilds)
async def unload(interaction: nextcord.Interaction, модуль: str):
    bot.unload_extension(f"cogs.{модуль}")
    await interaction.send(f'✅ Модуль **{модуль}** выгружен', ephemeral=True)

print(load_symbol*load_progress, end='\r')
bot.run(token)
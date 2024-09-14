import nextcord
import os
import json

from nextcord.ext import commands
from checkTierRL import CheckTierRL

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
bot.add_cog(CheckTierRL(bot, [1221242050305855509])) 

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print('_____________________________________')      

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    bot.run(config["token"])

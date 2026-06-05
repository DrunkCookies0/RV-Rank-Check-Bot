import nextcord
import os

from nextcord.ext import commands
from checkTierRL import CheckTier

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
bot.add_cog(CheckTier(bot))

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print('_____________________________________')      

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])

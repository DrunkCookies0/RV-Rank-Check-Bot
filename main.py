import nextcord
import os

from nextcord.ext import commands
from nextcord import SlashOption

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.slash_command()
async def checktier(
    ctx,
    game: str = SlashOption(
        name="game",
        description="Name of the game (only 'Rocket League' is supported)",
        choices=["Rocket League"]
    ),
    format: str = SlashOption(
        name="format",
        description="Choose the format (1v1, 2v2, 3v3)",
        choices=["1v1", "2v2", "3v3"]
    ),
    peak3s: int = SlashOption(
        name="peak3s",
        description="Peak MMR for 3v3",
        default=0,
        min_value=0,
        max_value=1999
    ),
    peak2s: int = SlashOption(
        name="peak2s",
        description="Peak MMR for 2v2",
        default=0,
        min_value=0,
        max_value=1999
    ),
    peak1s: int = SlashOption(
        name="peak1s",
        description="Peak MMR for 1v1",
        default=0,
        min_value=0,
        max_value=1999
    )
):
    if game.lower() == "rocket league":
        if format == "3v3":
            league_rank = calculate_custom_league_rank(peak3s, peak2s)
        elif format == "2v2":
            league_rank = calculate_custom_league_rank(peak2s, peak3s)
        elif format == "1v1":
            league_rank = calculate_league_rank_1v1(peak3s, peak2s, peak1s)
        else:
            await ctx.send("Invalid format selected.")
            return
        
        tier = determine_tier(format, league_rank)
        result = f"{format} League Rank: {league_rank:.0f} ({tier})"
    else:
        result = f"Game {game} not supported yet."
    
    await ctx.send(result)

def calculate_custom_league_rank(peak1, peak2):
    league_rank = max(peak1, peak2 - 120) * 0.75 + max(peak2, peak1 - 120) * 0.25
    return league_rank

def calculate_league_rank_1v1(peak3s, peak2s, peak1s):
    league_rank_1v1 = (0.2 * peak3s) + (0.25 * peak2s) + (0.8 * peak1s)
    return league_rank_1v1

def determine_tier(format, league_rank):
    # Define tier ranges for each format
    tiers = {
        "3v3": [
            (1800, 9999, "Tier 1"),
            (1650, 1799, "Tier 2"),
            (1500, 1649, "Tier 3"),
            (1350, 1499, "Tier 4"),
            (1200, 1349, "Tier 5"),
            (1050, 1199, "Tier 6"),
            (900, 1049, "Tier 7"),
            (0, 899, "Tier 8"),
        ],
        "2v2": [
            (1800, 9999, "Tier 1"),
            (1650, 1799, "Tier 2"),
            (1500, 1649, "Tier 3"),
            (1350, 1499, "Tier 4"),
            (1200, 1349, "Tier 5"),
            (1050, 1199, "Tier 6"),
            (900, 1049, "Tier 7"),
            (0, 899, "Tier 8"),
        ],
        "1v1": [
            (1800, 9999, "Tier 1"),
            (1650, 1799, "Tier 2"),
            (1500, 1649, "Tier 3"),
            (1350, 1499, "Tier 4"),
            (1200, 1349, "Tier 5"),
            (1050, 1199, "Tier 6"),
            (900, 1049, "Tier 7"),
            (750, 899, "Tier 8"),
            (0, 749, "Tier 9"),
        ],
        "Crew Battles": [
            (1800, 9999, "Tier 1"),
            (1650, 1799, "Tier 2"),
            (1500, 1649, "Tier 3"),
            (1350, 1499, "Tier 4"),
            (1200, 1349, "Tier 5"),
            (1050, 1199, "Tier 6"),
            (900, 1049, "Tier 7"),
            (750, 899, "Tier 8"),
            (0, 749, "Tier 9"),
        ]
    }

    for min_rank, max_rank, tier_name in tiers[format]:
        if min_rank <= league_rank <= max_rank:
            return tier_name
    
    return "Unknown Tier"

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name} ({bot.user.id})')
    print('_____________________________________')





bot.run('MTI4MzIyOTYzMTcyOTg5NzUyMw.GyVkV-.qmbgdGbxBEuiWGVBQ0PJ5OvzS69uCVFJNW8W_k')

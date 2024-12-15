import nextcord
import os

from nextcord.ext import commands
from nextcord import SlashOption

testGuilds = None

class CheckTier(commands.Cog):

    def __init__(self, bot, guilds = None):
        self.bot = bot
        global testGuilds
        testGuilds = guilds


    @nextcord.slash_command(guild_ids=testGuilds)
    async def checktier(self):
        pass

    @checktier.subcommand(description="Check your Rocket League tier")
    async def rocket_league(
        self,
        ctx,
        #game: str = SlashOption(
        #    name="game",
        #    description="Name of the game (only 'Rocket League' is supported)",
        #    required=True,
        #    choices=["Rocket League"]
        #),
        format: str = SlashOption(
            name="format",
            description="Choose the format (1v1, 2v2, 3v3 or All formats)",
            required=True,
            choices=["1v1", "2v2", "3v3", "All"]
        ),
        peak3s: int = SlashOption(
            name="peak3s",
            description="Peak MMR for 3v3",
            required=True,
            default=0,
            min_value=0,
            max_value=2500
        ),
        peak2s: int = SlashOption(
            name="peak2s",
            description="Peak MMR for 2v2",
            required=True,
            default=0,
            min_value=0,
            max_value=2500
        ),
        peak1s: int = SlashOption(
            name="peak1s",
            description="Peak MMR for 1v1",
            default=None,
            min_value=0,
            max_value=2500
        )
    ):
        if format == "3v3":
            league_rank = self.calculate_custom_league_rank(peak3s, peak2s)
            tier = self.determine_tier(format, league_rank)
            result = f"Based on the following information:\n\t" \
                    f"3v3: {peak3s}\n\t2v2: {peak2s}\n"\
                    f"Your unofficial league rank would be:\n\t" \
                    f"{format}: {league_rank:.0f} ({tier})"
        elif format == "2v2":
            league_rank = self.calculate_custom_league_rank(peak2s, peak3s)
            tier = self.determine_tier(format, league_rank)
            result = f"Based on the following information:\n\t" \
                    f"3v3: {peak3s}\n\t2v2: {peak2s}\n"\
                    f"Your unofficial league rank would be:\n\t" \
                    f"{format}: {league_rank:.0f} ({tier})"
        elif format == "1v1":
            if peak1s is None:
                await ctx.send("Peak MMR for 1v1 is required.", ephemeral=True)
                return
            else:
                league_rank = self.calculate_league_rank_1v1(peak3s, peak2s, peak1s)
                tier = self.determine_tier(format, league_rank)
                result = f"Based on the following information:\n\t" \
                    f"3v3: {peak3s}\n\t2v2: {peak2s}\n\t1v1: {peak1s}\n"\
                    f"Your unofficial league rank would be:\n\t" \
                    f"{format}: {league_rank:.0f} ({tier})"
        elif format == "All":
            if peak1s is None:
                await ctx.send("Peak MMR for 1v1 is required.", ephemeral=True)
                return
            else:
                league_rank_1v1 = self.calculate_league_rank_1v1(peak3s, peak2s, peak1s)
                tier_1v1 = self.determine_tier("1v1", league_rank_1v1)
                league_rank_2v2 = self.calculate_custom_league_rank(peak2s, peak3s)
                tier_2v2 = self.determine_tier("2v2", league_rank_2v2)
                league_rank_3v3 = self.calculate_custom_league_rank(peak3s, peak2s)
                tier_3v3 = self.determine_tier("3v3", league_rank_3v3)
                result = f"Given the following peaks:\n\t" \
                    f"3v3: {peak3s}\n\t2v2: {peak2s}\n\t1v1: {peak1s}\n"\
                    f"Your league ranks are:\n\t" \
                    f"3v3: {league_rank_3v3:.0f} ({tier_3v3})\n\t2v2: {league_rank_2v2:.0f} ({tier_2v2})\n\t1v1: {league_rank_1v1:.0f} ({tier_1v1})"

        else:
            await ctx.send("Invalid format selected.")
            return
        
        await ctx.send(result)

    def calculate_custom_league_rank(self, peak1, peak2):
        league_rank = max(peak1, peak2 - 120) * 0.75 + max(peak2, peak1 - 120) * 0.25
        return league_rank

    def calculate_league_rank_1v1(self, peak3s, peak2s, peak1s):
        league_rank_1v1 = (0.2 * max(peak3s, peak2s - 120)) + (0.25 * max(peak2s, peak3s - 120)) + (0.8 * peak1s)
        return league_rank_1v1

    def determine_tier(self, format, league_rank):
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
                (400, 899, "Tier 8"),
            ],
            "2v2": [
                (1800, 9999, "Tier 1"),
                (1650, 1799, "Tier 2"),
                (1500, 1649, "Tier 3"),
                (1350, 1499, "Tier 4"),
                (1200, 1349, "Tier 5"),
                (1050, 1199, "Tier 6"),
                (900, 1049, "Tier 7"),
                (400, 899, "Tier 8"),
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
                (400, 749, "Tier 9"),
            ]
        }

        for min_rank, max_rank, tier_name in tiers[format]:
            if min_rank <= league_rank <= max_rank:
                return tier_name
        
        return "Invalid Tier"

import nextcord

from nextcord.ext import commands


testGuilds = None
MIN_VALID_MMR = 300
MAX_VALID_MMR = 2500
RANK_PANEL_BUTTON_ID = "rank_check:open_modal"
PANEL_HISTORY_SCAN_LIMIT = 200


class RankInputModal(nextcord.ui.Modal):

    def __init__(self, cog):
        super().__init__("Check Your Rank Tier")
        self.cog = cog

        self.peak3s = nextcord.ui.TextInput(
            label="Peak 3v3 MMR",
            placeholder="Enter a number between 300 and 2500",
            min_length=1,
            max_length=4,
            required=True,
        )
        self.peak2s = nextcord.ui.TextInput(
            label="Peak 2v2 MMR",
            placeholder="Enter a number between 300 and 2500",
            min_length=1,
            max_length=4,
            required=True,
        )

        self.add_item(self.peak3s)
        self.add_item(self.peak2s)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            peak3s = int(self.peak3s.value.strip())
            peak2s = int(self.peak2s.value.strip())
        except ValueError:
            await interaction.response.send_message("Invalid input: please enter numbers for both MMR fields.", ephemeral=True)
            return

        is_valid, error_message = self.cog.validate_peak_inputs(peak3s, peak2s)
        if not is_valid:
            await interaction.response.send_message(error_message, ephemeral=True)
            return

        await interaction.response.send_message(self.cog.build_result_message(peak3s, peak2s))


class RankPanelView(nextcord.ui.View):

    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @nextcord.ui.button(
        label="Click here to check your rank tier",
        style=nextcord.ButtonStyle.primary,
        custom_id=RANK_PANEL_BUTTON_ID,
    )
    async def check_rank_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RankInputModal(self.cog))


class CheckTier(commands.Cog):

    def __init__(self, bot, guilds=None):
        self.bot = bot
        global testGuilds
        testGuilds = guilds
        self.panel_view = None

    def ensure_panel_view(self):
        if self.panel_view is None:
            self.panel_view = RankPanelView(self)
            self.bot.add_view(self.panel_view)

    def cog_unload(self):
        if self.panel_view is not None:
            self.panel_view.stop()

    @commands.Cog.listener()
    async def on_ready(self):
        self.ensure_panel_view()

    @nextcord.slash_command(
        guild_ids=testGuilds,
        description="Admin only: post the rank-check button panel in this channel",
        default_member_permissions=nextcord.Permissions(administrator=True),
    )
    async def setup(self, ctx):
        self.ensure_panel_view()

        if ctx.guild is None:
            await ctx.send("This command can only be used in a server channel.", ephemeral=True)
            return

        if not ctx.user.guild_permissions.administrator:
            await ctx.send("Only server admins can use this command.", ephemeral=True)
            return

        if await self.channel_has_rank_panel(ctx.channel):
            await ctx.send("A rank check panel already exists in this channel.", ephemeral=True)
            return

        panel_message = (
            "**RV Rank Check**\n"
            "Click the button below to open the rank checker form."
        )
        try:
            await ctx.channel.send(panel_message, view=self.panel_view)
        except (nextcord.Forbidden, nextcord.HTTPException):
            await ctx.send(
                "I couldn't post the rank check panel in this channel. Please ensure I have permission to Send Messages.",
                ephemeral=True,
            )
            return

        await ctx.send("Rank check panel posted in this channel.", ephemeral=True)

    async def channel_has_rank_panel(self, channel):
        try:
            async for message in channel.history(limit=PANEL_HISTORY_SCAN_LIMIT):
                if message.author.id != self.bot.user.id:
                    continue

                for action_row in message.components:
                    for component in action_row.children:
                        if getattr(component, "custom_id", None) == RANK_PANEL_BUTTON_ID:
                            return True
        except (nextcord.Forbidden, nextcord.HTTPException):
            return False

        return False

    def validate_peak_inputs(self, peak3s, peak2s):
        peaks_by_field = {
            "3v3": peak3s,
            "2v2": peak2s,
        }
        for field_name, peak in peaks_by_field.items():
            if peak < MIN_VALID_MMR or peak > MAX_VALID_MMR:
                return False, (
                    f"Error: {field_name} value must be between "
                    f"{MIN_VALID_MMR} and {MAX_VALID_MMR}."
                )

        return True, None

    def build_result_message(self, peak3s, peak2s):
        league_rank_2v2 = self.calculate_custom_league_rank(peak2s, peak3s)
        tier_2v2 = self.determine_tier("2v2", round(league_rank_2v2))
        league_rank_3v3 = self.calculate_custom_league_rank(peak3s, peak2s)
        tier_3v3 = self.determine_tier("3v3", round(league_rank_3v3))

        result = (
            f"Given the following peaks:\n\t"
            f"3v3: {peak3s}\n\t2v2: {peak2s}\n"
            f"Your unofficial league ranks are:\n\t"
            f"3v3: {league_rank_3v3} ({tier_3v3})\n\t2v2: {league_rank_2v2} ({tier_2v2})"
        )

        return result

    def calculate_custom_league_rank(self, peak1, peak2):
        league_rank = max(peak1, peak2 - 120) * 0.75 + max(peak2, peak1 - 120) * 0.25
        return round(league_rank)

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
                (300, 1049, "Tier 7"),
            ],
            "2v2": [
                (1800, 9999, "Tier 1"),
                (1650, 1799, "Tier 2"),
                (1500, 1649, "Tier 3"),
                (1350, 1499, "Tier 4"),
                (1200, 1349, "Tier 5"),
                (1050, 1199, "Tier 6"),
                (300, 1049, "Tier 7"),
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

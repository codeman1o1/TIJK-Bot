import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.ext import commands
from nextcord.application_command import SlashOption

from main import SLASH_GUILDS


class fun_slash(commands.Cog, name="Fun Slash", description="Fun slash commands"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(description="Flips a coin", guild_ids=SLASH_GUILDS)
    async def headsortails(self, interaction: Interaction):
        hot = random.randint(0, 1)
        if hot == 0:
            hot = "heads"
        if hot == 1:
            hot = "tails"
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(fun_slash(bot))

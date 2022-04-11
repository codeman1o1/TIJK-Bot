import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.ext import commands

from views.buttons.github import github_button

from main import SLASH_GUILDS


class general_slash(
    commands.Cog,
    name="General Slash",
    description="Slash commands that everyone can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(
        description="Sends a link to the official TIJK Bot GitHub page",
        guild_ids=SLASH_GUILDS,
    )
    async def github(self, interaction: Interaction):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="View the official TIJK Bot code now!",
            value="https://github.com/codeman1o1/TIJK-Bot",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, view=github_button())


def setup(bot: commands.Bot):
    bot.add_cog(general_slash(bot))

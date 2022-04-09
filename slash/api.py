import aiohttp
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
from main import SLASH_GUILDS


class api_slash(
    commands.Cog, name="API Slash commands", description="API slash commands"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    async def api(self, interaction: Interaction):
        """This will never get called since it has slash commands"""
        pass

    @api.subcommand(
        name="animal",
        description="Uses an animal API to get information",
        inherit_hooks=True,
    )
    async def animal_api(
        self,
        interaction: Interaction,
        animal=SlashOption(
            choices={
                "dog": "dog",
                "cat": "cat",
                "panda": "panda",
                "red panda": "red_panda",
                "bird": "bird",
                "fox": "fox",
                "koala": "koala",
            },
            description="The animal",
            required=True,
        ),
    ):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f"https://some-random-api.ml/img/{animal}")
            info = await request.json()
        await interaction.response.send_message(info["link"])


def setup(bot: commands.Bot):
    bot.add_cog(api_slash(bot))

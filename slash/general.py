import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.ext import commands
import requests
from mojang import MojangAPI

from views.buttons.github import github_button

from main import HYPIXEL_API_KEY, SLASH_GUILDS, USER_DATA


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

    @slash(description="Chooses a random player who can own the party", guild_ids=SLASH_GUILDS)
    async def hypixelparty(self, interaction: Interaction):
        hypixel_ping = nextcord.utils.get(interaction.guild.roles, name="Hypixel Ping")
        available = [
            user
            for user in interaction.channel.members
            if not user.bot
            if user.status != nextcord.Status.offline
            if hypixel_ping in user.roles
        ]
        if available:
            for user in available:
                user2 = await commands.converter.UserConverter().convert(
                    interaction, str(user)
                )
                query = {"_id": user2.id}
                if USER_DATA.count_documents(query) != 0:
                    user3 = USER_DATA.find_one(query)
                    if "minecraft_account" in user3:
                        username = user3["minecraft_account"]
                        uuid = MojangAPI.get_uuid(username)
                        data = requests.get(
                            f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
                        ).json()
                        logouttime = data["player"]["lastLogout"]
                        logintime = data["player"]["lastLogin"]
                        if logouttime >= logintime or data["success"] is False:
                            available.remove(user)
                    else:
                        available.remove(user)
                else:
                    available.remove(user)
        if available:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Party leader chosen!",
                value=f"{random.choice(available)} will be the party leader!",
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title="Nobody meets the requirements to be the party leader!",
            )
        await interaction.response.send_message(embed=embed, delete_after=300)
        del available


def setup(bot: commands.Bot):
    bot.add_cog(general_slash(bot))

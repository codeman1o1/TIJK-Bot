import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
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

    @slash(
        description="Chooses a random player who can own the party",
        guild_ids=SLASH_GUILDS,
    )
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

    @slash(description="Link your Minecraft account", guild_ids=SLASH_GUILDS)
    async def link(
        self,
        interaction: Interaction,
        username: str = SlashOption(description="Your username", required=False),
    ):
        if username:
            if username.lower() == "remove":
                query = {"_id": interaction.user.id}
                if USER_DATA.count_documents(query) == 0:
                    embed = nextcord.Embed(
                        color=0xFFC800,
                        title="You don't have your Minecraft account linked!",
                    )
                else:
                    user = USER_DATA.find_one(query)
                    if "minecraft_account" in user:
                        account = user["minecraft_account"]
                        USER_DATA.update_one(
                            {"_id": interaction.user.id},
                            {"$unset": {"minecraft_account": account}},
                        )
                    else:
                        embed = nextcord.Embed(
                            color=0xFFC800,
                            title="You don't have your Minecraft account linked!",
                        )
                embed = nextcord.Embed(
                    color=0x0DD91A, title="Successfully removed your Minecraft account"
                )
            else:
                uuid = MojangAPI.get_uuid(username)
                data = requests.get(
                    f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
                ).json()
                if data["success"] is True:
                    try:
                        if "DISCORD" in data["player"]["socialMedia"]["links"].keys():
                            if (
                                data["player"]["socialMedia"]["links"]["DISCORD"]
                                == f"{interaction.user}"
                            ):
                                query = {"_id": interaction.user.id}
                                if USER_DATA.count_documents(query) == 0:
                                    post = {
                                        "_id": interaction.user.id,
                                        "minecraft_account": username,
                                    }
                                    USER_DATA.insert_one(post)
                                else:
                                    USER_DATA.update_one(
                                        {"_id": interaction.user.id},
                                        {"$set": {"minecraft_account": username}},
                                    )
                                embed = nextcord.Embed(
                                    color=0x0DD91A,
                                    title=f"Linked your account to **{username}**!",
                                )
                            else:
                                embed = nextcord.Embed(
                                    color=0xFFC800,
                                    title="The user's Discord is not linked to this account!",
                                )
                        else:
                            embed = nextcord.Embed(
                                color=0xFFC800,
                                title="Make sure to link your Discord account in Hypixel by using `/discord` in-game!",
                            )
                    except KeyError:
                        embed = nextcord.Embed(
                            color=0xFFC800,
                            title="This account has no Social Media linked!",
                        )
                else:
                    cause = data["cause"]
                    embed = nextcord.Embed(color=0xFF0000)
                    embed.add_field(
                        name="An error occurred!",
                        value=f"Error provided by the official Hypixel API:\n{cause}",
                        inline=False,
                    )

        elif "minecraft_account" in USER_DATA.find_one({"_id": interaction.user.id}):
            minecraft_account: str = USER_DATA.find_one({"_id": interaction.user.id})[
                "minecraft_account"
            ]
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Your Discord account is linked to **{minecraft_account}**",
            )
        else:
            embed = nextcord.Embed(
                color=0xFFC800,
                title="You don't have your Minecraft account linked!\nDo so by using `/link <your username>`",
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(general_slash(bot))
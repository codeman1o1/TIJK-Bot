import datetime
import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands
import requests
from mojang import MojangAPI

from views.buttons.github import github_button

from main import HYPIXEL_API_KEY, SLASH_GUILDS, USER_DATA


class general_slash(commands.Cog, name="General Slash"):
    """Slash commands that everyone can use"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    async def github(self, interaction: Interaction):
        """Send a link to the official TIJK Bot GitHub page"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="View the official TIJK Bot code now!",
            value="https://github.com/codeman1o1/TIJK-Bot",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, view=github_button())

    @slash(guild_ids=SLASH_GUILDS)
    async def hypixelparty(self, interaction: Interaction):
        """Choose a random player who can own the party"""
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

    @slash(guild_ids=SLASH_GUILDS)
    async def link(
        self,
        interaction: Interaction,
        username: str = SlashOption(description="Your username", required=False),
    ):
        """Link your Minecraft account"""
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

    @slash(guild_ids=SLASH_GUILDS)
    async def birthday(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @birthday.subcommand(name="send", inherit_hooks=True)
    async def send_birthday(self, interaction: Interaction):
        """Send all birthdays"""
        birthdays = []
        embed = nextcord.Embed(color=0x0DD91A)
        today = datetime.date.today()
        year = today.year
        for user in USER_DATA.find():
            if "birthday" in user:
                birthday = user["birthday"]
                user = self.bot.get_user(int(user["_id"]))
                birthday2 = birthday.split("-")
                date = datetime.date(year, int(birthday2[1]), int(birthday2[0]))
                diff = date - today
                while diff.days < 0:
                    year += 1
                    date = datetime.date(year, int(birthday2[1]), int(birthday2[0]))
                    diff = date - today
                birthdays_dictionary = {
                    "userName": user.name,
                    "birthday": birthday,
                    "year": year,
                    "daysLeft": diff.days,
                }
                birthdays.append(birthdays_dictionary.copy())
        birthdays = sorted(birthdays, key=lambda i: i["daysLeft"])
        for user in birthdays:
            USERNAME = user["userName"]
            BIRTHDAY = user["birthday"]
            YEAR = user["year"]
            DAYS_LEFT = user["daysLeft"]
            embed.add_field(
                name=f"{USERNAME}'s birthday is on",
                value=f"{BIRTHDAY}-{YEAR} ({DAYS_LEFT} days left)",
                inline=False,
            )
        if embed.fields == 0:
            embed = nextcord.Embed(color=0x0DD91A, title="No-one has a birthday set!")
        await interaction.response.send_message(embed=embed)

    @birthday.subcommand(name="get", inherit_hooks=True)
    async def get_birthday(self, interaction: Interaction):
        """Get your birthday"""
        if "birthday" in USER_DATA.find_one({"_id": interaction.user.id}):
            birthday = USER_DATA.find_one({"_id": interaction.user.id})["birthday"]
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Your birthday is set to **{birthday}**",
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="You don't have a birthday set!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @birthday.subcommand(name="set", inherit_hooks=True)
    async def set_birthday(
        self,
        interaction: Interaction,
        date: str = SlashOption(
            description="Your birthday. Format: day-month", required=True
        ),
    ):
        """Set your birthday"""
        try:
            today = datetime.date.today()
            date2 = date.split("-")
            datetime.date(today.year, int(date2[1]), int(date2[0]))
        except (ValueError, IndexError):
            embed = nextcord.Embed(
                color=0xFFC800, title=f"**{date}** is not a valid date!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        query = {"_id": interaction.user.id}
        if USER_DATA.count_documents(query) == 0:
            post = {"_id": interaction.user.id, "birthday": date}
            USER_DATA.insert_one(post)
        else:
            USER_DATA.update_one(
                {"_id": interaction.user.id}, {"$set": {"birthday": date}}
            )
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Your birthday is set to **{date}**!"
        )
        await interaction.response.send_message(embed=embed)

    @birthday.subcommand(name="remove", inherit_hooks=True)
    async def remove_birthday(self, interaction: Interaction):
        """Remove your birthday"""
        if "birthday" in USER_DATA.find_one({"_id": interaction.user.id}):
            USER_DATA.update_one(
                {"_id": interaction.user.id}, {"$unset": {"birthday": ""}}
            )
            embed = nextcord.Embed(
                color=0x0DD91A, title="Your birthday has been removed!"
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="You don't have a birthday set!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(general_slash(bot))

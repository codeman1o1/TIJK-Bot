import datetime
import random
from urllib.parse import quote

import nextcord
import requests
from mojang import API as MAPI
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands

from main import HYPIXEL_API_KEY, logger
from utils.database import USER_DATA, get_user_data, set_user_data, unset_user_data
from views.buttons.link import Link

MojangAPI = MAPI()


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash()
    async def github(self, interaction: Interaction):
        """Send a link to the official TIJK Bot GitHub page"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="View the official TIJK Bot code now!",
            value="https://github.com/codeman1o1/TIJK-Bot",
            inline=False,
        )
        await interaction.response.send_message(
            embed=embed, view=Link("https://github.com/codeman1o1/TIJK-Bot")
        )

    @slash()
    async def avatar(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user of which you want to download their avatar",
            required=True,
        ),
    ):
        """Get someone's avatar"""
        avatars_list = []

        def target_avatar_formats(avatar):
            formats = ["JPEG", "PNG", "WebP"]
            if avatar.is_animated():
                formats.append("GIF")
            return formats

        if not user.avatar and not user.guild_avatar:
            await interaction.send(
                f"**{user}** has no avatar set, at all...", ephemeral=True
            )
            return

        if user.avatar:
            avatars_list.append(
                "**Account avatar:** "
                + " **-** ".join(
                    f"[{img_format}]({user.avatar.replace(format=img_format.lower(), size=1024)})"
                    for img_format in target_avatar_formats(user.avatar)
                )
            )

        embed = nextcord.Embed(
            title=f"🖼 Here is the avatar of **{user}**", color=0x0DD91A
        )

        if user.guild_avatar:
            avatars_list.append(
                "**Server avatar:** "
                + " **-** ".join(
                    f"[{img_format}]({user.guild_avatar.replace(format=img_format.lower(), size=1024)})"
                    for img_format in target_avatar_formats(user.guild_avatar)
                )
            )
            embed.set_thumbnail(url=user.avatar.replace(format="png"))

        embed.set_image(
            url=f"{user.display_avatar.replace(static_format='png', size=256)}"
        )
        embed.description = "\n".join(avatars_list)

        await interaction.send(embed=embed)

    @slash(guild_ids=(870973430114181141, 865146077236822017))
    async def hypixelparty(self, interaction: Interaction):
        """Choose a random player who can own the party"""
        hypixel_ping = nextcord.utils.get(interaction.guild.roles, name="Hypixel Ping")
        available = [
            user
            for user in interaction.channel.members
            if not user.bot and hypixel_ping in user.roles
        ]
        round_1 = ", ".join(str(user) for user in available) if available else "Nobody"
        remove = []
        if available:
            for user in available:
                if get_user_data(user.id, "minecraft_account"):
                    uuid = MojangAPI.get_uuid(
                        get_user_data(user.id, "minecraft_account")
                    )
                    response = requests.get(
                        f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
                    )
                    data = response.json()
                    if response.status_code == 429:
                        if data["global"] is True:
                            embed = nextcord.Embed(
                                color=0xFFC800,
                                title="Unfortunately, the Hypixel API is currently unavailable\nThis is for all users trying to access the Hypixel API\nPlease try again later",
                            )
                        else:
                            embed = nextcord.Embed(
                                color=0xFFC800,
                                title="Unfortunately, the Hypixel API is currently unavailable\nThis is due to it being rate limited (the limit is 120 requests per minute)\nPlease try again later",
                            )
                        await interaction.response.send_message(embed=embed)
                        return
                    if data["success"] is False:
                        cause = data["cause"]
                        embed = nextcord.Embed(
                            color=0xFF0000, title=f"An error occurred:\n{cause}"
                        )
                        embed.set_footer(
                            text="Click the button below to report this error"
                        )
                        await interaction.send(
                            embed=embed,
                            view=Link(
                                f"https://github.com/codeman1o1/TIJK-Bot/issues/new?assignees=&labels=bug&template=error.yaml&title=%5BERROR%5D+{quote(str(cause))}",
                                "Report error",
                            ),
                        )
                        logger.error(cause)
                        return
                    logouttime = data["player"]["lastLogout"]
                    logintime = data["player"]["lastLogin"]
                    if logouttime >= logintime:
                        remove.append(user)
                else:
                    remove.append(user)
        for user in remove:
            available.remove(user)
        round_2 = ", ".join(str(user) for user in available) if available else "Nobody"
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
        embed.set_footer(text=f"Round 1: {round_1}\nRound 2: {round_2}")
        await interaction.response.send_message(embed=embed, delete_after=300)

    @slash()
    async def link(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description='Your username. Type "remove" to remove.', required=False
        ),
    ):
        """Link your Minecraft account"""
        if username:
            if username.lower() == "remove":
                if get_user_data(interaction.user.id, "minecraft_account"):
                    embed = nextcord.Embed(
                        color=0xFFC800,
                        title="You don't have your Minecraft account linked!",
                    )
                else:
                    unset_user_data(interaction.user.id, "minecraft_account")
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title="Successfully removed your Minecraft account",
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
                                set_user_data(
                                    interaction.user.id, "minecraft_account", username
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

        elif get_user_data(interaction.user.id, "minecraft_account"):
            minecraft_account: str = get_user_data(
                interaction.user.id, "minecraft_account"
            )
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

    @slash()
    async def birthday(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @birthday.subcommand(name="send", inherit_hooks=True)
    async def send_birthday(self, interaction: Interaction):
        """Send all birthdays"""
        birthdays = []
        embed = nextcord.Embed(color=0x0DD91A)
        for user in USER_DATA.find():
            if "birthday" in user:
                today = datetime.date.today()
                year: int = today.year
                birthday: str = user["birthday"]
                user = self.bot.get_user(int(user["_id"]))
                day, month = birthday.split("-")
                date = datetime.date(year, int(month), int(day))
                diff = date - today
                while diff.days < 0:
                    year += 1
                    date = datetime.date(year, int(month), int(day))
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
            username = user["userName"]
            birthday = user["birthday"]
            yeah = user["year"]
            days_left = user["daysLeft"]
            embed.add_field(
                name=f"{username}'s birthday is on",
                value=f"{birthday}-{yeah} ({days_left} days left)",
                inline=False,
            )
        if embed.fields == 0:
            embed = nextcord.Embed(color=0x0DD91A, title="No-one has a birthday set!")
        await interaction.response.send_message(embed=embed)

    @birthday.subcommand(name="get", inherit_hooks=True)
    async def get_birthday(self, interaction: Interaction):
        """Get your birthday"""
        if get_user_data(interaction.user.id, "birthday"):
            birthday: str = get_user_data(interaction.user.id, "birthday")
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
            try:
                day, month = date.split("-")
            except ValueError:
                embed = nextcord.Embed(
                    color=0xFF0000,
                    title="Please use the correct format: day-month",
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            datetime.date(today.year, int(month), int(day))
        except (ValueError, IndexError):
            embed = nextcord.Embed(
                color=0xFFC800, title=f"**{date}** is not a valid date!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        set_user_data(interaction.user.id, "birthday", date)
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Your birthday is set to **{date}**!"
        )
        await interaction.response.send_message(embed=embed)

    @birthday.subcommand(name="remove", inherit_hooks=True)
    async def remove_birthday(self, interaction: Interaction):
        """Remove your birthday"""
        if get_user_data(interaction.user.id, "birthday"):
            unset_user_data(interaction.user.id, "birthday")
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
    bot.add_cog(General(bot))

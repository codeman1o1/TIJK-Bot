import datetime
import random

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from views.github import github_button
import requests
from mojang import MojangAPI

from main import USER_DATA, HYPIXEL_API_KEY


class general(commands.Cog, name="General"):
    """Commands that everyone can use"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="github", aliases=["git", "source"])
    async def github(self, ctx: Context):
        """Sends a link to the official TIJK Bot GitHub page"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="View the official TIJK Bot code now!",
            value="https://github.com/codeman1o1/TIJK-Bot",
            inline=False,
        )

        await ctx.send(embed=embed, view=github_button())

    @commands.group(name="hypixelparty", invoke_without_command=True, aliases=["hpp"])
    async def hypixelparty(self, ctx: Context):
        """Chooses a random player that can own the party"""
        await ctx.channel.purge(limit=1)
        hypixel_ping = nextcord.utils.get(ctx.guild.roles, name="Hypixel Ping")
        available = [
            user
            for user in ctx.guild.members
            if not user.bot
            if user.status != nextcord.Status.offline
            if hypixel_ping in user.roles
        ]
        if available:
            for k in available:
                user = await commands.converter.UserConverter().convert(ctx, k)
                query = {"_id": user.id}
                if USER_DATA.count_documents(query) != 0:
                    for k in USER_DATA.find(query):
                        if "minecraft_account" in k:
                            username = k["minecraft_account"]
                            uuid = MojangAPI.get_uuid(username)
                            data = requests.get(
                                f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
                            ).json()
                            logouttime = data["player"]["lastLogout"]
                            logintime = data["player"]["lastLogin"]
                            if not logouttime < logintime or data["success"] == False:
                                available.remove(str(user))
                        else:
                            available.remove(str(user))
                else:
                    available.remove(k)
        if available:
            embed = nextcord.Embed(color=0x0DD91A)
            randomInt = random.randint(0, len(available) - 1)
            embed.add_field(
                name="Party leader chosen!",
                value=f"{available[randomInt]} will be the party leader!",
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title="Nobody meets the requirements to be the party leader!",
            )
        await ctx.send(embed=embed, delete_after=300)
        available.clear()

    @hypixelparty.command(name="link")
    async def link_hypixelparty(self, ctx: Context, username: str):
        """Link your Minecraft account"""
        if username.lower() == "remove":
            query = {"_id": ctx.author.id}
            if USER_DATA.count_documents(query) == 0:
                embed = nextcord.Embed(
                    color=0xFFC800,
                    title="You don't have your Minecraft account linked!",
                )
            else:
                for k in USER_DATA.find(query):
                    if k["minecraft_account"]:
                        account = k["minecraft_account"]
                        USER_DATA.update_one(
                            {"_id": ctx.author.id},
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
            if data["success"] == True:
                try:
                    if "DISCORD" in data["player"]["socialMedia"]["links"].keys():
                        if (
                            data["player"]["socialMedia"]["links"]["DISCORD"]
                            == f"{ctx.author}"
                        ):
                            query = {"_id": ctx.author.id}
                            if USER_DATA.count_documents(query) == 0:
                                post = {
                                    "_id": ctx.author.id,
                                    "minecraft_account": username,
                                }
                                USER_DATA.insert_one(post)
                            else:
                                USER_DATA.update_one(
                                    {"_id": ctx.author.id},
                                    {"$set": {"minecraft_account": username}},
                                )
                            embed = nextcord.Embed(
                                color=0x0DD91A,
                                title=f"Linked your account to **{username}**",
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
                    name="An error occured!",
                    value=f"Error provided by the offical Hypixel API:\n{cause}",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @commands.group(name="admin", invoke_without_command=True)
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def admin(self, ctx: Context, admin: nextcord.Member, *, message: str):
        """Contact an admin"""
        owner_role = nextcord.utils.get(ctx.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(ctx.guild.roles, name="Admin")
        admin_roles = (owner_role, admin_role)
        if any(roles in admin.roles for roles in admin_roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(name="Bruh", value="Get some help", inline=False)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name="Someone needs your help!",
                    value=f"{ctx.author} needs your help with {message}",
                    inline=False,
                )

                await admin.send(embed=embed)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name="Asked for help!",
                    value=f"Asked {admin.display_name} for help with the  message {message}",
                    inline=False,
                )

        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"{admin.display_name} is not an admin!",
            )

        await ctx.send(embed=embed)

    @admin.command(name="urgent")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def urgent_admin(self, ctx: Context, admin: nextcord.Member, *, message: str):
        """Makes the .admin command urgent"""
        owner_role = nextcord.utils.get(ctx.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(ctx.guild.roles, name="Admin")
        admin_roles = (owner_role, admin_role)
        if any(roles in admin.roles for roles in admin_roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(name="Bruh", value="Get some urgent help", inline=False)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name="Someone needs your urgent help!",
                    value=f"{ctx.author} needs your help with {message}",
                    inline=False,
                )

                await admin.send(f"{admin.mention}", embed=embed)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name="Asked for urgent help!",
                    value=f"Asked {admin.display_name} for help with the  message {message}",
                    inline=False,
                )

        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"{admin.display_name} is not an admin!",
            )

        await ctx.send(embed=embed)

    @commands.group(name="birthday", invoke_without_command=True, aliases=["bday"])
    async def birthday(self, ctx: Context):
        """Sends birthday dates"""
        birthdays = []
        embed = nextcord.Embed(color=0x0DD91A)
        today = datetime.date.today()
        year = today.year
        for k in USER_DATA.find():
            try:
                user = self.bot.get_user(int(k["_id"]))
                birthday = k["birthday"]
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
            except KeyError:
                pass
        birthdays = sorted(birthdays, key=lambda i: i["daysLeft"])
        for k in birthdays:
            userName = k["userName"]
            birthday = k["birthday"]
            year = k["year"]
            daysLeft = k["daysLeft"]
            embed.add_field(
                name=f"{userName}'s birthay is on",
                value=f"{birthday}-{year} ({daysLeft} days left)",
                inline=False,
            )
        if embed.fields == 0:
            embed = nextcord.Embed(color=0x0DD91A, title="No-one has a birthday set!")
        await ctx.send(embed=embed)

    @birthday.command(name="set")
    async def set_birthday(self, ctx: Context, date=None):
        """Sets your birthday"""
        if not date:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Type your birthday as following:",
                value="day-month\nFor example: 22-05",
                inline=False,
            )

        if date:
            try:
                today = datetime.date.today()
                date2 = date.split("-")
                datetime.date(today.year, int(date2[1]), int(date2[0]))
            except (ValueError, IndexError):
                embed = nextcord.Embed(
                    color=0xFFC800, title=f"{date} is not a valid date!"
                )
                await ctx.send(embed=embed)
                return
            query = {"_id": ctx.author.id}
            if USER_DATA.count_documents(query) == 0:
                post = {"_id": ctx.author.id, "birthday": date}
                USER_DATA.insert_one(post)
            else:
                USER_DATA.update_one(
                    {"_id": ctx.author.id}, {"$set": {"birthday": date}}
                )
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Your birthday is set to {date}!"
            )
        await ctx.send(embed=embed)

    @birthday.command(name="remove")
    async def remove_birthday(self, ctx: Context):
        """Removes your birthday"""
        USER_DATA.update_one({"_id": ctx.author.id}, {"$unset": {"birthday": ""}})
        embed = nextcord.Embed(color=0x0DD91A, title="Your birthday has been removed!")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(general(bot))

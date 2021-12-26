import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import random
import datetime

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


class general_buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            nextcord.ui.Button(
                label="Open in browser",
                url="https://github.com/codeman1o1/TIJK-Bot",
                style=ButtonStyle.url,
            )
        )


class general(
    commands.Cog,
    name="General",
    description="Commands that everyone can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="github",
        description="Sends a link to the official TIJK Bot GitHub page",
        brief="Sends a link to the official TIJK Bot GitHub page",
        aliases=["git", "source"],
    )
    async def github(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"View the official TIJK Bot code now!",
            value=f"https://github.com/codeman1o1/TIJK-Bot",
            inline=False,
        )
        await ctx.send(embed=embed, view=general_buttons())

    @commands.command(
        name="hypixelparty",
        description="Chooses randomly a player that can own the party",
        brief="Chooses randomly a player that can own the party",
        aliases=["hpp"],
    )
    async def hypixelparty(self, ctx):
        await ctx.channel.purge(limit=1)
        hypixel_ping = nextcord.utils.get(ctx.guild.roles, name="Hypixel Ping")
        available = [
            str(user.name) + "#" + str(user.discriminator)
            for user in ctx.guild.members
            if not user.bot
            if user.status != nextcord.Status.offline
            if hypixel_ping in user.roles
        ]
        if not len(available) == 0:
            embed = nextcord.Embed(color=0x0DD91A)
            randomInt = random.randint(0, len(available) - 1)
            embed.add_field(
                name=f"Party leader chosen!",
                value=f"{available[randomInt]} will be the party leader!",
                inline=False,
            )
        elif len(available) == 0:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Nobody meets the requirements to be the party leader!",
            )
        await ctx.send(embed=embed, delete_after=300)
        available.clear()

    @commands.group(
        name="admin",
        description="Contact an admin",
        brief="Contact an admin",
        invoke_without_command=True,
    )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def admin(self, ctx, admin: nextcord.Member, *, message):
        owner_role = nextcord.utils.get(ctx.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(ctx.guild.roles, name="Admin")
        admin_roles = (owner_role, admin_role)
        if any(roles in admin.roles for roles in admin_roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Bruh",
                    value=f"Get some help",
                    inline=False,
                )
                await ctx.send(embed=embed)
            elif not admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Someone needs your help!",
                    value=f"{ctx.author} needs your help with {message}",
                    inline=False,
                )
                await admin.send(embed=embed)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Asked for help!",
                    value=f"Asked {admin.display_name} for help with the  message {message}",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"{admin.display_name} is not an admin!",
            )
            await ctx.send(embed=embed)

    @admin.command(
        name="urgent",
        description="Makes the .admin command urgent",
        brief="Makes the .admin command urgent",
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def urgent_admin(self, ctx, admin: nextcord.Member, *, message: str):
        owner_role = nextcord.utils.get(ctx.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(ctx.guild.roles, name="Admin")
        admin_roles = (owner_role, admin_role)
        if any(roles in admin.roles for roles in admin_roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Bruh",
                    value=f"Get some urgent help",
                    inline=False,
                )
                await ctx.send(embed=embed)
            elif not admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Someone needs your urgent help!",
                    value=f"{ctx.author} needs your help with {message}",
                    inline=False,
                )
                await admin.send(f"{admin.mention}", embed=embed)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Asked for urgent help!",
                    value=f"Asked {admin.display_name} for help with the  message {message}",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"{admin.display_name} is not an admin!",
            )
            await ctx.send(embed=embed)

    @commands.group(
        name="birthday",
        description="Sends birthday dates",
        brief="Sends birthday dates",
        invoke_without_command=True,
        aliases=["bday"],
    )
    async def birthday(self, ctx):
        birthdays = []
        embed = nextcord.Embed(color=0x0DD91A)
        indexes = UserData.find()
        today = datetime.date.today()
        year = today.year
        for k in indexes:
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
            embed = nextcord.Embed(color=0x0DD91A, title=f"No-one has a birthday set!")
        await ctx.send(embed=embed)

    @birthday.command(
        name="set", description="Sets your birthday", brief="Sets your birthday"
    )
    async def set_birthday(self, ctx, date=None):
        if not date:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Type your birthday as following:",
                value=f"day-month\nFor example: 22-05",
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
            if UserData.count_documents(query) == 0:
                post = {"_id": ctx.author.id, "birthday": date}
                UserData.insert_one(post)
            else:
                UserData.update_one(
                    {"_id": ctx.author.id}, {"$set": {"birthday": date}}
                )
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Your birthday is set to {date}!"
            )
        await ctx.send(embed=embed)

    @birthday.command(
        name="remove",
        description="Removes your birthday",
        brief="Removes your birthday",
    )
    async def remove_birthday(self, ctx):
        UserData.update_one({"_id": ctx.author.id}, {"$unset": {"birthday": ""}})
        embed = nextcord.Embed(color=0x0DD91A, title=f"Your birthday has been removed!")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(general(bot))

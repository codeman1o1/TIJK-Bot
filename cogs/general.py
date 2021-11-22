import nextcord
from nextcord.ext import commands
import random
import datetime


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
        await ctx.send(embed=embed)

    @commands.command(
        name="hypixelparty",
        description="Chooses randomly a player that can own the party",
        brief="Chooses randomly a player that can own the party",
        aliases=["hypixelp", "hpparty", "hpp"],
    )
    async def hypixelparty(self, ctx):
        hpon = []
        for user in ctx.guild.members:
            if not user.bot:
                if user.status != nextcord.Status.offline:
                    hping = nextcord.utils.get(ctx.guild.roles, name="hypixel ping")
                    if hping in user.roles:
                        hpon.append(str(user.name) + "#" + str(user.discriminator))
        if not len(hpon) == 0:
            embed = nextcord.Embed(color=0x0DD91A)
            randomInt = random.randint(0, len(hpon) - 1)
            embed.add_field(
                name=f"Party leader chosen!",
                value=f"{hpon[randomInt]} will be the party leader!",
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Nobody meets the requirements to be the party leader!",
            )
        await ctx.send(embed=embed)
        hpon.clear()

    @commands.group(
        name="admin",
        description="Contact an admin",
        brief="Contact an admin",
        invoke_without_command=True,
    )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def admin(self, ctx, admin: nextcord.Member, *, message):
        ownerR = nextcord.utils.get(ctx.guild.roles, name="Owner")
        adminR = nextcord.utils.get(ctx.guild.roles, name="Admin")
        roles = [ownerR, adminR]
        if any(roles in admin.roles for roles in roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Bruh",
                    value=f"Get some help",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
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
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"That is not an admin!",
                value=f"{admin.display_name} is not an admin!",
                inline=False,
            )
            await ctx.send(embed=embed)

    @admin.command(
        name="urgent",
        description="Makes the .admin command urgent",
        brief="Makes the .admin command urgent",
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def urgent_admin(self, ctx, admin: nextcord.Member, *, message: str):
        ownerR = nextcord.utils.get(ctx.guild.roles, name="Owner")
        adminR = nextcord.utils.get(ctx.guild.roles, name="Admin")
        roles = [ownerR, adminR]
        if any(roles in admin.roles for roles in roles):
            if admin == ctx.author:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Bruh",
                    value=f"Get some urgent help",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Someone needs your urgent help!",
                    value=f"{ctx.author} needs your help with {message}",
                    inline=False,
                )
                await admin.send(admin.mention)
                await admin.send(embed=embed)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Asked for urgent help!",
                    value=f"Asked {admin.display_name} for help with the  message {message}",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"That is not an admin!",
                value=f"{admin.display_name} is not an admin!",
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="birthday",
        description="Sends birthday dates",
        brief="Sends birthday dates",
        aliases=["bday"],
    )
    async def birthday(self, ctx):
        info = ""
        today = datetime.date.today()
        karsten = datetime.date(2022, 3, 25)
        ian = datetime.date(2022, 3, 26)
        tim = datetime.date(2021, 12, 15)
        jacco = datetime.date(2022, 5, 27)
        jurre = datetime.date(2022, 1, 24)
        embed = nextcord.Embed(color=0x0DD91A)
        diff = karsten - today
        if diff.days < 0:
            info = "\nThis is outdated, please report it to codeman1o1#1450"
        embed.add_field(
            name=f"Karsten",
            value=f"March 25th\nDays left: {diff.days}{info}",
            inline=False,
        )
        info = ""
        diff = ian - today
        if diff.days < 0:
            info = "\nThis is outdated, please report it to codeman1o1#1450"
        embed.add_field(
            name=f"Ian",
            value=f"March 26th\nDays left: {diff.days}{info}",
            inline=False,
        )
        info = ""
        diff = tim - today
        if diff.days < 0:
            info = "\nThis is outdated, please report it to codeman1o1#1450"
        embed.add_field(
            name=f"Tim",
            value=f"December 15th\nDays left: {diff.days}{info}",
            inline=False,
        )
        info = ""
        diff = jacco - today
        if diff.days < 0:
            info = "\nThis is outdated, please report it to codeman1o1#1450"
        embed.add_field(
            name=f"Jacco",
            value=f"May 27th\nDays left: {diff.days}{info}",
            inline=False,
        )
        info = ""
        diff = jurre - today
        if diff.days < 0:
            info = "\nThis is outdated, please report it to codeman1o1#1450"
        embed.add_field(
            name=f"Jurre",
            value=f"Januari 24th\nDays left: {diff.days}{info}",
            inline=False,
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(general(bot))

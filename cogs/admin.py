import nextcord
from nextcord.ext import commands
from nextcord.utils import get
import asyncio
import json
import os


class admin(
    commands.Cog,
    name="Admin",
    description="Commands that only admins or owners can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="shutdown",
        description="Shuts down TIJK Bot",
        brief="Shuts down TIJK Bot",
        aliases=["stop"],
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def shutdown(self, ctx):
        mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"TIJK Bot was shut down",
            value=f"TIJK Bot was shut down by {ctx.author.name}#{ctx.author.discriminator}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await mo.send(embed=embed)
        codeman1o1 = self.bot.get_user(656950082431615057)
        dm = await codeman1o1.create_dm()
        await dm.send(embed=embed)
        print(
            "TIJK Bot was shut down by "
            + ctx.author.name
            + "#"
            + ctx.author.discriminator
        )
        await self.bot.close()

    @commands.command(
        name="ping",
        description="Get the latency of TIJK Bot",
        brief="Get the latency of TIJK Bot",
    )
    async def ping(self, ctx, roundNr: int = 1):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Pong!",
            value=f"The latency is {round(self.bot.latency, roundNr)} seconds",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="readtherules",
        description="Tells a user to read the rules",
        brief="Tells a user to read the rules",
        aliases=["rtr"],
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def read_the_rules(self, ctx, rule_number: int, user: nextcord.Member):
        await ctx.channel.purge(limit=1)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Hey {user.display_name}!",
            value=f"Please read rule number {rule_number}",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(name="mute", description="Mutes a user", brief="Mutes a user")
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def mute(self, ctx, user: nextcord.Member):
        muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
        owner = nextcord.utils.get(ctx.guild.roles, name="Owner")
        admin = nextcord.utils.get(ctx.guild.roles, name="Admin")
        mute_protection = [owner, admin]
        if not muted in user.roles:
            if not any(role in user.roles for role in mute_protection):
                mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
                await user.add_roles(muted)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"User muted!",
                    value=f"{user.display_name} was muted by {ctx.author.name}#{ctx.author.discriminator}\nType .unmute {user.display_name}#{user.discriminator} to unmute",
                    inline=False,
                )
                await ctx.send(embed=embed)
                await mo.send(embed=embed)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Could not mute {user.display_name}!",
                    value=f"You can't mute the owner or an admin!",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Could not mute {user.display_name}",
                value=f"{user.display_name} is already muted!",
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="tempmute",
        description="Temporarely mutes an user",
        brief="Temporarely mutes an user",
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def tempmute(self, ctx, user: nextcord.Member, time: str):
        timeS = time
        timeL = ["s", "m", "h", "d"]
        if any(timeLI in time for timeLI in timeL):
            if time.endswith("s"):
                time = time.replace("s", "")
                timeS = time + " second(s)"
            elif time.endswith("m"):
                time = time.replace("m", "")
                timeS = time + " minute(s)"
                time = int(time)
                time = time * 60
            elif time.endswith("h"):
                time = time.replace("h", "")
                timeS = time + " hour(s)"
                time = int(time)
                time = time * 60
                time = time * 60
            elif time.endswith("d"):
                time = time.replace("d", "")
                timeS = time + " day(s)"
                time = int(time)
                time = time * 60
                time = time * 60
                time = time * 24
            time = int(time)
            muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
            owner = nextcord.utils.get(ctx.guild.roles, name="Owner")
            admin = nextcord.utils.get(ctx.guild.roles, name="Admin")
            mute_protection = [owner, admin]
            if not muted in user.roles:
                if not any(role in user.roles for role in mute_protection):
                    mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
                    await user.add_roles(muted)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{user.display_name} was muted for {timeS} by {ctx.author.name}#{ctx.author.discriminator}\nType .unmute {user.display_name}#{user.discriminator} to unmute",
                        inline=False,
                    )
                    await ctx.send(embed=embed)
                    await mo.send(embed=embed)
                    await asyncio.sleep(time)
                    await user.remove_roles(muted)
                    embed = nextcord.Embed(
                        color=0x0DD91A, title=f"{user.display_name} is now unmuted!"
                    )
                    await ctx.send(embed=embed)
                    await mo.send(embed=embed)
                else:
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"Could not mute {user.display_name}!",
                        value=f"You can't mute the owner or an admin!",
                        inline=False,
                    )
                    await ctx.send(embed=embed)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Could not mute {user.display_name}",
                    value=f"{user.display_name} is already muted!",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"{time} is not a valid option!",
                value=f"The time must end with any of the following:\n> s (seconds)\n> m (minutes)\n> h (hours)\n> d (days)",
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="unmute", description="Unmutes a user", brief="Unmutes a user"
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def unmute(self, ctx, user: nextcord.Member):
        muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
        if muted in user.roles:
            mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
            await user.remove_roles(muted)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"User unmuted!",
                value=f"{user.display_name} was unmuted by {ctx.author.name}#{ctx.author.discriminator}",
                inline=False,
            )
            await ctx.send(embed=embed)
            await mo.send(embed=embed)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Could not unmute {user.display_name}",
                value=f"{user.display_name} is not muted!",
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="nick",
        description="Gives a user a nickname",
        brief="Gives a user a nickname",
    )
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def nick(self, ctx, user: nextcord.Member, *, name):
        original_name = user.display_name
        await user.edit(nick=name)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Nickname changed!",
            value=f"{original_name}'s nickname has been changed to {name}",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="assignrole",
        description="Gives a user a role",
        brief="Gives a user a role",
        aliases=["ar"],
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def assignrole(self, ctx, role: nextcord.Role, user: nextcord.Member = None):
        if user == None:
            user = ctx.author
        if not role in user.roles:
            mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
            await user.add_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Role assigned!",
                value=f'Role "{role}" has been assigned to {user.display_name} by {ctx.author.name}#{ctx.author.discriminator}',
                inline=False,
            )
            await ctx.send(embed=embed)
            await mo.send(embed=embed)

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Could not assign that role!",
                value=f'{user.display_name} already has the "{role}" role',
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="removerole",
        description="Removes a role from a user",
        brief="Removes a role from a user",
        aliases=["rr"],
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def removerole(self, ctx, role: nextcord.Role, user: nextcord.Member = None):
        if user == None:
            user = ctx.author
        if role in user.roles:
            mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
            await user.remove_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Role removed!",
                value=f'Role "{role}" has been removed from {user.display_name} by {ctx.author.name}#{ctx.author.discriminator}',
                inline=False,
            )
            await ctx.send(embed=embed)
            await mo.send(embed=embed)

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Could not remove that role!",
                value=f'{user.display_name} does not have the "{role}" role',
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="clear", description="Clears the chat", brief="Clears the chat"
    )
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def clear(self, ctx, amount: int = 10):
        extra = ""
        if amount > 100:
            amount = 100
            extra = " (only 100 messages can be deleted at the same time)"
        await ctx.channel.purge(limit=amount + 1)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{amount}{extra} messages cleared!",
            value=f"This message wil delete itself after 5 seconds",
            inline=False,
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(
        name="kick",
        description="Kicks a user from the server",
        brief="Kicks a user from the server",
    )
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def kick(self, ctx, user: nextcord.Member, *, reason="No reason provided"):
        mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
        await user.kick(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"User kicked!",
            value=f"{user.display_name} has been kicked by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await mo.send(embed=embed)

    @commands.command(
        name="ban",
        description="Bans a user from the server",
        brief="Bans a user from the server",
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def ban(self, ctx, user: nextcord.Member, *, reason="No reason provided"):
        mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
        await user.ban(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"User banned!",
            value=f"{user.display_name} has been banned by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await mo.send(embed=embed)

    @commands.group(
        name="warn",
        description="Warn someone",
        brief="Warn someone",
        invoke_without_command=True,
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def warn(
        self,
        ctx,
        user: nextcord.Member,
        amount: int = 1,
        *,
        reason="No reason provided",
    ):
        with open(os.getcwd() + "\warns.json", "r+") as f:
            data = json.load(f)
            try:
                data[str(user.id)] = int(data[str(user.id)]) - amount
            except:
                data[str(user.id)] = 10 - amount
            remaining = data[str(user.id)]
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        embed = nextcord.Embed(color=0x0DD91A)
        if remaining > 0:
            embed.add_field(
                name=f"{user.display_name} has been warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}",
                value=f"{user.display_name} has {remaining} warns left!",
                inline=False,
            )
        if remaining == 0:
            embed.add_field(
                name=f"{user.display_name} has been warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}",
                value=f"{user.display_name} has no more warns left! Next time, he shall be punished!",
                inline=False,
            )
        if remaining < 0:
            punish = 0
            while True:
                if remaining < 0:
                    with open(os.getcwd() + "\warns.json", "r+") as f:
                        data = json.load(f)
                        try:
                            data[str(user.id)] = int(data[str(user.id)]) + 10
                        except:
                            data[str(user.id)] = 10 - amount
                        remaining = data[str(user.id)]
                        punish = punish + 1
                        f.seek(0)
                        json.dump(data, f, indent=2)
                        f.truncate()
                else:
                    break
            punishTime = punish * 10
            embed.add_field(
                name=f"{user.display_name} exceeded the warn limit {punish} time(s)!",
                value=f"He shall be punished with a {punishTime} minute mute!",
                inline=False,
            )
            await ctx.send(embed=embed)
            punishTime = punishTime * 60
            muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
            if not muted in user.roles:
                mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
                await user.add_roles(muted)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"User muted!",
                    value=f"{user.display_name} was muted by Warn System",
                    inline=False,
                )
                await mo.send(embed=embed)
                await asyncio.sleep(punishTime)
                await user.remove_roles(muted)
                embed = nextcord.Embed(
                    color=0x0DD91A, title=f"{user.display_name} is now unmuted!"
                )
                await mo.send(embed=embed)
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Could not mute {user.display_name}",
                    value=f"{user.display_name} is already muted!",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @warn.command(
        name="add",
        description="Adds a warn point to someone",
        brief="Adds a warn point to someone",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_warn(
        self,
        ctx,
        user: nextcord.Member,
        amount: int = 1,
        *,
        reason="No reason provided",
    ):
        with open(os.getcwd() + "\warns.json", "r+") as f:
            data = json.load(f)
            try:
                data[str(user.id)] = int(data[str(user.id)]) + amount
            except:
                data[str(user.id)] = 10 + amount
                warnPoints = data[str(user.id)]
            warnPoints = data[str(user.id)]
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{user.display_name} now has {amount} warn point(s) extra because of {reason}!",
            value=f"{user.display_name} now has a total of {warnPoints} warn points!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @warn.command(
        name="list",
        description="Lists the warn points of everyone that received at least 1",
        brief="Lists the warn points of everyone that received at least 1",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def list_warn(self, ctx):
        with open(os.getcwd() + "\warns.json", "r+") as f:
            data = json.load(f)
            if str(data) == "{}":
                embed = nextcord.Embed(
                    color=0x0DD91A, title=f"Nobody has been warned yet!"
                )
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                for k in data:
                    u = self.bot.get_user(int(k))
                    if not u == None:
                        embed.add_field(
                            name=f"{u} has",
                            value=f"{data[k]} warn points",
                            inline=False,
                        )
        await ctx.send(embed=embed)

    @warn.command(
        name="get", description="Gets your warn points", brief="Gets your warn points"
    )
    async def get_warn(self, ctx):
        with open(os.getcwd() + "\warns.json", "r+") as f:
            data = json.load(f)
            try:
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f"{ctx.author.display_name} has {data[str(ctx.author.id)]} warn points",
                )
            except:
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f"{ctx.author.display_name} has 10 warn points",
                )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))

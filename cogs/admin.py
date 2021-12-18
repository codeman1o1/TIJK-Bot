import nextcord
from nextcord.errors import HTTPException
from nextcord.ext import commands
from cogs.role_view import RoleView
from dotenv import load_dotenv
from pymongo import MongoClient
import asyncio
import os


load_dotenv(os.path.join(os.getcwd() + "\.env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


class admin(
    commands.Cog,
    name="Admin",
    description="Commands that only admins or owners can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(RoleView())

    @commands.group(
        name="buttonroles",
        description="Sends a message with buttons where people can get roles",
        brief="Sends a message with buttons where people can get roles",
        invoke_without_command=True,
        aliases=["br"],
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def buttonroles(self, ctx):
        roles = BotData.find()
        for k in roles:
            roles = k["roles"]
        if len(roles) == 0:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"There are no roles selected!\nMake sure to add them by using `.br add <role>`",
            )
            await ctx.send(embed=embed)
        elif len(roles) > 0:
            await ctx.channel.purge(limit=1)
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Click a button to add/remove that role!"
            )
            await ctx.send(embed=embed, view=RoleView())

    @buttonroles.command(
        name="list",
        description="Lists all button roles",
        brief="Lists all button roles",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def list_buttonroles(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        roles = BotData.find()
        for k in roles:
            roles = k["roles"]
        roles = "> " + str(roles)
        roles = roles.replace("[", "")
        roles = roles.replace("]", "")
        roles = roles.replace("'", "")
        roles = roles.replace(",", "\n>")
        embed.add_field(
            name=f"The current button roles are:",
            value=roles,
            inline=False,
        )
        await ctx.send(embed=embed)

    @buttonroles.command(
        name="add", description="Adds a button role", brief="Adds a button role"
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_buttonroles(self, ctx, role: nextcord.Role):
        role = str(role)
        role = role.replace("@", "")
        roles = BotData.find()
        for k in roles:
            roles = k["roles"]
            if not role in roles:
                roles.append(role)
                BotData.update_one(
                    {"_id": k["_id"]},
                    {"$set": {"roles": roles}},
                    upsert=False,
                )
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f'The "{role}" role has been added!\nMake sure to use `.buttonroles` again!',
                )
            elif role in roles:
                embed = nextcord.Embed(
                    color=0x0DD91A, title=f'The "{role}" role is already listed!'
                )
            await ctx.send(embed=embed)

    @buttonroles.command(
        name="remove",
        description="Removes a button role",
        brief="Removes a button role",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_buttonroles(self, ctx, role: nextcord.Role):
        role = str(role)
        role = role.replace("@", "")
        roles = BotData.find()
        for k in roles:
            roles = k["roles"]
            if role in roles:
                roles.remove(role)
                BotData.update_one(
                    {"_id": k["_id"]},
                    {"$set": {"roles": roles}},
                    upsert=False,
                )
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f'The "{role}" role has been Removed!\nMake sure to use `.buttonroles` again!',
                )
                await ctx.send(embed=embed)
            elif not role in roles:
                embed = nextcord.Embed(
                    color=0x0DD91A, title=f'The "{role}" role is not listed!'
                )
                await ctx.send(embed=embed)

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
        channel = nextcord.utils.get(ctx.guild.channels, name="rules")
        messages = await channel.history(limit=50).flatten()
        messages.reverse()
        await ctx.channel.purge(limit=1)
        try:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Hey {user.display_name}, please read rule number {rule_number}!",
                value=f"{messages[rule_number - 1].content}",
                inline=False,
            )
            embed.set_footer(text="You also received 1 warn!")
            await ctx.send(embed=embed)
            query = {"_id": user.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": user.id, "warns": 1}
                UserData.insert_one(post)
                total = 1
            else:
                user2 = UserData.find(query)
                warns = 0
                try:
                    for result in user2:
                        warns = result["warns"]
                except KeyError:
                    pass
                warns = warns + 1
                UserData.update_one({"_id": user.id}, {"$set": {"warns": warns}})
                total = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total <= 8:
                embed.add_field(
                    name=f"{user.display_name} has been warned by Warn System",
                    value=f"{user.display_name} has {10 - total} warns left!",
                    inline=False,
                )
            if total == 9:
                embed.add_field(
                    name=f"{user.display_name} has been warned by Warn System",
                    value=f"{user.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total >= 10:
                query = {"_id": user.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": user.id, "warns": 0}
                    UserData.insert_one(post)
                else:
                    UserData.update_one({"_id": user.id}, {"$set": {"warns": 0}})
                embed.add_field(
                    name=f"{user.display_name} exceeded the warn limit!",
                    value=f"He shall be punished with a 10 minute mute!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
                if not muted in user.roles:
                    mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
                    await user.add_roles(muted)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{user.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await mo.send(embed=embed)
                    await asyncio.sleep(600)
                    await user.remove_roles(muted)
                    embed = nextcord.Embed(
                        color=0x0DD91A, title=f"{user.display_name} is now unmuted!"
                    )
                    await mo.send(embed=embed)
        except IndexError:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"{rule_number} is not a valid rule number!"
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
            value=f"{user.name}#{user.discriminator} has been banned by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await mo.send(embed=embed)

    @commands.command(
        name="unban",
        description="Unbans a user from the server",
        brief="Unbans a user from the server",
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def unban(self, ctx, user, *, reason="No reason provided"):
        user = await commands.converter.UserConverter().convert(ctx, user)
        embed = nextcord.Embed(color=0x0DD91A)
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
            await ctx.guild.unban(user, reason=reason)
            embed.add_field(
                name=f"User unbanned!",
                value=f"{user.name}#{user.discriminator} has been unbanned by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
                inline=False,
            )
            await mo.send(embed=embed)
        else:
            embed.add_field(
                name=f"Unbanning failed!",
                value=f"{user.display_name} is not banned!",
                inline=False,
            )

        await ctx.send(embed=embed)

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
        async with ctx.typing():
            query = {"_id": user.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": user.id, "warns": 1}
                UserData.insert_one(post)
                total = 0 + amount
            else:
                user2 = UserData.find(query)
                warns = 0
                try:
                    for result in user2:
                        warns = result["warns"]
                except KeyError:
                    pass
                warns = warns + amount
                UserData.update_one({"_id": user.id}, {"$set": {"warns": warns}})
                total = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total <= 8:
                embed.add_field(
                    name=f"{user.display_name} has been warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}",
                    value=f"{user.display_name} has {10 - total} warns left!",
                    inline=False,
                )
            if total == 9:
                embed.add_field(
                    name=f"{user.display_name} has been warned by {ctx.author.name}#{ctx.author.discriminator} for {reason}",
                    value=f"{user.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total >= 10:
                query = {"_id": user.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": user.id, "warns": 0}
                    UserData.insert_one(post)
                else:
                    UserData.update_one({"_id": user.id}, {"$set": {"warns": 0}})
                embed.add_field(
                    name=f"{user.display_name} exceeded the warn limit!",
                    value=f"He shall be punished with a 10 minute mute!",
                    inline=False,
                )
                await ctx.send(embed=embed)
                muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
                if not muted in user.roles:
                    mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
                    await user.add_roles(muted)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{user.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await mo.send(embed=embed)
                    await asyncio.sleep(600)
                    await user.remove_roles(muted)
                    embed = nextcord.Embed(
                        color=0x0DD91A, title=f"{user.display_name} is now unmuted!"
                    )
                    await mo.send(embed=embed)
        await ctx.send(embed=embed)

    @warn.command(
        name="remove",
        description="Removes a warn from someone",
        brief="Removes a warn from someone",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_warn(
        self,
        ctx,
        user: nextcord.Member,
        amount: int = 1,
        *,
        reason="No reason provided",
    ):
        async with ctx.typing():
            query = {"_id": user.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": user.id, "warns": 0}
                UserData.insert_one(post)
            else:
                user2 = UserData.find(query)
                try:
                    for result in user2:
                        warns = result["warns"]
                except KeyError:
                    pass
                warns2 = warns
                warns = warns - amount
                if warns < 0:
                    warns = 0
                    amount = 0 + warns2
                UserData.update_one({"_id": user.id}, {"$set": {"warns": warns}})
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"{user.display_name} now has {amount} warn(s) less because {reason}!",
                value=f"{user.display_name} now has a total of {warns} warn(s)!",
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
        async with ctx.typing():
            embed = nextcord.Embed(color=0x0DD91A)
            indexes = UserData.find()
            for k in indexes:
                try:
                    user = self.bot.get_user(int(k["_id"]))
                    warns = k["warns"]
                    if not warns == 0:
                        embed.add_field(
                            name=f"{user} has",
                            value=f"{warns} warns",
                            inline=False,
                        )
                except KeyError:
                    pass
        try:
            await ctx.send(embed=embed)
        except HTTPException:
            embed = nextcord.Embed(color=0x0DD91A, title=f"Nobody has warns!")
            await ctx.send(embed=embed)

    @warn.command(
        name="get", description="Gets your warn points", brief="Gets your warn points"
    )
    async def get_warn(self, ctx):
        async with ctx.typing():
            for k in UserData.find({"_id": ctx.author.id}):
                try:
                    warns = k["warns"]
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"You ({ctx.author.display_name}) have {warns} warn(s)!",
                    )
                except KeyError:
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"You ({ctx.author.display_name}) have 0 warns!",
                    )
        await ctx.send(embed=embed)

    @commands.group(
        name="forbiddenwords",
        description="Shows the forbidden words",
        brief="Shows the forbidden words",
        invoke_without_command=True,
        aliases=["fwords", "fword"],
    )
    async def forbiddenwords(self, ctx):
        forbidden_words = BotData.find()
        for k in forbidden_words:
            forbidden_words = k["forbidden_words"]
        forbidden_words2 = ""
        for k in forbidden_words:
            forbidden_words2 = (
                f"{forbidden_words2} \n> {k} (index number {forbidden_words.index(k)})"
            )
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"These are the forbidden words",
            value=forbidden_words2,
            inline=False,
        )
        await ctx.send(embed=embed)

    @forbiddenwords.command(
        name="add", description="Adds a forbidden word", brief="Adds a forbidden word"
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_forbiddenwords(self, ctx, *, word: str):
        forbidden_words = BotData.find()
        for k in forbidden_words:
            forbidden_words = k["forbidden_words"]
            forbidden_words.append(word)
            BotData.update_one(
                {"_id": k["_id"]},
                {"$set": {"forbidden_words": forbidden_words}},
                upsert=False,
            )
        embed = nextcord.Embed(color=0x0DD91A, title=f"{word} is now a forbidden word!")
        await ctx.send(embed=embed)

    @forbiddenwords.command(
        name="remove",
        description="Removes a forbidden word",
        brief="Removes a forbidden word",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_forbiddenwords(self, ctx, *, index: int):
        forbidden_words = BotData.find()
        for k in forbidden_words:
            forbidden_words = k["forbidden_words"]
            word = forbidden_words[index]
            forbidden_words.remove(forbidden_words[index])
            BotData.update_one(
                {"_id": k["_id"]},
                {"$set": {"forbidden_words": forbidden_words}},
                upsert=False,
            )
        embed = nextcord.Embed(color=0x0DD91A, title=f"{word} is now an allowed word!")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))

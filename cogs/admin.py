import datetime
import os

import basic_logger as bl
import humanfriendly
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from pymongo import MongoClient
from views.button_roles import RoleView

from cogs import event_handler

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
        for k in BotData.find():
            roles = k["roles"]
        if len(roles) == 0:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title='There are no roles selected!\nMake sure to add them by using `.buttonroles add <role>`',
            )

            await ctx.send(embed=embed)
        elif len(roles) > 0:
            await ctx.channel.purge(limit=1)
            embed = nextcord.Embed(
                color=0x0DD91A, title='Click a button to add/remove that role!'
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
        for k in BotData.find():
            roles = k["roles"]
        roles = "> " + str(roles)
        roles = roles.replace("[", "")
        roles = roles.replace("]", "")
        roles = roles.replace("'", "")
        roles = roles.replace(",", "\n>")
        embed.add_field(
            name='The current button roles are:', value=roles, inline=False
        )

        await ctx.send(embed=embed)

    @buttonroles.command(
        name="add", description="Adds a button role", brief="Adds a button role"
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_buttonroles(self, ctx, role: nextcord.Role):
        role = role.name
        for k in BotData.find():
            roles = k["roles"]
            if role not in roles:
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
            else:
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
        role = role.name
        for k in BotData.find():
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
                    title=f'The "{role}" role has been removed!\nMake sure to use `.buttonroles` again!',
                )
            else:
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
        logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='TIJK Bot was shut down',
            value=f"TIJK Bot was shut down by {ctx.author.name}#{ctx.author.discriminator}",
            inline=False,
        )

        await ctx.send(embed=embed)
        await logs_channel.send(embed=embed)
        info = await self.bot.application_info()
        owner = await commands.converter.UserConverter().convert(ctx, str(info.owner))
        dm = await owner.create_dm()
        await dm.send(embed=embed)
        bl.info(
            "TIJK Bot was shut down by "
            + ctx.author.name
            + "#"
            + ctx.author.discriminator,
            __file__,
        )
        await self.bot.close()

    @commands.command(
        name="ping",
        description="Get the latency of TIJK Bot",
        brief="Get the latency of TIJK Bot",
    )
    async def ping(self, ctx, decimals: int = 1):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='Pong!',
            value=f"The latency is {round(self.bot.latency, decimals)} seconds",
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
            await event_handler.event_handler.warn_system(ctx, user)
        except IndexError:
            embed = nextcord.Embed(
                color=0xFF0000, title=f"{rule_number} is not a valid rule number!"
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="timeout",
        description="Mute a user",
        brief="Mutes a user",
        aliases=["to"],
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(
        self, ctx, user: nextcord.Member, time, *, reason="No reason provided"
    ):
        time = humanfriendly.parse_timespan(time)
        await user.edit(
            timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time)
        )
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='User muted!',
            value=f"{user.display_name} was muted by {ctx.author.name}#{ctx.author.discriminator} because of {reason}",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="unmute",
        description="Unmutes a user",
        brief="Unmutes a user",
    )
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute(self, ctx, user: nextcord.Member, *, reason="No reason provided"):
        await user.edit(timeout=None)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='User unmuted!',
            value=f"{user.display_name} was unmuted by {ctx.author.name}#{ctx.author.discriminator} because of {reason}",
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
            name='Nickname changed!',
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
        if user is None:
            user = ctx.author
        if role not in user.roles:
            logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
            await user.add_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name='Role assigned!',
                value=f'Role "{role}" has been assigned to {user.display_name} by {ctx.author.name}#{ctx.author.discriminator}',
                inline=False,
            )

            await ctx.send(embed=embed)
            await logs_channel.send(embed=embed)

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name='Could not assign that role!',
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
        if user is None:
            user = ctx.author
        if role in user.roles:
            logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
            await user.remove_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name='Role removed!',
                value=f'Role "{role}" has been removed from {user.display_name} by {ctx.author.name}#{ctx.author.discriminator}',
                inline=False,
            )

            await ctx.send(embed=embed)
            await logs_channel.send(embed=embed)

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name='Could not remove that role!',
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
        if amount > 99:
            amount = 99
            extra = " (only 100 messages can be deleted at the same time)"
        await ctx.channel.purge(limit=amount + 1)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{amount}{extra} messages cleared!",
            value='This message wil delete itself after 5 seconds',
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
        logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
        await user.kick(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='User kicked!',
            value=f"{user.display_name} has been kicked by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
            inline=False,
        )

        await ctx.send(embed=embed)
        await logs_channel.send(embed=embed)

    @commands.command(
        name="ban",
        description="Bans a user from the server",
        brief="Bans a user from the server",
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def ban(self, ctx, user: nextcord.Member, *, reason="No reason provided"):
        logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
        await user.ban(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name='User banned!',
            value=f"{user.name}#{user.discriminator} has been banned by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}\nUse `.unban {user.name}#{user.discriminator}` to unban {user.display_name}",
            inline=False,
        )

        await ctx.send(embed=embed)
        await logs_channel.send(embed=embed)

    @commands.command(
        name="unban",
        description="Unbans a user from the server",
        brief="Unbans a user from the server",
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def unban(self, ctx, user: str, *, reason="No reason provided"):
        user = await commands.converter.UserConverter().convert(ctx, user)
        embed = nextcord.Embed(color=0x0DD91A)
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
            await ctx.guild.unban(user, reason=reason)
            embed.add_field(
                name='User unbanned!',
                value=f"{user.name}#{user.discriminator} has been unbanned by {ctx.author.name}#{ctx.author.discriminator} with the reason {reason}",
                inline=False,
            )

            await logs_channel.send(embed=embed)
        else:
            embed.add_field(
                name='Unbanning failed!',
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
    ):
        await event_handler.event_handler.warn_system(ctx, user, amount)

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
        embed = nextcord.Embed(color=0x0DD91A)
        for k in UserData.find():
            try:
                user = self.bot.get_user(int(k["_id"]))
                warns = k["warns"]
                if warns != 0:
                    embed.add_field(
                        name=f"{user} has",
                        value=f"{warns} warns",
                        inline=False,
                    )
            except KeyError:
                pass
        if embed.fields == 0:
            embed = nextcord.Embed(color=0x0DD91A, title='Nobody has warns!')
        await ctx.send(embed=embed)

    @warn.command(
        name="get", description="Gets your warn points", brief="Gets your warn points"
    )
    async def get_warn(self, ctx):
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


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))

import datetime
import os

import basic_logger as bl
import humanfriendly
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from views.button_roles import button_roles
from views.profile_picture import profile_picture
import json

from main import warn_system, logger

from main import BOT_DATA, USER_DATA

BOT_PREFIXES = tuple(BOT_DATA.find_one()["botprefixes"])


class admin(commands.Cog, name="Admin"):
    """Commands that only admins or owners can use"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(button_roles(bot=bot))

    @commands.group(name="buttonroles", invoke_without_command=True, aliases=["br"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def buttonroles(self, ctx: Context):
        """Sends a message with buttons where people can get roles"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(ctx.guild.roles, id=buttonrole)
        )
        if roles > 0:
            await ctx.message.delete()
            embed = nextcord.Embed(
                color=0x0DD91A, title="Click a button to add/remove that role!"
            )

            await ctx.send(embed=embed, view=button_roles(ctx=ctx))
        else:
            embed = nextcord.Embed(
                color=0xFFC800,
                title="There are no button roles!\nMake sure to add them by using `.buttonroles add <role>`",
            )

            await ctx.send(embed=embed)

    @buttonroles.command(name="list")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def list_buttonroles(self, ctx: Context):
        """Lists all button roles"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(ctx.guild.roles, id=buttonrole)
        )
        if roles > 0:
            buttonroles2 = ""
            for buttonrole in buttonroles:
                if nextcord.utils.get(ctx.guild.roles, id=buttonrole):
                    buttonroles2 = (
                        buttonroles2
                        + "\n> "
                        + nextcord.utils.get(ctx.guild.roles, id=buttonrole).name
                    )
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="The current button roles are:",
                value=buttonroles2,
                inline=False,
            )
            embed.set_footer(text=f"{roles}/25 buttonroles")
        else:
            embed = nextcord.Embed(color=0xFFC800, title="There are no button roles")

        await ctx.send(embed=embed)

    @buttonroles.command(name="add")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_buttonroles(self, ctx: Context, role: nextcord.Role):
        """Adds a button role"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(ctx.guild.roles, id=buttonrole)
        )

        if roles >= 25:
            embed = nextcord.Embed(
                color=0xFFC800, title="You can only add 25 button roles!"
            )
        elif role.id not in buttonroles:
            buttonroles.append(role.id)
            BOT_DATA.update_one(
                {},
                {"$set": {"buttonroles": buttonroles}},
                upsert=False,
            )
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f'The "{role.name}" role has been added!\nMake sure to use `.buttonroles` again!',
            )
            await logger(ctx, f'The "{role.name}" role has been added to buttonroles')
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is already listed!'
            )
        await ctx.send(embed=embed)

    @buttonroles.command(name="remove")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_buttonroles(self, ctx: Context, role: nextcord.Role):
        """Removes a button role"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        if role.id in buttonroles:
            buttonroles.remove(role.id)
            BOT_DATA.update_one(
                {},
                {"$set": {"buttonroles": buttonroles}},
                upsert=False,
            )
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f'The "{role.name}" role has been removed!\nMake sure to use `.buttonroles` again!',
            )
            await logger(
                ctx, f'The "{role.name}" role has been removed from buttonroles'
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is not listed!'
            )
        await ctx.send(embed=embed)

    @commands.command(name="shutdown", aliases=["stop"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def shutdown(self, ctx: Context):
        """Shuts down TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot was shut down",
            value=f"TIJK Bot was shut down by {ctx.author}",
            inline=False,
        )

        await ctx.send(embed=embed)
        await logger(
            ctx,
            f"TIJK Bot was shut down by {ctx.author}",
        )
        info = await self.bot.application_info()
        owner = info.owner
        dm = await owner.create_dm()
        await dm.send(embed=embed)
        bl.info(f"TIJK Bot was shut down by {ctx.author}", __file__)
        await self.bot.close()

    @commands.command(name="ping")
    async def ping(self, ctx: Context, decimals: int = 1):
        """Get the latency of TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Pong!",
            value=f"The latency is {round(self.bot.latency, decimals)} seconds",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command(name="readtherules", aliases=["rtr", "rule"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def read_the_rules(
        self,
        ctx: Context,
        rule_number: int,
        user: nextcord.Member = None,
        *,
        reason: str = None,
    ):
        """Tells a user to read the rules"""
        channel = nextcord.utils.get(ctx.guild.channels, name="rules")
        messages = await channel.history(limit=50).flatten()
        messages.reverse()
        await ctx.message.delete()
        try:
            embed = nextcord.Embed(color=0x0DD91A)
            if user:
                embed.add_field(
                    name=f"Hey {user}, please read rule number {rule_number}!",
                    value=messages[rule_number - 1].content,
                    inline=False,
                )
                embed.set_footer(text="You also received 1 warn!")
                await ctx.send(embed=embed)
                await warn_system(ctx, user, 1, ctx.author, reason)
            else:
                embed.add_field(
                    name=f"Here is rule number {rule_number}:",
                    value=messages[rule_number - 1].content,
                    inline=False,
                )
                await ctx.send(embed=embed)
        except IndexError:
            embed = nextcord.Embed(
                color=0xFF0000, title=f"{rule_number} is not a valid rule number!"
            )
            await ctx.send(embed=embed)

    @commands.command(name="mute", aliases=["timeout", "to"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(
        self,
        ctx: Context,
        user: nextcord.Member,
        time: str,
        *,
        reason=None,
    ):
        """Mutes a user"""
        reason2 = f" because of {reason}" if reason else ""
        time = humanfriendly.parse_timespan(time)
        await user.edit(
            timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time)
        )
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User muted!",
            value=f"{user} was muted for {humanfriendly.format_timespan(time)} by {ctx.author}{reason2}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(
            ctx,
            f"{user} was muted for {humanfriendly.format_timespan(time)} by {ctx.author}{reason2}",
        )

    @commands.command(name="unmute")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute(self, ctx: Context, user: nextcord.Member, *, reason=None):
        """Unmutes a user"""
        reason2 = f" because of {reason}" if reason else ""
        await user.edit(timeout=None)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User unmuted!",
            value=f"{user} was unmuted by {ctx.author}{reason2}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(
            ctx,
            f"{user} was unmuted by {ctx.author}{reason2}",
        )

    @commands.command(name="nick")
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def nick(self, ctx: Context, user: nextcord.Member, *, name: str):
        """Gives a user a nickname"""
        original_name = user.display_name
        await user.edit(nick=name)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Nickname changed!",
            value=f"{original_name}'s nickname has been changed to {name}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(ctx, f"{original_name}'s nickname has been changed to {name}")

    @commands.command(name="assignrole", aliases=["ar"])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def assignrole(
        self, ctx: Context, role: nextcord.Role, user: nextcord.Member = None
    ):
        """Gives a user a role"""
        if user is None:
            user = ctx.author
        if role not in user.roles:
            await user.add_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role assigned!",
                value=f'Role "{role}" has been assigned to {user} by {ctx.author}',
                inline=False,
            )
            await ctx.send(embed=embed)
            await logger(
                ctx,
                f'Role "{role}" has been assigned to {user} by {ctx.author}',
            )

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Could not assign that role!",
                value=f'{user} already has the "{role}" role',
                inline=False,
            )

            await ctx.send(embed=embed)

    @commands.command(name="removerole", aliases=["rr"])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def removerole(
        self, ctx: Context, role: nextcord.Role, user: nextcord.Member = None
    ):
        """Removes a role from a user"""
        if user is None:
            user = ctx.author
        if role in user.roles:
            await user.remove_roles(role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role removed!",
                value=f'Role "{role}" has been removed from {user} by {ctx.author}',
                inline=False,
            )
            await ctx.send(embed=embed)
            await logger(
                ctx,
                f'Role "{role}" has been removed from {user} by {ctx.author}',
            )

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Could not remove that role!",
                value=f'{user} does not have the "{role}" role',
                inline=False,
            )

            await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def clear(self, ctx: Context, amount: int):
        """Clears the chat"""
        async with ctx.typing():
            await ctx.message.delete()
            deleted_messages = await ctx.channel.purge(limit=amount)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"{len(deleted_messages)} messages cleared!",
                value="This message wil delete itself after 5 seconds",
                inline=False,
            )
        await ctx.send(embed=embed, delete_after=5)
        await logger(
            ctx,
            f"{len(deleted_messages)} messages have been cleared from {ctx.message.channel.name}",
        )

    @commands.command(name="clean")
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def clean(self, ctx: Context, amount: int):
        """Clears the chat from bot messages"""
        async with ctx.typing():

            def check(message: nextcord.Message):
                return bool(
                    message.author.bot
                    or message.content.lower().startswith(BOT_PREFIXES)
                )

            await ctx.message.delete()
            deleted_messages = await ctx.channel.purge(limit=amount, check=check)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"{len(deleted_messages)} messages cleaned!",
                value="This message wil delete itself after 5 seconds",
                inline=False,
            )
        await ctx.send(embed=embed, delete_after=5)
        await logger(
            ctx,
            f"{len(deleted_messages)} messages have been cleaned from {ctx.message.channel.name}",
        )

    @commands.command(name="kick")
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def kick(self, ctx: Context, user: nextcord.Member, *, reason=None):
        """Kicks a user from the server"""
        reason2 = f" because of {reason}" if reason else ""
        await user.kick(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User kicked!",
            value=f"{user} has been kicked by {ctx.author}{reason2}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(
            ctx,
            f"{user} has been kick by {ctx.author}{reason2}",
        )

    @commands.command(name="ban")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def ban(self, ctx: Context, user: nextcord.Member, *, reason=None):
        """Bans a user from the server"""
        reason2 = f" because of {reason}" if reason else ""
        await user.ban(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User banned!",
            value=f"{user} has been banned by {ctx.author}{reason2}\nUse `.unban {user}` to unban {user}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(
            ctx,
            f"{user} has been banned by {ctx.author}{reason2}",
        )

    @commands.command(name="unban")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def unban(self, ctx: Context, user: str, *, reason=None):
        """Unbans a user from the server"""
        reason2 = f" because of {reason}" if reason else ""
        user = await commands.converter.UserConverter().convert(ctx, user)
        embed = nextcord.Embed(color=0x0DD91A)
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason=reason)
            embed.add_field(
                name="User unbanned!",
                value=f"{user} has been unbanned by {ctx.author}{reason2}",
                inline=False,
            )
            await logger(
                ctx,
                f"{user} has been unbanned by {ctx.author}{reason2}",
            )
        else:
            embed.add_field(
                name="Unbanning failed!",
                value=f"{user} is not banned!",
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.group(name="warn", invoke_without_command=True)
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def warn(
        self,
        ctx: Context,
        user: nextcord.Member,
        amount: int = 1,
        *,
        reason: str = None,
    ):
        """Warns someone"""
        await warn_system(ctx, user, amount, ctx.author, reason)
        await logger(
            ctx,
            f"{user} has been warned {amount}x by {ctx.author} {reason}",
        )

    @warn.command(name="remove")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_warn(
        self,
        ctx: Context,
        user: nextcord.Member,
        amount: int = 1,
        *,
        reason=None,
    ):
        """Removes a warn from someone"""
        reason2 = f"because of {reason}" if reason else ""
        query = {"_id": user.id}
        if USER_DATA.count_documents(query) == 0:
            post = {"_id": user.id, "warns": 0}
            USER_DATA.insert_one(post)
        else:
            user2 = USER_DATA.find_one(query)
            if "warns" in user2:
                warns = user2["warns"]
            warns2 = warns
            warns = warns - amount
            if warns < 0:
                warns = 0
                amount = 0 + warns2
            USER_DATA.update_one({"_id": user.id}, {"$set": {"warns": warns}})
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{user} now has {amount} warn(s) less {reason2}!",
            value=f"{user} now has a total of {warns} warn(s)!",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(ctx, f"{amount} warn(s) have been removed from {user}")

    @warn.command(name="list")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def list_warn(self, ctx: Context):
        """Lists the warn points of everyone that received at least 1"""
        embed = nextcord.Embed(color=0x0DD91A)
        for user in USER_DATA.find():
            if "warns" in user:
                warns = user["warns"]
                user = self.bot.get_user(int(user["_id"]))
                if warns != 0:
                    embed.add_field(
                        name=f"{user} has",
                        value=f"{warns} warns",
                        inline=False,
                    )
        if embed.fields == 0:
            embed = nextcord.Embed(color=0x0DD91A, title="Nobody has warns!")
        await ctx.send(embed=embed)

    @warn.command(name="get")
    async def get_warn(self, ctx: Context):
        """Sends your warn points"""
        user = USER_DATA.find_one({"_id": ctx.author.id})
        if "warns" in user:
            warns = user["warns"]
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"You ({ctx.author}) have {warns} warn(s)!",
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"You ({ctx.author}) have 0 warns!",
            )
        await ctx.send(embed=embed)

    @commands.command(name="role-info", aliases=["ri"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def role_info(self, ctx: Context, role: nextcord.Role):
        """Show information about a role"""
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Here is information about the {role.name} role"
        )
        embed.add_field(name="Role name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(
            name="Role color",
            value="#" + hex(role._colour).replace("0x", "").upper(),
            inline=True,
        )
        embed.add_field(
            name="Users with this role", value=len(role.members), inline=True
        )
        permissions = ", ".join(name for name, value in role.permissions if value)
        embed.add_field(
            name="Role permissions", value=permissions or "None", inline=True
        )
        await ctx.send(embed=embed)

    @commands.command(name="server-info", aliases=["si"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def server_info(self, ctx: Context, guild_id: int = None):
        """Show information about a server"""
        guild_id = guild_id or ctx.guild.id
        guild = self.bot.get_guild(guild_id)
        if guild is not None:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Here is information about the {guild.name} server",
            )
            if guild.icon:
                embed.set_thumbnail(url=guild.icon)
            embed.add_field(name="Server name", value=guild.name, inline=True)
            embed.add_field(name="Server ID", value=guild.id, inline=True)
            if guild.owner.name == guild.owner:
                embed.add_field(name="Owner", value=guild.owner, inline=True)
            else:
                embed.add_field(
                    name="Owner",
                    value=f"{guild.owner} ({guild.owner.name})",
                )
            embed.add_field(name="Total members", value=len(guild.members), inline=True)
            embed.add_field(name="Total humans", value=len(guild.humans), inline=True)
            embed.add_field(name="Total bots", value=len(guild.bots), inline=True)
            embed.add_field(name="Total roles", value=len(guild.roles), inline=True)
            try:
                bans = 0
                for _ in await guild.bans():
                    bans += 1
                embed.add_field(name="Total bans", value=bans, inline=True)
            except nextcord.Forbidden:
                pass
        else:
            embed = nextcord.Embed(color=0xFFC800, title="I can not access that guild!")
        await ctx.send(embed=embed)

    @commands.command(name="user-info", aliases=["ui"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def user_info(self, ctx: Context, user: nextcord.Member = None):
        """Show information about a user"""
        user = user or ctx.author
        if user is not None:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Here is information for {user.name}"
            )
            if user.avatar:
                embed.set_thumbnail(url=user.display_avatar)
            embed.add_field(name="Name", value=user, inline=True)
            if user.nick:
                embed.add_field(name="Nickname", value=user.nick, inline=True)
            embed.add_field(name="ID", value=user.id, inline=True)
            embed.add_field(
                name="Account created at",
                value=user.created_at.strftime("%d %b %Y"),
                inline=True,
            )
            embed.add_field(
                name=f"Joined {user.guild.name} at",
                value=user.joined_at.strftime("%d %b %Y"),
                inline=True,
            )
            if user.timeout:
                embed.add_field(name="Timeout", value=user.timeout, inline=True)
            embed.add_field(name="Top role", value=user.top_role.mention, inline=True)
            roles_list: list = user.roles
            roles_list.reverse()
            roles = ", ".join(role.mention for role in roles_list)
            embed.add_field(name="Roles", value=roles, inline=True)
            public_flags_list: list = user.public_flags.all()
            if public_flags_list:
                public_flags = ", ".join(flag.name for flag in public_flags_list)
                embed.add_field(name="Public flags", value=public_flags, inline=True)
            embed.add_field(
                name="In mutual guilds", value=len(user.mutual_guilds), inline=True
            )
            messages = USER_DATA.find_one({"_id": user.id})["messages"] or 0
            warns = USER_DATA.find_one({"_id": user.id})["warns"] or 0
            embed.add_field(name="Messages sent", value=messages, inline=True)
            embed.add_field(name="Total warns", value=warns, inline=True)
            if user.guild_permissions:
                permissions = ", ".join(
                    name for name, value in user.guild_permissions if value
                )
                embed.add_field(
                    name="Permissions in guild", value=permissions, inline=True
                )
            await ctx.send(embed=embed, view=profile_picture(user.display_avatar.url))
        else:
            embed = nextcord.Embed(color=0xFFC800, title="I can not acces that user!")
            await ctx.send(embed=embed)

    @commands.command(name="slowmode", aliases=["slow", "sm"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def slowmode(
        self, ctx: Context, time: str, channel: nextcord.TextChannel = None
    ):
        """Enables slowmode for a channel"""
        if channel is None:
            channel = ctx.channel
        time_seconds = int(humanfriendly.parse_timespan(time))
        time = humanfriendly.format_timespan(time_seconds)
        if time_seconds <= 21600:
            await channel.edit(slowmode_delay=time_seconds)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Set the slowmode for the {channel.name} channel to {time}",
            )
            await logger(
                ctx,
                f"The slowmode for the {channel.name} channel has been set to {time}",
            )
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="The limit for slowmode is 6 hours"
            )
        await ctx.send(embed=embed)

    @commands.group(name="pingpoll", invoke_without_command=True, aliases=["pp"])
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def pingpoll(self, ctx: Context):
        """Modify the roles used in Ping Poll"""
        await ctx.send_help("pingpoll")

    @pingpoll.command(name="add")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def add_pingpoll(self, ctx: Context, role: nextcord.Role):
        """Add roles used in Ping Poll"""
        pingpolls = list(BOT_DATA.find_one()["pingpolls"])
        if role.id not in pingpolls:
            pingpolls.append(role.id)
            BOT_DATA.update_one(
                {},
                {"$set": {"pingpolls": pingpolls}},
                upsert=False,
            )
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Role `{role.name}` added to PingPolls!"
            )
            await logger(ctx, f"Role `{role.name}` added to PingPolls!")
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"Role `{role.name}` is already in PingPolls!"
            )
        await ctx.send(embed=embed)

    @pingpoll.command(name="remove")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def remove_pingpoll(self, ctx: Context, role: nextcord.Role):
        """Remove roles used in Ping Poll"""
        pingpolls = list(BOT_DATA.find_one()["pingpolls"])
        if role.id in pingpolls:
            pingpolls.remove(role.id)
            BOT_DATA.update_one(
                {},
                {"$set": {"pingpolls": pingpolls}},
                upsert=False,
            )
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Role `{role.name}` is removed from PingPolls"
            )
            await logger(ctx, f"Role `{role.name}` is removed from PingPolls")
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{role.name}` is not in PingPolls"
            )
        await ctx.send(embed=embed)

    @pingpoll.command(name="list")
    @commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def list_pingpoll(self, ctx: Context):
        """List the roles used in Ping Poll"""
        if pingpolls := list(BOT_DATA.find_one()["pingpolls"]):
            pingpolls2 = ""
            for pingpoll in pingpolls:
                if nextcord.utils.get(ctx.guild.roles, id=pingpoll):
                    pingpolls2 = (
                        pingpolls2
                        + "\n> "
                        + nextcord.utils.get(ctx.guild.roles, id=pingpoll).name
                    )
            if not pingpolls2:
                embed = nextcord.Embed(color=0xFFC800, title="There are no PingPolls!")
            else:
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name="The current PingPolls are",
                    value=pingpolls2,
                    inline=False,
                )
        else:
            embed = nextcord.Embed(color=0xFFC800, title="There are no PingPolls!")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))

from contextlib import suppress
import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
import nextcord.ext.application_checks as checks
from views.buttons.button_roles import button_roles
from views.buttons.change_name_back import ChangeNameBack
from views.buttons.link import link_button
from views.modals.button_roles import ButtonRolesModal

from main import (
    USER_DATA,
    logger,
    warn_system,
    SLASH_GUILDS,
    BOT_DATA,
    bl,
)

BOT_PREFIXES = tuple(BOT_DATA.find_one()["botprefixes"])


class admin_slash(commands.Cog, name="Admin Slash Commands"):
    """Slash commands for admins"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(button_roles(bot=self.bot))
        self.bot.add_view(ChangeNameBack(None, None))
        self.bot.add_modal(ButtonRolesModal(None))

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def buttonroles(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @buttonroles.subcommand(name="send", inherit_hooks=True)
    async def send_buttonroles(
        self,
        interaction: Interaction,
        custom_text: bool = SlashOption(
            description="Set to True if you want custom text",
            required=False,
            default=False,
        ),
    ):
        """Sends a message with buttons where people can get roles"""
        buttonroles_id = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            bool(nextcord.utils.get(interaction.guild.roles, id=buttonrole))
            for buttonrole in buttonroles_id
        )

        if roles > 0:
            if custom_text:
                await interaction.response.send_modal(
                    ButtonRolesModal(button_roles(guild=interaction.guild))
                )
                return
            embed = nextcord.Embed(
                color=0x0DD91A, title="Click a button to add/remove that role!"
            )
            await interaction.channel.send(
                embed=embed, view=button_roles(guild=interaction.guild)
            )
            embed = nextcord.Embed(color=0x0DD91A, title="The message has been sent!")
        else:
            embed = nextcord.Embed(
                color=0xFFC800,
                title="There are no button roles!\nMake sure to add them by using `.buttonroles add <role>`",
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(name="add", inherit_hooks=True)
    async def add_buttonroles(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(description="The role to add", required=True),
    ):
        """Add a button role"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(interaction.guild.roles, id=buttonrole)
        )

        if roles >= 25:
            embed = nextcord.Embed(
                color=0xFFC800, title="You can only add 25 button roles!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
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
            await logger(
                interaction, f'The "{role.name}" role has been added to buttonroles'
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is already listed!'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(name="remove", inherit_hooks=True)
    async def remove_buttonroles(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to remove", required=True
        ),
    ):
        """Remove a button role"""
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
                interaction, f'The "{role.name}" role has been removed from buttonroles'
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is not listed!'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(name="list", inherit_hooks=True)
    async def list_buttonroles(self, interaction: Interaction):
        """List all button roles"""
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(interaction.guild.roles, id=buttonrole)
        )
        if roles > 0:
            buttonroles2 = ""
            for buttonrole in buttonroles:
                if nextcord.utils.get(interaction.guild.roles, id=buttonrole):
                    buttonroles2 = (
                        buttonroles2
                        + "\n> "
                        + nextcord.utils.get(
                            interaction.guild.roles, id=buttonrole
                        ).name
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

        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def shutdown(self, interaction: Interaction):
        """Shut down TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot was shut down",
            value=f"TIJK Bot was shut down by {interaction.user}",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)
        await logger(
            interaction,
            f"TIJK Bot was shut down by {interaction.user}",
        )
        info = await self.bot.application_info()
        owner = info.owner
        dm = await owner.create_dm()
        await dm.send(embed=embed)
        bl.info(f"TIJK Bot was shut down by {interaction.user}", __file__)
        await self.bot.close()

    @slash(guild_ids=SLASH_GUILDS)
    async def ping(
        self,
        interaction: Interaction,
        decimals: int = SlashOption(
            description="At how may decimals the latency should round",
            min_value=0,
            max_value=17,
            default=1,
        ),
    ):
        """Get the latency of TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        latency = round(self.bot.latency, decimals)
        embed.add_field(
            name="Pong!",
            value=f"The latency is {latency} seconds",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def readtherules(
        self,
        interaction: Interaction,
        rule_number: int = SlashOption(
            description="The rule number", min_value=1, required=True
        ),
        user: nextcord.Member = SlashOption(
            description="The user to tell to read the rules", required=False
        ),
        reason: str = SlashOption(
            description="The reason why the user is warned", required=False
        ),
        warn_user: bool = SlashOption(
            description="Wether to warn the user", required=False, default=True
        ),
    ):
        """Tell a user to read the rules"""
        channel = nextcord.utils.get(interaction.guild.channels, name="rules")
        messages = await channel.history(limit=50).flatten()
        messages.reverse()
        try:
            embed = nextcord.Embed(color=0x0DD91A)
            if user:
                embed.add_field(
                    name=f"Hey {user}, please read rule number {rule_number}!",
                    value=messages[rule_number - 1].content,
                    inline=False,
                )
                if warn_user:
                    embed.set_footer(text="You also received 1 warn!")
            else:
                embed.add_field(
                    name=f"Here is rule number {rule_number}:",
                    value=messages[rule_number - 1].content,
                    inline=False,
                )
            await interaction.response.send_message(embed=embed)
            if warn_user:
                await warn_system(interaction, user, 1, interaction.user, reason)
        except IndexError:
            embed = nextcord.Embed(
                color=0xFF0000, title=f"{rule_number} is not a valid rule number!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @checks.bot_has_permissions(moderate_members=True)
    async def mute(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to mute", required=True
        ),
        time: str = SlashOption(
            description="How long the user should be muted", required=True
        ),
        reason: str = SlashOption(
            description="The reason why the user was muted", required=False
        ),
    ):
        """Mute a user"""
        try:
            reason2 = f" because of {reason}" if reason else ""
            time = humanfriendly.parse_timespan(time)
            await user.timeout(
                nextcord.utils.utcnow() + datetime.timedelta(seconds=time)
            )
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="User muted!",
                value=f"{user} was muted for {humanfriendly.format_timespan(time)} by {interaction.user}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await logger(
                interaction,
                f"{user} was muted for {humanfriendly.format_timespan(time)} by {interaction.user}{reason2}",
            )
        except humanfriendly.InvalidTimespan:
            embed = nextcord.Embed(color=0xFFC800, title="Invalid time!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @checks.bot_has_permissions(moderate_members=True)
    async def unmute(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to unmute", required=True
        ),
        reason: str = SlashOption(
            description="The reason why the user was unmuted", required=False
        ),
    ):
        """Unmute a user"""
        reason2 = f" because of {reason}" if reason else ""
        await user.timeout(None)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User unmuted!",
            value=f"{user} was unmuted by {interaction.user}{reason2}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await logger(
            interaction,
            f"{user} was unmuted by {interaction.user}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @checks.bot_has_permissions(manage_nicknames=True)
    async def nick(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @nick.subcommand(name="set", inherit_hooks=True)
    async def nick_set(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user that should be nicked", required=True
        ),
        name: str = SlashOption(description="The new nickname", required=True),
    ):
        """Give a user a nickname"""
        ORIGINAL_NAME = user.display_name
        await user.edit(nick=name)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{ORIGINAL_NAME}'s nickname has been changed to {name}\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, ORIGINAL_NAME)
        )
        await logger(
            interaction, f"{ORIGINAL_NAME}'s nickname has been changed to {name}"
        )

    @nick.subcommand(name="reset", inherit_hooks=True)
    async def nick_reset(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(description="The user", required=True),
    ):
        """Reset a user's nickname"""
        ORIGINAL_NAME = user.display_name
        await user.edit(nick=None)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{ORIGINAL_NAME}'s nickname has been reset\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, ORIGINAL_NAME)
        )
        await logger(interaction, f"{ORIGINAL_NAME}'s nickname has been reset")

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def role(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @role.subcommand(name="assign", inherit_hooks=True)
    async def assign_role(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role that should be assigned", required=True
        ),
        user: nextcord.Member = SlashOption(
            description="The user that should be assigned to the role. Defaults to yourself",
            required=False,
        ),
        reason: str = SlashOption(
            description="The reason why the user was assigned the role", required=False
        ),
    ):
        """Give a user a role"""
        user = user or interaction.user
        if role not in user.roles:
            await user.add_roles(role, reason=reason)
            reason2 = f" because of {reason}" if reason else ""
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role assigned!",
                value=f"Role {role.mention} has been assigned to {user.mention} by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await logger(
                interaction,
                f"Role {role.mention} has been assigned to {user.mention} by {interaction.user.mention}",
            )
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Could not assign that role!",
                value=f"{user.mention} already has the {role.mention} role",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @role.subcommand(name="remove", inherit_hooks=True)
    async def remove_role(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role that should be remove", required=True
        ),
        user: nextcord.Member = SlashOption(
            description="The user where the role should be removed. Defaults to yourself",
            required=False,
        ),
        reason: str = SlashOption(
            description="The reason why the role was removed from the user",
            required=False,
        ),
    ):
        """Remove a role from a user"""
        user = user or interaction.user
        if role in user.roles:
            await user.remove_roles(role, reason=reason)
            reason2 = f" because of {reason}" if reason else ""
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role removed!",
                value=f"Role {role.mention} has been removed from {user.mention} by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await logger(
                interaction,
                f"Role {role.mention} has been removed from {user.mention} by {interaction.user.mention}",
            )

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Could not remove that role!",
                value=f"{user.mention} does not have the {role.mention} role!",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def clear(
        self,
        interaction: Interaction,
        amount: int = SlashOption(
            description="The amount of messages to clear", min_value=1, required=True
        ),
        channel: nextcord.abc.GuildChannel = SlashOption(
            description="The channel to clear messages from. Defaults to the current channel",
            channel_types=[nextcord.ChannelType.text],
            required=False,
        ),
    ):
        """Clear the chat"""
        channel: nextcord.TextChannel = channel or interaction.channel
        deleted_messages = await channel.purge(limit=amount, bulk=True)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{len(deleted_messages)} messages cleared!",
            value="This message wil delete itself after 10 seconds",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, delete_after=10)
        await logger(
            interaction,
            f"{len(deleted_messages)} messages have been cleared from {channel.mention}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def clean(
        self,
        interaction: Interaction,
        amount: int = SlashOption(
            description="The amount of messages to clear", min_value=1, required=True
        ),
        channel: nextcord.abc.GuildChannel = SlashOption(
            description="The channel to clear messages from",
            channel_types=[nextcord.ChannelType.text],
            required=False,
        ),
    ):
        """Clear the chat from bot messages"""

        def check(message: nextcord.Message):
            return bool(
                message.author.bot or message.content.lower().startswith(BOT_PREFIXES)
            )

        channel = channel or interaction.channel
        deleted_messages = await channel.purge(limit=amount, check=check)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"{len(deleted_messages)} messages cleaned!",
            value="This message wil delete itself after 10 seconds",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, delete_after=10)
        await logger(
            interaction,
            f"{len(deleted_messages)} messages have been cleaned from {channel.mention}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def kick(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to kick", required=True
        ),
        reason: str = SlashOption(
            description="The reason why the user was kicked", required=False
        ),
    ):
        """Kick a user from the server"""
        reason2 = f" because of {reason}" if reason else ""
        await user.kick(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User kicked!",
            value=f"{user} has been kicked by {interaction.user.mention}{reason2}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await logger(
            interaction,
            f"{user} has been kicked by {interaction.user.mention}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def ban(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to ban", required=True
        ),
        reason: str = SlashOption(
            description="The reason why the user was banned", required=False
        ),
    ):
        """Ban a user from the server"""
        reason2 = f" because of {reason}" if reason else ""
        await user.ban(reason=reason)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User banned!",
            value=f"{user} has been banned by {interaction.user.mention}{reason2}\nUse `.unban {user}` to unban",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await logger(
            interaction,
            f"{user} has been banned by {interaction.user.mention}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def unban(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="The user to unban", required=True),
        reason: str = SlashOption(
            description="The reason why the user was unbanned", required=False
        ),
    ):
        """Unban a user from the server"""
        try:
            user = await commands.converter.UserConverter().convert(interaction, user)
        except commands.UserNotFound:
            embed = nextcord.Embed(color=0xFFC800, title="User not found!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = nextcord.Embed(color=0x0DD91A)
        bans = tuple(ban_entry.user for ban_entry in await interaction.guild.bans())
        if user in bans:
            await interaction.guild.unban(user, reason=reason)
            reason2 = f" because of {reason}" if reason else ""
            embed.add_field(
                name="User unbanned!",
                value=f"{user} has been unbanned by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await logger(
                interaction,
                f"{user} has been unbanned by {interaction.user.mention}{reason2}",
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(color=0xFF0000, title=f"{user} is not banned!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def warn(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @warn.subcommand(name="add", inherit_hooks=True)
    async def add_warn(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to warn", required=True
        ),
        amount: int = SlashOption(
            description="The amount of warns to give. Defaults to 1",
            min_value=1,
            default=1,
            required=False,
        ),
        reason: str = SlashOption(
            description="The reason why the user was warned", required=False
        ),
    ):
        """Warn a user"""
        await warn_system(interaction, user, amount, interaction.user, reason)

    @warn.subcommand(name="remove", inherit_hooks=True)
    async def remove_warn(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to remove a warn from", required=True
        ),
        amount: int = SlashOption(
            description="The amount of warns to remove. Defaults to 1",
            min_value=1,
            default=1,
            required=False,
        ),
        reason: str = SlashOption(
            description="The reason why the user was warned", required=False
        ),
    ):
        """Remove a warn from a user"""
        await warn_system(interaction, user, amount, interaction.user, reason, True)

    @warn.subcommand(name="list", inherit_hooks=True)
    async def list_warn(self, interaction: Interaction):
        """List the warn points of everyone that received at least 1"""
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
        await interaction.response.send_message(embed=embed)

    @warn.subcommand(name="get")
    async def get_warn(self, interaction: Interaction):
        """Get your warns"""
        user = USER_DATA.find_one({"_id": interaction.user.id})
        warns = user["warns"] if "warns" in user else 0
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"You have {warns} warn(s)!",
        )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def info(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @info.subcommand(name="role", inherit_hooks=True)
    async def role_info(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to show info about", required=True
        ),
    ):
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
        await interaction.response.send_message(embed=embed)

    @info.subcommand(name="server", inherit_hooks=True)
    async def server_info(
        self,
        interaction: Interaction,
        server_id: str = SlashOption(
            description="The server to show info about. Defaults to the current server",
            required=False,
        ),
    ):
        """Show information about a server"""
        try:
            server_id = int(server_id)
        except ValueError:
            embed = nextcord.Embed(color=0xFFC800, title="Please put in a server ID!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        guild_id = server_id or interaction.guild.id
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
            with suppress(nextcord.Forbidden):
                bans = 0
                for _ in await guild.bans():
                    bans += 1
                embed.add_field(name="Total bans", value=bans, inline=True)
        else:
            embed = nextcord.Embed(color=0xFFC800, title="I can not access that guild!")
        await interaction.response.send_message(embed=embed)

    @info.subcommand(name="user", inherit_hooks=True)
    async def user_info(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to show information about. Defaults to yourself",
            required=False,
        ),
    ):
        """Show information about a user"""
        user = user or interaction.user
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
        if user._timeout:
            embed.add_field(
                name="Timed out until",
                value=user._timeout.strftime("%H:%M:%S %d %b %Y"),
                inline=True,
            )
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
            embed.add_field(name="Permissions in guild", value=permissions, inline=True)
        await interaction.response.send_message(
            embed=embed,
            view=link_button(user.display_avatar.url, "Download profile picture"),
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def slowmode(
        self,
        interaction: Interaction,
        time: str = SlashOption(
            description="How long the slowmode should be. Use 0 to turn off",
            required=True,
        ),
        channel: nextcord.abc.GuildChannel = SlashOption(
            description="The channel to set a slowmode for. Defaults to the current channel",
            channel_types=[nextcord.ChannelType.text],
            required=False,
        ),
    ):
        """Enable slowmode for a channel"""
        if any(
            time.lower() == option for option in ("reset", "off", "disable", "disabled")
        ):
            time = "0"
        try:
            time_seconds = int(humanfriendly.parse_timespan(time))
        except humanfriendly.InvalidTimespan:
            embed = nextcord.Embed(color=0xFFC800, title="Invalid time!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        channel = channel or interaction.channel
        time = humanfriendly.format_timespan(time_seconds)
        if time_seconds <= 21600:
            await channel.edit(slowmode_delay=time_seconds)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Set the slowmode for the {channel.name} channel to {time}",
            )
            await logger(
                interaction,
                f"The slowmode for the {channel.name} channel has been set to {time}",
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="The limit for slowmode is 6 hours"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def pingpoll(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @pingpoll.subcommand(name="add", inherit_hooks=True)
    async def add_pingpoll(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to add to Ping Poll", required=True
        ),
    ):
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
            await interaction.response.send_message(embed=embed)
            await logger(interaction, f"Role `{role.name}` added to PingPolls!")
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"Role `{role.name}` is already in PingPolls!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @pingpoll.subcommand(name="remove", inherit_hooks=True)
    async def remove_pingpoll(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to remove from Ping Poll", required=True
        ),
    ):
        """Remove roles used from Ping Poll"""
        pingpolls = list(BOT_DATA.find_one()["pingpolls"])
        if role.id in pingpolls:
            pingpolls.remove(role.id)
            BOT_DATA.update_one(
                {},
                {"$set": {"pingpolls": pingpolls}},
                upsert=False,
            )
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Role `{role.name}` removed from PingPolls!"
            )
            await interaction.response.send_message(embed=embed)
            await logger(interaction, f"Role `{role.name}` is removed from PingPolls")
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"Role `{role.name}` is not in PingPolls!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @pingpoll.subcommand(name="list", inherit_hooks=True)
    async def list_pingpoll(self, interaction: Interaction):
        """List roles used in Ping Poll"""
        if pingpolls := list(BOT_DATA.find_one()["pingpolls"]):
            pingpolls2 = ""
            for pingpoll in pingpolls:
                if nextcord.utils.get(interaction.guild.roles, id=pingpoll):
                    pingpolls2 = (
                        pingpolls2
                        + "\n> "
                        + nextcord.utils.get(interaction.guild.roles, id=pingpoll).name
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
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(admin_slash(bot))

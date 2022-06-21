import datetime
from contextlib import suppress

from humanfriendly import parse_timespan, format_timespan, InvalidTimespan
import nextcord
import nextcord.ext.application_checks as checks
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from views.buttons.button_roles import ButtonRoles
from views.buttons.change_name_back import ChangeNameBack
from views.buttons.link import Link
from views.modals.button_roles import ButtonRolesModal

from slash.custom_checks import (
    check_bot_owner,
    check_server_owner,
    is_admin,
    is_mod,
    is_server_owner,
)

from main import (
    SLASH_GUILDS,
    USER_DATA,
    get_bot_data,
    get_user_data,
    log,
    logger,
    set_bot_data,
    warn_system,
)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ButtonRoles(bot=self.bot))
        self.bot.add_modal(ButtonRolesModal(None))

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
        buttonroles_id = get_bot_data("buttonroles")
        roles = sum(
            bool(nextcord.utils.get(interaction.guild.roles, id=buttonrole))
            for buttonrole in buttonroles_id
        )

        if roles > 0:
            if custom_text:
                await interaction.response.send_modal(
                    ButtonRolesModal(ButtonRoles(guild=interaction.guild))
                )
                return
            embed = nextcord.Embed(
                color=0x0DD91A, title="Click a button to add/remove that role!"
            )
            await interaction.channel.send(
                embed=embed, view=ButtonRoles(guild=interaction.guild)
            )
            embed = nextcord.Embed(color=0x0DD91A, title="The message has been sent!")
        else:
            embed = nextcord.Embed(
                color=0xFFC800,
                title="There are no button roles!\nMake sure to add them by using `/buttonroles add <role>`",
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(name="add", inherit_hooks=True)
    async def add_buttonroles(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(description="The role to add", required=True),
    ):
        """Add a button role"""
        buttonroles = get_bot_data("buttonroles")
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
            set_bot_data("buttonroles", buttonroles)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f'The "{role.name}" role has been added!\nMake sure to use `/buttonroles send` again!',
            )
            await log(
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
        buttonroles = get_bot_data("buttonroles")
        if role.id in buttonroles:
            buttonroles.remove(role.id)
            set_bot_data("buttonroles", buttonroles)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f'The "{role.name}" role has been removed!\nMake sure to use `/buttonroles send` again!',
            )
            await log(
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
        buttonroles = get_bot_data("buttonroles")
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
    @is_server_owner()
    async def shutdown(self, interaction: Interaction):
        """Shut down TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot was shut down",
            value=f"TIJK Bot was shut down by {interaction.user}",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)
        await log(
            interaction,
            f"TIJK Bot was shut down by {interaction.user}",
        )
        info = await self.bot.application_info()
        await info.owner.dm_channel.send(embed=embed)
        logger.info("TIJK Bot was shut down by %s", interaction.user)
        await self.bot.close()

    @slash(guild_ids=SLASH_GUILDS)
    @is_mod()
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
    @is_mod()
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
            description="Whether to warn the user", required=False, default=True
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
        except IndexError:
            embed = nextcord.Embed(
                color=0xFF0000, title=f"{rule_number} is not a valid rule number!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @is_mod()
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
            time = parse_timespan(time)
            await user.timeout(
                nextcord.utils.utcnow() + datetime.timedelta(seconds=time)  # type: ignore[arg-type]
            )
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="User muted!",
                value=f"{user} was muted for {format_timespan(time)} by {interaction.user}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await log(
                interaction,
                f"{user} was muted for {format_timespan(time)} by {interaction.user}{reason2}",
            )
        except InvalidTimespan:
            embed = nextcord.Embed(color=0xFFC800, title="Invalid time!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @is_mod()
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
        await user.timeout(None)  # type: ignore[arg-type]
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User unmuted!",
            value=f"{user} was unmuted by {interaction.user}{reason2}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await log(
            interaction,
            f"{user} was unmuted by {interaction.user}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
        original_name = user.display_name
        await user.edit(nick=name)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{original_name}'s nickname has been changed to {name}\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, original_name)
        )
        await log(interaction, f"{original_name}'s nickname has been changed to {name}")

    @nick.subcommand(name="reset", inherit_hooks=True)
    async def nick_reset(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(description="The user", required=True),
    ):
        """Reset a user's nickname"""
        original_name = user.display_name
        await user.edit(nick=None)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{original_name}'s nickname has been reset\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, original_name)
        )
        await log(interaction, f"{original_name}'s nickname has been reset")

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
            mod_role = nextcord.utils.get(interaction.guild.roles, name="Moderator")
            admin_role = nextcord.utils.get(interaction.guild.roles, name="Admin")
            owner_role = nextcord.utils.get(interaction.guild.roles, name="Owner")
            admin_roles = (mod_role, admin_role, owner_role)
            if (
                not check_server_owner(interaction)
                or not await check_bot_owner(interaction)
            ) and role in admin_roles:
                embed = nextcord.Embed(
                    color=0xFFC800, title="You cannot give an admin role!"
                )
                await interaction.response.send_message(embed=embed)
                server_owner = interaction.guild.owner
                embed = nextcord.Embed(
                    color=0xFFC800,
                    title=f"{interaction.user} tried to give an admin role ({role.name}) to {user}",
                )
                await server_owner.dm_channel.send(embed=embed)
                return
            await user.add_roles(role, reason=reason)  # type: ignore[arg-type]
            reason2 = f" because of {reason}" if reason else ""
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role assigned!",
                value=f"Role {role.mention} has been assigned to {user.mention} by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await log(
                interaction,
                f"Role {role.name} has been assigned to {user} by {interaction.user}{reason2}",
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
            mod_role = nextcord.utils.get(interaction.guild.roles, name="Moderator")
            admin_role = nextcord.utils.get(interaction.guild.roles, name="Admin")
            owner_role = nextcord.utils.get(interaction.guild.roles, name="Owner")
            admin_roles = (mod_role, admin_role, owner_role)
            if (
                not check_server_owner(interaction)
                or not await check_bot_owner(interaction)
            ) and role in admin_roles:
                embed = nextcord.Embed(
                    color=0xFFC800, title="You cannot remove an admin role!"
                )
                await interaction.response.send_message(embed=embed)
                server_owner = interaction.guild.owner
                embed = nextcord.Embed(
                    color=0xFFC800,
                    title=f"{interaction.user} tried to remove an admin role ({role.name}) from {user}",
                )
                await server_owner.dm_channel.send(embed=embed)
                return
            await user.remove_roles(role, reason=reason)  # type: ignore[arg-type]
            reason2 = f" because of {reason}" if reason else ""
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Role removed!",
                value=f"Role {role.mention} has been removed from {user.mention} by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            await log(
                interaction,
                f"Role {role.name} has been removed from {user} by {interaction.user}{reason2}",
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
    @is_mod()
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
        await log(
            interaction,
            f"{len(deleted_messages)} messages have been cleared from {channel.name}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
                message.author.bot
                or message.content.lower().startswith(get_bot_data("botprefixes"))
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
        await log(
            interaction,
            f"{len(deleted_messages)} messages have been cleaned from {channel.name}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
        await log(
            interaction,
            f"{user} has been kicked by {interaction.user}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_server_owner()
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
            value=f"{user} has been banned by {interaction.user.mention}{reason2}\nUse `/unban {user}` to unban",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await log(
            interaction,
            f"{user} has been banned by {interaction.user}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_server_owner()
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
        bans = tuple(
            ban_entry.user.id
            for ban_entry in await interaction.guild.bans(limit=None).flatten()
        )
        if user.id in bans:
            await interaction.guild.unban(user, reason=reason)  # type: ignore[arg-type]
            reason2 = f" because of {reason}" if reason else ""
            embed.add_field(
                name="User unbanned!",
                value=f"{user} has been unbanned by {interaction.user.mention}{reason2}",
                inline=False,
            )
            await log(
                interaction,
                f"{user} has been unbanned by {interaction.user}{reason2}",
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(color=0xFF0000, title=f"{user} is not banned!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @is_mod()
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
        await warn_system(interaction, user, amount, str(interaction.user), reason)

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
        await warn_system(
            interaction, user, amount, str(interaction.user), reason, True
        )

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
        warns = get_user_data(interaction.user.id, "warns")
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"You have {warns} warn(s)!",
        )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
            value="#" + hex(role.color.value).replace("0x", "").upper(),
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
        guild_id = server_id or interaction.guild.id
        try:
            guild_id = int(guild_id)
        except ValueError:
            embed = nextcord.Embed(color=0xFFC800, title="Please put in a server ID!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
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
        if user.communication_disabled_until:
            embed.add_field(
                name="Timed out until",
                value=user.communication_disabled_until.strftime("%H:%M:%S %d %b %Y"),
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
        embed.add_field(
            name="Messages sent", value=get_user_data(user.id, "messages"), inline=True
        )
        embed.add_field(
            name="Total warns", value=get_user_data(user.id, "warns"), inline=True
        )
        if user.guild_permissions:
            permissions = ", ".join(
                name for name, value in user.guild_permissions if value
            )
            embed.add_field(name="Permissions in guild", value=permissions, inline=True)
        await interaction.response.send_message(
            embed=embed,
            view=Link(user.display_avatar.url, "Download profile picture"),
        )

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
            time_seconds = int(parse_timespan(time))
        except InvalidTimespan:
            embed = nextcord.Embed(color=0xFFC800, title="Invalid time!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        channel: nextcord.TextChannel = channel or interaction.channel
        time = format_timespan(time_seconds)
        if time_seconds <= 21600:
            await channel.edit(slowmode_delay=time_seconds)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Set the slowmode for the {channel.name} channel to {time}",
            )
            await log(
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
    @is_admin()
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
        pingpolls = get_bot_data("pingpolls")
        if role.id not in pingpolls:
            pingpolls.append(role.id)
            set_bot_data("pingpolls", pingpolls)
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Role `{role.name}` added to PingPolls!"
            )
            await interaction.response.send_message(embed=embed)
            await log(interaction, f"Role `{role.name}` added to PingPolls!")
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
        pingpolls = get_bot_data("pingpolls")
        if role.id in pingpolls:
            pingpolls.remove(role.id)
            set_bot_data("pingpolls", pingpolls)
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Role `{role.name}` removed from PingPolls!"
            )
            await interaction.response.send_message(embed=embed)
            await log(interaction, f"Role `{role.name}` is removed from PingPolls")
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"Role `{role.name}` is not in PingPolls!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @pingpoll.subcommand(name="list", inherit_hooks=True)
    async def list_pingpoll(self, interaction: Interaction):
        """List roles used in Ping Poll"""
        if pingpolls := get_bot_data("pingpolls"):
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
    bot.add_cog(Admin(bot))

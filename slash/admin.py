import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
import nextcord.ext.application_checks as checks
from views.buttons.button_roles import button_roles
from views.buttons.change_name_back import ChangeNameBack
from views.modals.button_roles import ButtonRolesModal

from main import (
    interaction_logger as ilogger,
    warn_system,
    SLASH_GUILDS,
    BOT_DATA,
    bl,
)


class admin_slash(
    commands.Cog, name="Admin Slash Commands", description="Slash commands for admins"
):
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

    @buttonroles.subcommand(
        name="send",
        description="Sends a message with buttons where people can get roles",
        inherit_hooks=True,
    )
    async def send_buttonroles(
        self,
        interaction: Interaction,
        custom_text: bool = SlashOption(
            description="Set to True if you want custom text",
            required=False,
            default=False,
        ),
    ):
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
            else:
                embed = nextcord.Embed(
                    color=0x0DD91A, title="Click a button to add/remove that role!"
                )
                await interaction.channel.send(
                    embed=embed, view=button_roles(guild=interaction.guild)
                )
                embed = nextcord.Embed(
                    color=0x0DD91A, title="The message has been sent!"
                )
        else:
            embed = nextcord.Embed(
                color=0xFFC800,
                title="There are no button roles!\nMake sure to add them by using `.buttonroles add <role>`",
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(
        name="add", description="Add a button role", inherit_hooks=True
    )
    async def add_buttonroles(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(description="The role to add", required=True),
    ):
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
            await ilogger(
                interaction, f'The "{role.name}" role has been added to buttonroles'
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is already listed!'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(
        name="remove", description="Remove a button role", inherit_hooks=True
    )
    async def remove_buttonroles(
        self,
        interaction: Interaction,
        role: nextcord.Role = SlashOption(
            description="The role to remove", required=True
        ),
    ):
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
            await ilogger(
                interaction, f'The "{role.name}" role has been removed from buttonroles'
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f'The "{role.name}" role is not listed!'
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @buttonroles.subcommand(
        name="list", description="Lists all button roles", inherit_hooks=True
    )
    async def list_buttonroles(self, interaction: Interaction):
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

    @slash(description="Shuts down TIJK Bot", guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def shutdown(self, interaction: Interaction):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot was shut down",
            value=f"TIJK Bot was shut down by {interaction.user}",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)
        await ilogger(
            interaction,
            f"TIJK Bot was shut down by {interaction.user}",
        )
        info = await self.bot.application_info()
        owner = info.owner
        dm = await owner.create_dm()
        await dm.send(embed=embed)
        bl.info(f"TIJK Bot was shut down by {interaction.user}", __file__)
        await self.bot.close()

    @slash(description="Get the latency of TIJK Bot", guild_ids=SLASH_GUILDS)
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
        embed = nextcord.Embed(color=0x0DD91A)
        latency = round(self.bot.latency, decimals)
        embed.add_field(
            name="Pong!",
            value=f"The latency is {latency} seconds",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @slash(description="Tell a user to read the rules", guild_ids=SLASH_GUILDS)
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
                    await warn_system(interaction, user, 1, interaction.user, reason)
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

    @slash(description="Mute a user", guild_ids=SLASH_GUILDS)
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
            await ilogger(
                interaction,
                f"{user} was muted for {humanfriendly.format_timespan(time)} by {interaction.user}{reason2}",
            )
        except humanfriendly.InvalidTimespan:
            embed = nextcord.Embed(color=0xFFC800, title="Invalid time!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(description="Unmute a user", guild_ids=SLASH_GUILDS)
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
        reason2 = f" because of {reason}" if reason else ""
        await user.timeout(None)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="User unmuted!",
            value=f"{user} was unmuted by {interaction.user}{reason2}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await ilogger(
            interaction,
            f"{user} was unmuted by {interaction.user}{reason2}",
        )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    @checks.bot_has_permissions(manage_nicknames=True)
    async def nick(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @nick.subcommand(description="Gives a user a nickname", inherit_hooks=True)
    async def set(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="The user that should be nicked", required=True
        ),
        name: str = SlashOption(description="The new nickname", required=True),
    ):
        ORIGINAL_NAME = user.display_name
        await user.edit(nick=name)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{ORIGINAL_NAME}'s nickname has been changed to {name}\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, ORIGINAL_NAME)
        )
        await ilogger(
            interaction, f"{ORIGINAL_NAME}'s nickname has been changed to {name}"
        )

    @nick.subcommand(description="Resets a users nickname", inherit_hooks=True)
    async def reset(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(description="The user", required=True),
    ):
        ORIGINAL_NAME = user.display_name
        await user.edit(nick=None)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"{ORIGINAL_NAME}'s nickname has been reset\nClick the button below to change the name back",
        )
        await interaction.response.send_message(
            embed=embed, view=ChangeNameBack(user, ORIGINAL_NAME)
        )
        await ilogger(interaction, f"{ORIGINAL_NAME}'s nickname has been reset")

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def role(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @role.subcommand(
        name="assign", description="Give a user a role", inherit_hooks=True
    )
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
            await ilogger(
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


def setup(bot):
    bot.add_cog(admin_slash(bot))

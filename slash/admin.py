import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
import nextcord.ext.application_checks as checks
from views.button_roles import button_roles

from main import (
    interaction_logger as ilogger,
    logger,
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
        text: str = SlashOption(
            description="Text that will be used with the message",
            required=False,
            default="Click a button to add/remove that role!",
        ),
    ):
        buttonroles = BOT_DATA.find_one()["buttonroles"]
        roles = sum(
            1
            for buttonrole in buttonroles
            if nextcord.utils.get(interaction.guild.roles, id=buttonrole)
        )
        if roles > 0:
            embed = nextcord.Embed(color=0x0DD91A, title="The message has been sent!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            embed = nextcord.Embed(color=0x0DD91A, title=text)

            await interaction.channel.send(
                embed=embed, view=button_roles(guild=interaction.guild)
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


def setup(bot):
    bot.add_cog(admin_slash(bot))

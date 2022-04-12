import subprocess
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
import nextcord.ext.application_checks as checks
from nextcord.ext.commands.errors import *  # noqa F403
import os
import sys
import datetime
import time

from main import USER_DATA, logger, SLASH_GUILDS, START_TIME
import basic_logger as bl


class developer_slash(commands.Cog, name="Developer Slash Commands"):
    """Slash commands for developers"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def embed(
        self,
        interaction: Interaction,
        title: str = SlashOption(
            name="title", description="The title of the embed", required=False
        ),
        color: int = SlashOption(
            name="color",
            description="The color of the embed",
            choices={"green": 0x0DD91A, "orange": 0xFFC800, "red": 0xFF0000},
            required=False,
        ),
        name1: str = SlashOption(
            name="name1", description="The name of the 1st field", required=False
        ),
        value1: str = SlashOption(
            name="value1", description="The value of the 1st field", required=False
        ),
        name2: str = SlashOption(
            name="name2", description="The name of the 2nd field", required=False
        ),
        value2: str = SlashOption(
            name="value2", description="The value of the 2nd field", required=False
        ),
        name3: str = SlashOption(
            name="name3", description="The name of the 3d field", required=False
        ),
        value3: str = SlashOption(
            name="value3", description="The value of the 3d field", required=False
        ),
    ):
        """Generate an embed"""
        try:
            if not color:
                color = 0x0DD91A
            if title:
                embed = nextcord.Embed(color=color, title=title)
            else:
                embed = nextcord.Embed(color=color)
            if name1 and value1:
                embed.add_field(
                    name=name1,
                    value=value1,
                    inline=False,
                )
            if name2 and value2:
                embed.add_field(
                    name=name2,
                    value=value2,
                    inline=False,
                )
            if name3 and value3:
                embed.add_field(
                    name=name3,
                    value=value3,
                    inline=False,
                )
            await interaction.response.send_message(embed=embed)
        except nextcord.errors.HTTPException:
            await interaction.response.send_message(
                "The embed is invalid", ephemeral=True
            )

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def restart(self, interaction: nextcord.Interaction):
        """Restart TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot is restarting...",
            value=f"TIJK Bot was restarted by {interaction.user}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await logger(
            interaction,
            f"TIJK Bot was restarted by {interaction.user}",
            interaction.channel.name,
        )
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.playing, name="Restarting..."
            )
        )
        command = "cls" if os.name in ("nt", "dos") else "clear"
        subprocess.call(command, shell=False)
        os.execv(sys.executable, ["python"] + sys.argv)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def status(
        self,
        interaction: Interaction,
    ):
        """This will never get called since it has subcommands"""
        pass

    @status.subcommand(name="set", inherit_hooks=True)
    async def set_status(
        self,
        interaction: Interaction,
        type: str = SlashOption(
            description="The type of status",
            choices=[
                "watching",
                "playing",
                "streaming",
                "listening",
                "competing",
            ],
            required=True,
        ),
        text: str = SlashOption(
            description="The text that will show up", required=True
        ),
    ):
        """Change the status of TIJK Bot"""
        if type == "watching":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.watching, name=text
                )
            )
        elif type == "playing":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.playing, name=text
                )
            )
        elif type == "streaming":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.streaming, name=text
                )
            )
        elif type == "listening":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.listening, name=text
                )
            )
        elif type == "competing":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.competing, name=text
                )
            )

        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Status changed!",
            value=f"Changed the status to **{type} {text}**",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @status.subcommand(name="reset", inherit_hooks=True)
    async def reset_status(self, interaction: Interaction):
        """Reset the status of TIJK Bot"""
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching, name="over the TIJK Server"
            )
        )
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Status changed!",
            value="Reset the status to **watching over the TIJK Server**",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    async def stats(self, interaction: Interaction):
        """Show the statistics of TIJK Bot"""
        embed = nextcord.Embed(
            color=0x0DD91A, title="Here are some stats for TIJK Bot!"
        )
        embed.add_field(
            name="Nextcord version:",
            value=nextcord.__version__,
            inline=False,
        )
        embed.add_field(
            name="Total commands:", value=f"{len(self.bot.commands)}", inline=False
        )
        embed.add_field(
            name="Uptime:",
            value=str(datetime.timedelta(seconds=int(round(time.time() - START_TIME)))),
            inline=False,
        )
        guilds = "".join(
            f"{self.bot.guilds.index(guild)+1}. {guild.name} (**{guild.id}**)\n"
            for guild in self.bot.guilds
        )
        embed.add_field(name="Guilds:", value=guilds, inline=False)
        embed.add_field(name="Users:", value=f"{len(self.bot.users)}", inline=False)
        embed.add_field(
            name="Cogs loaded:", value=f"{len(self.bot.cogs)}", inline=False
        )
        embed.add_field(
            name="Latency:", value=f"{self.bot.latency} seconds", inline=False
        )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def tijkbotdeveloper(self, interaction: Interaction):
        """Give the TIJK-Bot developer role to the owner of TIJK Bot"""
        tijk_bot_developer_role = nextcord.utils.get(
            interaction.guild.roles, name="TIJK-Bot developer"
        )
        if tijk_bot_developer_role not in interaction.user.roles:
            await interaction.user.add_roles(tijk_bot_developer_role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Done!",
                value="You now have the `TIJK-Bot developer` role!",
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title="You already have the `TIJK-Bot developer` role"
            )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def purge_unknown_users(self, interaction: Interaction):
        """Remove invalid users from the database"""
        users_removed = 0
        for user in USER_DATA.find():
            if not self.bot.get_user(user["_id"]):
                USER_DATA.delete_one({"_id": user["_id"]})
                users_removed += 1
        if users_removed > 0:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Removed {users_removed} user(s)!"
            )
        else:
            embed = nextcord.Embed(color=0xFFC800, title="No users were removed!")
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def leave_server(
        self, interaction: Interaction, server_id: str = SlashOption(required=False)
    ):
        """Remove TIJK Bot from a server"""
        if server_id:
            try:
                server_id = int(server_id)
            except ValueError:
                embed = nextcord.Embed(color=0xFFC800, title="Invalid server ID!")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if GUILD := nextcord.utils.get(self.bot.guilds, id=server_id):
                await GUILD.leave()
                embed = nextcord.Embed(color=0x0DD91A, title=f"Left {GUILD.name}")
                await interaction.response.send_message(embed=embed)
            else:
                embed = nextcord.Embed(
                    color=0xFFC800, title="That is not a guild or I am not in it!"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            servers = "\n".join(
                f"> {GUILD.name} (**{GUILD.id}**)" for GUILD in self.bot.guilds
            )
            embed.add_field(name="Available servers:", value=servers)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def cog(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @cog.subcommand(name="load", inherit_hooks=True)
    async def load_cog(
        self,
        interaction: Interaction,
        cog: str = SlashOption(
            choices=[
                "admin",
                "api",
                "developer",
                "error_handler",
                "event_handler",
                "fun",
                "general",
            ],
            description="The cog to load",
            required=True,
        ),
    ):
        """Load a cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Loaded the `{cog}` cog")
            await interaction.response.send_message(embed=embed)
        except ExtensionAlreadyLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is already loaded!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @cog.subcommand(name="reload", inherit_hooks=True)
    async def reload_cog(
        self,
        interaction: Interaction,
        cog: str = SlashOption(
            choices=[
                "admin",
                "api",
                "developer",
                "error_handler",
                "event_handler",
                "fun",
                "general",
            ],
            description="The cog to reload",
            required=True,
        ),
    ):
        """Reload a cog"""
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Reloaded the `{cog}` cog")
            await interaction.response.send_message(embed=embed)
        except ExtensionNotLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is not loaded!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @cog.subcommand(name="unload", inherit_hooks=True)
    async def unload_cog(
        self,
        interaction: Interaction,
        cog: str = SlashOption(
            choices=[
                "admin",
                "api",
                "developer",
                "error_handler",
                "event_handler",
                "fun",
                "general",
            ],
            description="The cog to unload",
            required=True,
        ),
    ):
        """Unload a cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Unloaded the `{cog}` cog")
            await interaction.response.send_message(embed=embed)
        except ExtensionNotLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is not loaded!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.has_any_role("Owner", "Admin", "TIJK-Bot developer")
    async def command(self, interaction: Interaction):
        """This will never get called since it has subcommands"""
        pass

    @command.subcommand(name="enable", inherit_hooks=True)
    async def enable_command(
        self,
        interaction: Interaction,
        command_name: str = SlashOption(
            name="command", description="The command to enable", required=True
        ),
    ):
        """Enable a command"""
        command = self.bot.get_command(command_name)
        if not command:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"The `{command_name}` command is not found"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif not command.enabled:
            command.enabled = True
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The `{command.qualified_name}` command is now enabled!",
            )
            bl.debug(f"The {command.qualified_name} command is now enabled!", __file__)
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The `{command.qualified_name}` command is already enabled!",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @command.subcommand(name="disable", inherit_hooks=True)
    async def disable_command(
        self,
        interaction: Interaction,
        command_name: str = SlashOption(
            name="command", description="The command to disable", required=True
        ),
    ):
        """Disable a command"""
        command = self.bot.get_command(command_name)
        if not command:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"The `{command_name}` command is not found"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command.enabled:
            command.enabled = False
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The `{command.qualified_name}` command is now disabled!",
            )
            bl.debug(f"The {command.qualified_name} command is now disabled!", __file__)
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The `{command.qualified_name}` command is already disabled!",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(developer_slash(bot))

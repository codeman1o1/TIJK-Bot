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


class developer_slash(
    commands.Cog,
    name="Developer Slash Commands",
    description="Slash commands for developers",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(
        description="Generate an embed",
        guild_ids=SLASH_GUILDS,
    )
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

    @slash(
        description="Restarts TIJK Bot",
        guild_ids=SLASH_GUILDS,
    )
    @checks.is_owner()
    async def restart(self, interaction: nextcord.Interaction):
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
        os.system(command)
        os.execv(sys.executable, ["python"] + sys.argv)

    @slash(guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def status(
        self,
        interaction: Interaction,
    ):
        """This will never get called since it has subcommands"""
        pass

    @status.subcommand(
        name="set", description="Sets the status of TIJK Bot", inherit_hooks=True
    )
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

    @status.subcommand(
        name="reset", description="Resets the status of TIJK Bot", inherit_hooks=True
    )
    async def reset_status(self, interaction: Interaction):
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

    @slash(description="Shows the statistics of TIJK Bot", guild_ids=SLASH_GUILDS)
    async def stats(self, interaction: Interaction):
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

    @slash(
        description="Gives the TIJK-Bot developer role to the owner of TIJK Bot",
        guild_ids=SLASH_GUILDS,
    )
    @checks.is_owner()
    async def tijkbotdeveloper(self, interaction: Interaction):
        tijk_bot_developer_role = nextcord.utils.get(
            interaction.guild.roles, name="TIJK-Bot developer"
        )
        if tijk_bot_developer_role not in interaction.user.roles:
            await interaction.user.add_roles(tijk_bot_developer_role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Done!",
                value="You now have the `TIJK Bot developer` role!",
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title="You already have the `TIJK-Bot developer` role"
            )
        await interaction.response.send_message(embed=embed)

    @slash(
        description="Removes invalid users from the database", guild_ids=SLASH_GUILDS
    )
    @checks.is_owner()
    async def purge_unknown_users(self, interaction: Interaction):
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

    @slash(description="Lets TIJK Bot leave a server", guild_ids=SLASH_GUILDS)
    @checks.is_owner()
    async def leave_server(
        self, interaction: Interaction, server_id: str = SlashOption(required=False)
    ):
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
        """This will never get called since it has subcommand"""
        pass

    @cog.subcommand(name="load", description="Load a cog", inherit_hooks=True)
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
        try:
            self.bot.load_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Loaded the `{cog}` cog")
        except ExtensionAlreadyLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is already loaded!"
            )
        await interaction.response.send_message(embed=embed)

    @cog.subcommand(name="reload", description="Reload a cog", inherit_hooks=True)
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
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Reloaded the `{cog}` cog")
        except ExtensionNotLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is not loaded!"
            )
        await interaction.response.send_message(embed=embed)

    @cog.subcommand(name="unload", description="Unload a cog", inherit_hooks=True)
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
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            embed = nextcord.Embed(color=0x0DD91A, title=f"Unloaded the `{cog}` cog")
        except ExtensionNotLoaded:
            embed = nextcord.Embed(
                color=0xFFC800, title=f"The `{cog}` cog is not loaded!"
            )
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(developer_slash(bot))

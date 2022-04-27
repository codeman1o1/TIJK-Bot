import datetime
import os
import sys
import time

import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands

from main import USER_DATA, log, SLASH_GUILDS, START_TIME
from slash.custom_checks import is_bot_owner, is_server_owner, is_admin


class Developer(commands.Cog, name="Developer Slash Commands"):
    """Slash commands for developers"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    @is_admin()
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
        footer: str = SlashOption(
            description="The footer of the embed", required=False
        ),
        name1: str = SlashOption(
            description="The name of the 1st field", required=False
        ),
        value1: str = SlashOption(
            description="The value of the 1st field", required=False
        ),
        name2: str = SlashOption(
            description="The name of the 2nd field", required=False
        ),
        value2: str = SlashOption(
            description="The value of the 2nd field", required=False
        ),
        name3: str = SlashOption(
            description="The name of the 3d field", required=False
        ),
        value3: str = SlashOption(
            description="The value of the 3d field", required=False
        ),
        name4: str = SlashOption(
            description="The name of the 3d field", required=False
        ),
        value4: str = SlashOption(
            description="The value of the 3d field", required=False
        ),
        name5: str = SlashOption(
            description="The name of the 3d field", required=False
        ),
        value5: str = SlashOption(
            description="The value of the 3d field", required=False
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
            if footer:
                embed.set_footer(text=footer)
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
            if name4 and value4:
                embed.add_field(
                    name=name4,
                    value=value4,
                    inline=False,
                )
            if name5 and value5:
                embed.add_field(
                    name=name5,
                    value=value5,
                    inline=False,
                )
            await interaction.response.send_message(embed=embed)
        except nextcord.errors.HTTPException:
            await interaction.response.send_message(
                "The embed is invalid", ephemeral=True
            )

    @slash(guild_ids=SLASH_GUILDS)
    @is_server_owner()
    async def restart(self, interaction: nextcord.Interaction):
        """Restart TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot is restarting...",
            value=f"TIJK Bot was restarted by {interaction.user}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        await log(
            interaction,
            f"TIJK Bot was restarted by {interaction.user}",
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
    @is_server_owner()
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
        status_type: str = SlashOption(
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
        if status_type == "watching":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.watching, name=text
                )
            )
        elif status_type == "playing":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.playing, name=text
                )
            )
        elif status_type == "streaming":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.streaming, name=text
                )
            )
        elif status_type == "listening":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.listening, name=text
                )
            )
        elif status_type == "competing":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.competing, name=text
                )
            )

        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Status changed!",
            value=f"Changed the status to **{status_type} {text}**",
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
            name="Uptime:",
            value=str(datetime.timedelta(seconds=int(round(time.time() - START_TIME)))),
            inline=False,
        )
        guilds = "".join(
            f"{self.bot.guilds.index(guild) + 1}. {guild.name} (**{guild.id}**)\n"
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
    @is_bot_owner()
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
    @is_bot_owner()
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
            if guild := nextcord.utils.get(self.bot.guilds, id=server_id):
                await guild.leave()
                embed = nextcord.Embed(color=0x0DD91A, title=f"Left {guild.name}")
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


def setup(bot):
    bot.add_cog(Developer(bot))

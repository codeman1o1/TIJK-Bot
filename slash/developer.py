import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
import nextcord.ext.application_checks as checks
import os, sys
import datetime, time

from main import logger, SLASH_GUILDS, START_TIME


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
        name4: str = SlashOption(
        name="name4", description="The name of the 4th field", required=False
        ),
        value4: str = SlashOption(
        name="value4", description="The value of the 4th field", required=False
        ),
        name5: str = SlashOption(
        name="name5", description="The name of the 5th field", required=False
        ),
        value5: str = SlashOption(
        name="value5", description="The value of the 5th field", required=False
        ),
        name6: str = SlashOption(
        name="name6", description="The name of the 6th field", required=False
        ),
        value6: str = SlashOption(
        name="value6", description="The value of the 6th field", required=False
        ),
        name7: str = SlashOption(
        name="name7", description="The name of the 7th field", required=False
        ),
        valu7: str = SlashOption(
        name="value7", description="The value of the 7th field", required=False
        ),
        name8: str = SlashOption(
        name="name8", description="The name of the 8th field", required=False
        ),
        value8: str = SlashOption(
        name="value8", description="The value of the 8th field", required=False
        ),
        name8: str = SlashOption(
        name="name8", description="The name of the 8th field", required=False
        ),
        value8: str = SlashOption(
        name="value8", description="The value of the 8th field", required=False
        ),
        name9: str = SlashOption(
        name="name9", description="The name of the 9th field", required=False
        ),
        value9: str = SlashOption(
        name="value9", description="The value of the 9th field", required=False
        ),
        name10: str = SlashOption(
        name="name10", description="The name of the 10th field", required=False
        ),
        value10: str = SlashOption(
        name="value10", description="The value of the 10th field", required=False
        ),
        name11: str = SlashOption(
        name="name11", description="The name of the 11th field", required=False
        ),
        value11: str = SlashOption(
        name="value11", description="The value of the 11th field", required=False
        ),
        name12: str = SlashOption(
        name="name12", description="The name of the 12th field", required=False
        ),
        value12: str = SlashOption(
        name="value12", description="The value of the 12th field", required=False
        ),
        name13: str = SlashOption(
        name="name13", description="The name of the 13th field", required=False
        ),
        value13: str = SlashOption(
        name="value13", description="The value of the 13th field", required=False
        ),
        name14: str = SlashOption(
        name="name14", description="The name of the 14th field", required=False
        ),
        value14: str = SlashOption(
        name="value14", description="The value of the 14th field", required=False
        ),
        name15: str = SlashOption(
        name="name15", description="The name of the 15th field", required=False
        ),
        value15: str = SlashOption(
        name="value15", description="The value of the 15th field", required=False
        ),
    ):
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
            if name6 and value6:
                embed.add_field(
                    name=name6,
                    value=value6,
                    inline=False,
                )
            if name7 and value7:
                embed.add_field(
                    name=name7,
                    value=value7,
                    inline=False,
                )
            if name8 and value8:
                embed.add_field(
                    name=name8,
                    value=value8,
                    inline=False,
                )
            if name9 and value9:
                embed.add_field(
                    name=name9,
                    value=value9,
                    inline=False,
                )
            if name10 and value10:
                embed.add_field(
                    name=name10,
                    value=value10,
                    inline=False,
                )
            if name11 and value11:
                embed.add_field(
                    name=name11,
                    value=value11,
                    inline=False,
                )
            if name12 and value12:
                embed.add_field(
                    name=name12,
                    value=value12,
                    inline=False,
                )
            if name13 and value13:
                embed.add_field(
                    name=name13,
                    value=value13,
                    inline=False,
                )
            if name14 and value14:
                embed.add_field(
                    name=name14,
                    value=value14,
                    inline=False,
                )
            if name15 and value15:
                embed.add_field(
                    name=name15,
                    value=value15,
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


def setup(bot):
    bot.add_cog(developer_slash(bot))

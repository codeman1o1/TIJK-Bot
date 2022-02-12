import datetime
import os
import sys
import time

import nextcord
import psutil
from nextcord.ext import commands
from nextcord.ext.commands import Context

from main import logger
from main import BOT_DATA, USER_DATA, START_TIME


class developer(commands.Cog, name="Developer"):
    """Commands only the owner of TIJK Bot can use"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="restart")
    @commands.is_owner()
    async def restart(self, ctx: Context):
        """Restarts TIJK Bot"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="TIJK Bot is restarting...",
            value=f"TIJK Bot was restarted by {ctx.author}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logger(ctx, f"TIJK Bot was restarted by {ctx.author}")
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.playing, name="Restarting..."
            )
        )
        command = "cls" if os.name in ("nt", "dos") else "clear"
        os.system(command)
        os.execv(sys.executable, ["python"] + sys.argv)

    @commands.command(name="status")
    @commands.is_owner()
    async def status(self, ctx: Context, type: str, *, text: str = "the TIJK Server"):
        """Sets the status of TIJK Bot"""
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
        elif type == "reset":
            await self.bot.change_presence(
                activity=nextcord.Activity(
                    type=nextcord.ActivityType.watching, name=text
                )
            )
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Status changed!",
                value="Reset the status to **watching the TIJK Server**",
                inline=False,
            )

            await ctx.send(embed=embed)
            return

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Could not change te status!",
                value=f"{type} is not a valid activity",
                inline=False,
            )

            await ctx.send(embed=embed)
            return

        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Status changed!",
            value=f"Changed the status to **{type} {text}**",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command(name="tijkbotdeveloper", aliases=["tbdv"])
    @commands.bot_has_permissions(manage_roles=True)
    @commands.is_owner()
    async def tijkbotdeveloper(self, ctx: Context):
        """Gives the TIJK-Bot developer role to the owner of TIJK Bot"""
        tijk_bot_developer_role = nextcord.utils.get(
            ctx.guild.roles, name="TIJK-Bot developer"
        )
        if tijk_bot_developer_role not in ctx.author.roles:
            await ctx.author.add_roles(tijk_bot_developer_role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Done!",
                value='You now have the "TIJK Bot developer" role!',
                inline=False,
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title='You already have the "TIJK-Bot developer" role'
            )
        await ctx.send(embed=embed)

    @commands.command(name="stats")
    async def stats(self, ctx: Context):
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
        await ctx.send(embed=embed)

    @commands.command(name="puu")
    @commands.is_owner()
    async def purge_unknown_users(self, ctx: Context):
        """Removes invalid users from the database"""
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
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(developer(bot))

import nextcord
from nextcord.ext import commands
import urllib
import requests
import os
import sys


class developer(
    commands.Cog,
    name="Developer",
    description="Commands only the owner of TIJK Bot can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(
        name="debug",
        description="Gets the status codes from the TIJK Bot websites",
        brief="Gets the status codes from the TIJK Bot websites",
        invoke_without_command=True,
    )
    @commands.is_owner()
    async def debug(self, ctx):
        async with ctx.typing():
            embed = nextcord.Embed(color=0x0DD91A)
            try:
                response = urllib.request.urlopen("https://TIJK-Bot.codeman1o1.repl.co")
                status_code = response.getcode()
                elapsed = requests.get(
                    "https://TIJK-Bot.codeman1o1.repl.co"
                ).elapsed.total_seconds()
                embed.add_field(
                    name=f"https://TIJK-Bot.codeman1o1.repl.co",
                    value=f"Status code: {status_code}\nResponse time: {elapsed} seconds",
                    inline=False,
                )
            except:
                embed.add_field(
                    name=f"https://TIJK-Bot.codeman1o1.repl.co",
                    value=f"TIJK Bot doesn't seem reachable",
                    inline=False,
                )

            try:
                response = urllib.request.urlopen(
                    "https://TIJK-Music.codeman1o1.repl.co"
                )
                status_code = response.getcode()
                elapsed = requests.get(
                    "https://TIJK-Music.codeman1o1.repl.co"
                ).elapsed.total_seconds()
                embed.add_field(
                    name=f"https://TIJK-Music.codeman1o1.repl.co",
                    value=f"Status code: {status_code}\nResponse time: {elapsed} seconds",
                    inline=False,
                )
            except:
                embed.add_field(
                    name=f"https://TIJK-Bot.codeman1o1.repl.co",
                    value=f"TIJK Music doesn't seem reachable",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @debug.command(
        name="codes", description="View the status codes", brief="View the status codes"
    )
    async def codes_debug(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The status codes are the following:",
            value=f"> 200: Ok\n> 301: Permanent Redirect\n> 302: Temporary Redirect\n> 404: Not Found\n> 410: Gone\n> 500: Internal Server Error\n> 503: Service Unavailable",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="restart", description="Restarts TIJK Bot", brief="Restarts TIJK Bot"
    )
    @commands.has_any_role("TIJK-Bot developer")
    async def restart(self, ctx):
        mo = nextcord.utils.get(ctx.guild.channels, name="moderator-only")
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"TIJK Bot is restarting...",
            value=f"TIJK Bot was restarted by {ctx.author.display_name}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await mo.send(embed=embed)
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.playing, name="Restarting..."
            )
        )
        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)
        os.execv(sys.executable, ["python"] + sys.argv)

    @commands.command(
        name="status",
        description="Sets the status of TIJK Bot",
        brief="Sets the status of TIJK Bot",
    )
    @commands.is_owner()
    async def status(self, ctx, type, *, text: str = "the TIJK Server"):
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
                name=f"Status changed!",
                value=f"Reset the status to **watching the TIJK Server**",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Could not change te status!",
                value=f"{type} is not a valid activity",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Status changed!",
            value=f"Changed the status to **{type} {text}**",
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="tijkbotdeveloper",
        description="Gives the TIJK-Bot developer role to codeman1o1#1450 if it was somehow removed",
        brief="Gives the TIJK-Bot developer role to codeman1o1#1450 if it was somehow removed",
        aliases=["tbdv"],
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.is_owner()
    async def tijkbotdeveloper(self, ctx):
        tbdv = nextcord.utils.get(ctx.guild.roles, name="TIJK-Bot developer")
        if not tbdv in ctx.author.roles:
            await ctx.author.add_roles(tbdv)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Done!",
                value='You now have the "TIJK Bot developer" role!',
                inline=False,
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x0DD91A, title='You already have the "TIJK-Bot developer" role'
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(developer(bot))

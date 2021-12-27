import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
import uptime
import time
import psutil
import os
import sys
import json

load_dotenv(os.path.join(os.getcwd() + "\.env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


class developer(
    commands.Cog,
    name="Developer",
    description="Commands only the owner of TIJK Bot can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="restart", description="Restarts TIJK Bot", brief="Restarts TIJK Bot"
    )
    @commands.has_any_role("TIJK-Bot developer")
    async def restart(self, ctx):
        logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"TIJK Bot is restarting...",
            value=f"TIJK Bot was restarted by {ctx.author.display_name}",
            inline=False,
        )
        await ctx.send(embed=embed)
        await logs_channel.send(embed=embed)
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
        description="Gives the TIJK-Bot developer role to the owner of TIJK Bot if it was somehow removed",
        brief="Gives the TIJK-Bot developer role to the owner of TIJK Bot if it was somehow removed",
        aliases=["tbdv"],
    )
    @commands.bot_has_permissions(manage_roles=True)
    @commands.is_owner()
    async def tijkbotdeveloper(self, ctx):
        tijk_bot_developer_role = nextcord.utils.get(
            ctx.guild.roles, name="TIJK-Bot developer"
        )
        if not tijk_bot_developer_role in ctx.author.roles:
            await ctx.author.add_roles(tijk_bot_developer_role)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Done!",
                value='You now have the "TIJK Bot developer" role!',
                inline=False,
            )
        elif tijk_bot_developer_role in ctx.author.roles:
            embed = nextcord.Embed(
                color=0x0DD91A, title='You already have the "TIJK-Bot developer" role'
            )
        await ctx.send(embed=embed)

    @commands.group(
        name="reactionmessages",
        description="",
        brief="",
        invoke_without_command=True,
        aliases=["rm"],
    )
    @commands.is_owner()
    async def reactionmessages(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        for k in BotData.find():
            reaction_messages = k["reactionmessages"]
        reaction_messages = json.loads(reaction_messages)
        reaction_messages2 = ""
        for k, v in reaction_messages.items():
            reaction_messages2 = reaction_messages2 + f"{k}: {v}\n"

        embed.add_field(
            name=f"The current reaction messages are:",
            value=reaction_messages2,
            inline=False,
        )
        embed.add_field(
            name=f"Things to keep in mind:",
            value="> The reaction messages will always be checked in lowercase\n> You can use `{user}` to use the display name of the sender\n> Use quotation marks to define multiple words\n> You can overwrite existing keys by adding a reaction message with the same key",
            inline=False,
        )
        await ctx.send(embed=embed)

    @reactionmessages.command(name="add", description="", brief="")
    async def add_reactionmessages(self, ctx, message: str, reaction: str):
        message = message.lower()
        new_dictionary = {message: reaction}
        for k in BotData.find():
            reaction_messages = k["reactionmessages"]
            reaction_messages = dict(json.loads(reaction_messages))
            reaction_messages = reaction_messages | new_dictionary
            reaction_messages = str(reaction_messages)
            reaction_messages = reaction_messages.replace("'", '"')
            BotData.update_one(
                {"_id": k["_id"]},
                {"$set": {"reactionmessages": reaction_messages}},
                upsert=False,
            )
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"Succesfully added `{message}: {reaction}` to the reaction messages",
        )
        await ctx.send(embed=embed)

    @reactionmessages.command(name="remove", description="", brief="")
    async def remove_reactionmessages(self, ctx, message: str):
        try:
            message = message.lower()
            for k in BotData.find():
                reaction_messages = k["reactionmessages"]
                reaction_messages = dict(json.loads(reaction_messages))
                del reaction_messages[message]
                reaction_messages = str(reaction_messages)
                reaction_messages = reaction_messages.replace("'", '"')
                BotData.update_one(
                    {"_id": k["_id"]},
                    {"$set": {"reactionmessages": reaction_messages}},
                    upsert=False,
                )
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Succesfully removed `{message}` from the reaction messages",
            )
            await ctx.send(embed=embed)
        except KeyError:
            embed = nextcord.Embed(color=0xFF0000, title=f"`{message}` was not found")
            await ctx.send(embed=embed)

    @commands.command(
        name="stats",
        description="Shows the stats of TIJK Bot",
        brief="Shows the stats of TIJK Bot",
    )
    async def stats(self, ctx):
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Here are some stats for TIJK Bot!"
        )
        embed.add_field(
            name=f"Total commands:",
            value=f"{len(self.bot.commands)}",
            inline=False,
        )
        uptime2 = time.strftime("%H:%M:%S", time.gmtime(uptime.uptime()))
        embed.add_field(
            name=f"Uptime:",
            value=f"{uptime2}",
            inline=False,
        )
        embed.add_field(
            name=f"Guilds:",
            value=f"{len(self.bot.guilds)}",
            inline=False,
        )
        embed.add_field(
            name=f"Users:",
            value=f"{len(self.bot.users)}",
            inline=False,
        )
        embed.add_field(
            name=f"Cogs loaded:",
            value=f"{len(self.bot.cogs)}",
            inline=False,
        )
        # CPU usage is index nr. 5
        embed.add_field(
            name=f"CPU usage:",
            value=f"`Please wait 5 seconds for accurate usage`",
            inline=False,
        )
        embed.add_field(
            name=f"Latency:",
            value=f"{self.bot.latency} seconds",
            inline=False,
        )
        msg = await ctx.send(embed=embed)
        embed.set_field_at(
            5, name=f"CPU usage:", value=f"{psutil.cpu_percent(5)} percent"
        )
        await msg.edit(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(developer(bot))

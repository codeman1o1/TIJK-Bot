# TIJK-Bot is made and maintaned by codeman1o1 (https://github.com/codeman1o1)

import asyncio
import os
import datetime
import time
import basic_logger as bl

import nextcord
import nextcord.ext.commands.errors
from nextcord.ext import commands
from nextcord.ext import tasks
from dotenv import load_dotenv
from pretty_help import PrettyHelp
from pymongo import MongoClient

load_dotenv(os.path.join(".env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]

client = nextcord.Client()
bot = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    strip_after_prefix=True,
    intents=nextcord.Intents.all(),
    help_command=PrettyHelp(
        color=0x0DD91A,
        no_category="Root",
        ending_note="Type .help command for more info on a command.\nIf you need help with any of our bots please type\n- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- ,help for Hydra",
    ),
)


@bot.event
async def on_ready():
    bl.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}", __file__)
    with open("spam_detect.txt", "a+") as file:
        file.truncate(0)
    cogs = os.listdir("cogs")
    try:
        cogs.remove("__pycache__")
    except ValueError:
        pass
    for cog in cogs:
        try:
            cog = cog.strip(".py")
            bot.load_extension(f"cogs.{cog}")
            bl.debug(f"{cog}.py loaded!", __file__)
        except:
            bl.error(f"{cog}.py couldn't be loaded!", __file__)
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name="the TIJK Server"
        )
    )
    birthday_checker.start()
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@tasks.loop(seconds=10)
async def birthday_checker():
    if time.strftime("%H") == "12":
        birthdays = []
        today = datetime.date.today()
        year = today.year
        for k in UserData.find():
            try:
                if k["birthday"]:
                    birthday2 = k["birthday"].split("-")
                    date = datetime.date(year, int(birthday2[1]), int(birthday2[0]))
                    if today == date:
                        birthdays.append(k["_id"])
            except KeyError:
                pass
        for member in birthdays:
            member = bot.get_user(member)
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Happy birthday {member.name} :tada:",
                value=f"We hope you will have a great day!",
                inline=False,
            )
            for guild in bot.guilds:
                await guild.system_channel.send(embed=embed)
        birthdays.clear()
        birthday_checker.cancel()


@bot.command(
    name="load_cog", description="Loads a cog", brief="Loads a cog", aliases=["lc"]
)
@commands.is_owner()
async def load_cog(ctx, cog: str = None):
    if cog is None:
        cogs = os.listdir("cogs")
        cogs.remove("__pycache__")
        cogs = str(cogs)
        cogs = cogs.replace(".py", "")
        cogs = cogs.replace("[", "")
        cogs = cogs.replace("]", "")
        cogs = cogs.replace("'", "")
        cogs = cogs.replace(",", "\n>")
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {cogs}",
            inline=False,
        )
        await ctx.send(embed=embed)
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for cog in cogs:
            cog = cog.strip(".py")
            bot.load_extension(f"cogs.{cog}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been loaded!")
        bl.debug(f"All cogs have been loaded!", __file__)
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.load_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully loaded {cog.lower()}.py"
        )
        bl.debug(f"Succesfully loaded {cog.lower()}.py", __file__)
    await ctx.send(embed=embed)


@bot.command(
    name="reloadcog",
    description="Reloads a cog",
    brief="Reloads a cog",
    aliases=["rlc", "rc"],
)
async def reload_cog(ctx, cog: str = None):
    cogs = os.listdir("cogs")
    cogs.remove("__pycache__")
    cogs = str(cogs)
    cogs = cogs.replace(".py", "")
    cogs = cogs.replace("[", "")
    cogs = cogs.replace("]", "")
    cogs = cogs.replace("'", "")
    cogs = cogs.replace(",", "\n>")
    if cog is None:
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {cogs}",
            inline=False,
        )
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for cog in cogs:
            cog = cog.strip(".py")
            bot.reload_extension(f"cogs.{cog}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been reloaded!")
        bl.debug(f"All cogs have been reloaded!", __file__)
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.reload_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully reloaded {cog.lower()}.py"
        )
        bl.debug(f"Succesfully reloaded {cog.lower()}.py", __file__)
    await ctx.send(embed=embed)


@bot.command(
    name="unload_cog",
    description="Unloads a cog",
    brief="Unloads a cog",
    aliases=["ulc", "uc"],
)
@commands.is_owner()
async def unload_cog(ctx, cog: str = None):
    cogs = os.listdir("cogs")
    cogs.remove("__pycache__")
    cogs = str(cogs)
    cogs = cogs.replace(".py", "")
    cogs = cogs.replace("[", "")
    cogs = cogs.replace("]", "")
    cogs = cogs.replace("'", "")
    cogs = cogs.replace(",", "\n>")
    if cog is None:
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {cogs}",
            inline=False,
        )
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for cog in cogs:
            cog = cog.strip(".py")
            bot.unload_extension(f"cogs.{cog}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been unloaded!")
        bl.debug(f"All cogs have been unloaded!", __file__)
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.unload_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully unloaded {cog.lower()}.py!"
        )
        bl.debug(f"Succesfully unloaded {cog.lower()}.py!", __file__)
    await ctx.send(embed=embed)


@bot.command(
    name="enable_command",
    description="Enables a command",
    brief="Enables a command",
    aliases=["ec"],
)
@commands.is_owner()
async def enable_command(ctx, *, command: str):
    command_name = command
    command = bot.get_command(command)
    if command is None:
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"The .{command_name} command is not found"
        )
    elif not command.enabled:
        command.enabled = True
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"The .{command.qualified_name} command is now enabled!",
        )
        bl.debug(f"The .{command.qualified_name} command is now enabled!", __file__)
    elif command.enabled:
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"The .{command.qualified_name} command is already enabled!",
        )
    await ctx.send(embed=embed)


@bot.command(
    name="disable_command",
    description="Disables a command",
    brief="Disables a command",
    aliases=["dc"],
)
@commands.is_owner()
async def disable_command(ctx, *, command: str):
    command_name = command
    command = bot.get_command(command)
    load_cog_command = bot.get_command("load_cog")
    unload_cog_command = bot.get_command("unload_cog")
    load_command_command = bot.get_command("load_command")
    unload_command_command = bot.get_command("unload_command")
    disable_prevention = (
        load_cog_command,
        unload_cog_command,
        load_command_command,
        unload_command_command,
    )
    if command is None:
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"The .{command_name} command is not found"
        )
    elif not command in disable_prevention:
        if command.enabled:
            command.enabled = False
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The .{command.qualified_name} command is now disabled!",
            )
            bl.debug(
                f"The .{command.qualified_name} command is now disabled!", __file__
            )
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The .{command.qualified_name} command is already disabled!",
            )
    elif command in disable_prevention:
        embed = nextcord.Embed(color=0x0DD91A, title="Root commands can't be disabled!")
    await ctx.send(embed=embed)


bot.run(os.environ["BotToken"])

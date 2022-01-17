# TIJK-Bot is made and maintaned by codeman1o1 (https://github.com/codeman1o1)

import asyncio
import datetime
import os
import time

import nextcord
import nextcord.ext.commands.errors
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from pretty_help import PrettyHelp
from pymongo import MongoClient

import basic_logger as bl

load_dotenv(".env")
BOT_TOKEN = os.environ["BotToken"]
HYPIXEL_API_KEY = os.environ["HypixelApiKey"]
CLUSTER = MongoClient(os.environ["MongoURL"])
DATA = CLUSTER["Data"]
BOT_DATA = DATA["BotData"]
USER_DATA = DATA["UserData"]

client = nextcord.Client()
bot = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    strip_after_prefix=True,
    intents=nextcord.Intents.all(),
    help_command=PrettyHelp(
        color=0x0DD91A,
        no_category="Root",
        ending_note="Type .help <command> for more info on a command\nType .help <category> for more info on a category\nIf you need help with any of our bots please type\n- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- ,help for Hydra",
    ),
)


@bot.event
async def on_ready():
    bl.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}", __file__)
    cogs = os.listdir("cogs")
    try:
        cogs.remove("__pycache__")
    except ValueError:
        pass
    for cog in cogs:
        if cog.endswith(".py"):
            try:
                cog2 = cog.strip(".py")
                bot.load_extension(f"cogs.{cog2}")
                bl.debug(f"{cog} loaded", __file__)
            except Exception as e:
                print(e)
                bl.error(f"{cog} couldn't be loaded", __file__)
    with open("spam_detect.txt", "a+") as file:
        file.truncate(0)
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name="over the TIJK Server"
        )
    )
    remove_invalid_users.start()
    birthday_checker.start()
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@tasks.loop(hours=1)
async def remove_invalid_users():
    for k in USER_DATA.find():
        if not bot.get_user(k["_id"]):
            USER_DATA.delete_one({"_id": k["_id"]})


@tasks.loop(seconds=10)
async def birthday_checker():
    if time.strftime("%H") != "12":
        return

    birthdays = []
    today = datetime.date.today()
    year = today.year
    for k in USER_DATA.find():
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
            value="We hope you will have a great day!",
            inline=False,
        )

        for guild in bot.guilds:
            await guild.system_channel.send(embed=embed)
    birthdays.clear()
    birthday_checker.cancel()


@bot.event
async def on_message(message):
    if "Event Handler" in bot.cogs:
        return
    else:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    embed = nextcord.Embed(color=0xFF0000)
    embed.add_field(name="An error occured!", value=error, inline=True)
    await ctx.send(embed=embed)
    bl.error(error, __file__)


@bot.command(
    name="load_cog", description="Loads a cog", brief="Loads a cog", aliases=["lc"]
)
@commands.is_owner()
async def load_cog(ctx, cog: str = None):
    try:
        if cog is None:
            cogs = os.listdir("cogs")
            try:
                cogs.remove("__pycache__")
            except ValueError:
                pass
            cogs2 = "> all"
            for k in cogs:
                cogs2 = cogs2 + "\n> " + k.strip(".py")
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="The available cogs are:",
                value=cogs2,
                inline=False,
            )

        elif cog.lower() == "all":
            try:
                cogs = os.listdir("cogs")
                try:
                    cogs.remove("__pycache__")
                except ValueError:
                    pass
                for cog in cogs:
                    if cog.endswith(".py"):
                        cog2 = cog.strip(".py")
                        bot.load_extension(f"cogs.{cog2}")
                embed = nextcord.Embed(
                    color=0x0DD91A, title="All cogs have been loaded"
                )
                bl.debug("All cogs have been loaded", __file__)
            except:
                embed = nextcord.Embed(
                    color=0xFF0000, title="Not all cogs could be loaded"
                )
                bl.warning("Not all cogs could be loaded", __file__)
        else:
            if cog.lower() == "dev":
                cog = "developer"
            if cog.lower() == "eh":
                cog = "event_handler"
            bot.load_extension(f"cogs.{cog.lower()}")
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Succesfully loaded {cog.lower()}.py"
            )
            bl.debug(f"Succesfully loaded {cog.lower()}.py", __file__)
    except nextcord.ext.commands.errors.ExtensionNotFound:
        embed = nextcord.Embed(color=0xFF0000, title=f'The "{cog}" cog was not found')
    except nextcord.ext.commands.errors.NoEntryPointError:
        embed = nextcord.Embed(color=0xFF0000, title=f"{cog} is not a valid cog")
    await ctx.send(embed=embed)


@bot.command(
    name="reloadcog",
    description="Reloads a cog",
    brief="Reloads a cog",
    aliases=["rlc", "rc"],
)
async def reload_cog(ctx, cog: str = None):
    try:
        cogs = os.listdir("cogs")
        cogs.remove("__pycache__")
        cogs2 = "> all"
        for k in cogs:
            cogs2 = cogs2 + "\n> " + k.strip(".py")
        if cog is None:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="The available cogs are:",
                value=cogs2,
                inline=False,
            )

        elif cog.lower() == "all":
            try:
                cogs = os.listdir("cogs")
                try:
                    cogs.remove("__pycache__")
                except ValueError:
                    pass
                for cog in cogs:
                    if cog.endswith(".py"):
                        cog2 = cog.strip(".py")
                        bot.reload_extension(f"cogs.{cog2}")
                embed = nextcord.Embed(
                    color=0x0DD91A, title="All cogs have been reloaded"
                )
                bl.debug("All cogs have been reloaded", __file__)
            except:
                embed = nextcord.Embed(
                    color=0xFF0000, title="Not all cogs could be reloaded"
                )
                bl.warning("Not all cogs could be reloaded", __file__)
        else:
            if cog.lower() == "dev":
                cog = "developer"
            if cog.lower() == "eh":
                cog = "event_handler"
            bot.reload_extension(f"cogs.{cog.lower()}")
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Succesfully reloaded {cog.lower()}.py"
            )
            bl.debug(f"Succesfully reloaded {cog.lower()}.py", __file__)
    except nextcord.ext.commands.errors.ExtensionNotLoaded:
        embed = nextcord.Embed(color=0xFF0000, title=f'The "{cog}" cog is not loaded')
    except nextcord.ext.commands.errors.NoEntryPointError:
        embed = nextcord.Embed(color=0xFF0000, title=f"{cog} is not a valid cog")
    await ctx.send(embed=embed)


@bot.command(
    name="unload_cog",
    description="Unloads a cog",
    brief="Unloads a cog",
    aliases=["ulc", "uc"],
)
@commands.is_owner()
async def unload_cog(ctx, cog: str = None):
    try:
        cogs = os.listdir("cogs")
        cogs.remove("__pycache__")
        cogs2 = "> all"
        for k in cogs:
            cogs2 = cogs2 + "\n> " + k.strip(".py")
        if cog is None:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="The available cogs are:",
                value=cogs2,
                inline=False,
            )

        elif cog.lower() == "all":
            try:
                cogs = os.listdir("cogs")
                try:
                    cogs.remove("__pycache__")
                except ValueError:
                    pass
                for cog in cogs:
                    cog2 = cog.strip(".py")
                    bot.unload_extension(f"cogs.{cog2}")
                embed = nextcord.Embed(
                    color=0x0DD91A, title="All cogs have been unloaded"
                )
                bl.debug("All cogs have been unloaded", __file__)
            except:
                embed = nextcord.Embed(
                    color=0xFF0000, title="Not all cogs could be unloaded"
                )
                bl.warning("Not all cogs could be unloaded", __file__)
        else:
            if cog.lower() == "dev":
                cog = "developer"
            if cog.lower() == "eh":
                cog = "event_handler"
            bot.unload_extension(f"cogs.{cog.lower()}")
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Succesfully unloaded {cog.lower()}.py!"
            )
            bl.debug(f"Succesfully unloaded {cog.lower()}.py!", __file__)
    except nextcord.ext.commands.errors.ExtensionNotLoaded:
        embed = nextcord.Embed(color=0xFF0000, title=f'The "{cog}" cog is not loaded')
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
    else:
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
    elif command not in disable_prevention:
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
    else:
        embed = nextcord.Embed(color=0x0DD91A, title="Root commands can't be disabled!")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    slash = os.listdir("slash")
    try:
        slash.remove("__pycache__")
    except ValueError:
        pass
    for file in slash:
        if file.endswith(".py"):
            try:
                file2 = file.strip(".py")
                bot.load_extension(f"slash.{file2}")
                bl.debug(f"{file} loaded", __file__)
            except:
                bl.error(f"{file} couldn't be loaded", __file__)

    bot.run(BOT_TOKEN)

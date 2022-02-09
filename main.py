# TIJK-Bot is made and maintaned by codeman1o1 (https://github.com/codeman1o1)

import asyncio
import datetime
import os
import time

import nextcord
import nextcord.ext.commands.errors
from nextcord.ext.commands import Context
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
START_TIME = time.time()


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


async def warn_system(
    event,
    user: nextcord.Member,
    amount: int = 1,
    invoker_username: str = "Warn System",
    reason: str = None,
):
    """
    Warn users\n
    Allowed arguments:
    `event`: The event
    `user` (member): The user to warn
    `amount` (int): The amount of warns to give. Defaults to 1
    `invoker_username` (str): The user who warned someone
    `reason` (str): The reason for the warn
    """
    reason2 = " because of " + reason if reason else ""
    query = {"_id": user.id}
    if USER_DATA.count_documents(query) == 0:
        post = {"_id": user.id, "warns": amount}
        USER_DATA.insert_one(post)
        total_warns = amount
    else:
        user2 = USER_DATA.find(query)
        warns = 0
        try:
            for result in user2:
                warns = result["warns"]
        except KeyError:
            pass
        total_warns = warns + amount
        USER_DATA.update_one({"_id": user.id}, {"$set": {"warns": total_warns}})
    embed = nextcord.Embed(color=0x0DD91A)
    if total_warns <= 9:
        embed.add_field(
            name=f"{user} has been warned by {invoker_username}{reason2}",
            value=f"{user} has {10 - total_warns} warns left!",
            inline=False,
        )
        await event.channel.send(embed=embed)
    if total_warns >= 10:
        USER_DATA.update_one({"_id": user.id}, {"$set": {"warns": 0}})
        embed.add_field(
            name=f"{user} exceeded the warn limit!",
            value="He shall be punished with a 10 minute mute!",
            inline=False,
        )

        await event.channel.send(embed=embed)
        await user.edit(
            timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=1200)
        )
        await logger(ctx, f"{user} was muted for 10 minutes by Warn System")


async def logger(ctx: Context, message: str):
    """Log a message in the #logs channel"""
    logs_channel = nextcord.utils.get(ctx.guild.channels, name="logs")
    embed = nextcord.Embed(color=0x0DD91A, title=message)
    embed.set_footer(text=f'Used from the "{ctx.message.channel.name}" channel')
    await logs_channel.send(embed=embed)


@bot.event
async def on_ready():
    """Runs when the bot is online"""
    bl.info(f"Logged in as {bot.user}", __file__)
    cogs = os.listdir("cogs")
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
    birthday_checker.start()
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@tasks.loop(seconds=10)
async def birthday_checker():
    """Sends a message when it is someone's birthday"""
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
    """Processes messages"""
    if "Event Handler" not in bot.cogs:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: Context, error: commands.CommandError):
    """Processes command errors"""
    if "Event Handler" not in bot.cogs:
        bl.error(error, __file__)


@bot.command(name="load_cog", aliases=["lc"])
@commands.is_owner()
async def load_cog(ctx: Context, cog: str = None):
    """Loads a cog"""
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
            except Exception as e:
                print(e)
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


@bot.command(name="reloadcog", aliases=["rlc", "rc"])
async def reload_cog(ctx: Context, cog: str = None):
    """Reloads a cog"""
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
            except Exception as e:
                print(e)
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


@bot.command(name="unload_cog", aliases=["ulc", "uc"])
@commands.is_owner()
async def unload_cog(ctx: Context, cog: str = None):
    """Unloads a cog"""
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
            except Exception as e:
                print(e)
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


@bot.command(name="enable_command", aliases=["ec"])
@commands.is_owner()
async def enable_command(ctx: Context, *, command: str):
    """Enables a command"""
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


@bot.command(name="disable_command", aliases=["dc"])
@commands.is_owner()
async def disable_command(ctx: Context, *, command: str):
    """Disables a command"""
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
    for file in slash:
        if file.endswith(".py"):
            try:
                file2 = file.strip(".py")
                bot.load_extension(f"slash.{file2}")
                bl.debug(f"{file} loaded", __file__)
            except Exception as e:
                print(e)
                bl.error(f"{file} couldn't be loaded", __file__)

    context = os.listdir("context")
    for ctx in context:
        if ctx.endswith(".py"):
            try:
                ctx2 = ctx.strip(".py")
                bot.load_extension(f"context.{ctx2}")
                bl.debug(f"{ctx} loaded", __file__)
            except Exception as e:
                print(e)
                bl.error(f"{ctx} couldn't be loaded", __file__)

    bot.run(BOT_TOKEN)

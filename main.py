# TIJK-Bot is made and maintained by codeman1o1 (https://github.com/codeman1o1)

import asyncio
import datetime
import logging
import os
import re
import sys
import time

import coloredlogs
import nextcord
import nextcord.ext.commands.errors
from dotenv import load_dotenv
from nextcord import Interaction
from nextcord.ext import commands, tasks
from pydactyl import PterodactylClient
from pymongo import MongoClient

load_dotenv()
HYPIXEL_API_KEY = os.getenv("HypixelApiKey")
CLUSTER: MongoClient = MongoClient(os.getenv("MongoURL"))
DATA = CLUSTER["Data"]
BOT_DATA = DATA["BotData"]
USER_DATA = DATA["UserData"]
START_TIME = time.time()
SLASH_GUILDS = (870973430114181141, 865146077236822017)
PTD_SERVER_ID = os.getenv("PterodactylServerId")

PtdClient = PterodactylClient(
    "https://control.sparkedhost.us/", os.getenv("PterodactylApiKey")
)


def set_intents() -> nextcord.Intents:
    # pylint: disable=assigning-non-slot
    intents = nextcord.Intents.none()
    intents.guilds = True
    intents.members = True
    intents.bans = True
    intents.presences = True
    intents.messages = True
    intents.reactions = True
    intents.message_content = True
    return intents


bot = commands.Bot(intents=set_intents())


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        # 0 means block, anything else (e.g. 1) means allow
        allow = 1
        regexs = [
            r"^Shard ID (%s) has sent the (\w+) payload\.$",
            r"^Got a request to (%s) the websocket\.$",
            r"^Shard ID (%s) has connected to Gateway: (%s) \(Session ID: (%s)\)\.$",
            r"^Shard ID (%s) has successfully (\w+) session (%s) under trace (%s)\.$",
        ]
        for regex in regexs:
            if re.search(regex, record.msg):
                allow = 0
                break
        return allow


TEXT_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
handler = logging.FileHandler(filename="nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(TEXT_FORMAT))

logger = logging.getLogger("TIJK Bot")
logger.addHandler(handler)
coloredlogs.install(
    level=logging.DEBUG,
    logger=logger,
    fmt=TEXT_FORMAT,
)

nextcord_logger = logging.getLogger("nextcord")
nextcord_logger.addHandler(handler)
coloredlogs.install(
    level=logging.INFO,
    logger=nextcord_logger,
    fmt=TEXT_FORMAT,
)

for handler in logging.getLogger("nextcord").handlers:
    handler.addFilter(LogFilter())


async def warn_system(
    interaction: Interaction,
    user: nextcord.Member,
    amount: int = 1,
    invoker_username: str = "Warn System",
    reason: str = None,
    remove: bool = False,
):
    """
    Warns a user

    :param interaction: The interaction
    :type interaction: Interaction
    :param user: The user who is warned
    :type user: nextcord.Member
    :param amount: The amount of warns to give, defaults to 1
    :type amount: int, optional
    :param invoker_username: The user who warned a user, defaults to "Warn System"
    :type invoker_username: str, optional
    :param reason: The reason why the user was warned, defaults to None
    :type reason: str, optional
    :param remove: Wether to remove warns instead of adding them, defaults to False
    :type remove: bool, optional
    """
    # Can't place import on top because that would cause circular imports
    from utils.database import (  # pylint: disable=import-outside-toplevel
        get_user_data,
        set_user_data,
    )

    reason2 = f" because of {reason}" if reason else ""
    warns = get_user_data(user.id, "warns")
    total_warns = max(warns - amount, 0) if remove else warns + amount
    set_user_data(user_id=user.id, query="warns", value=total_warns)
    if not remove:
        await log(
            interaction,
            f"{user} has been warned {amount}x by {interaction.user}{reason2}",
        )
    else:
        await log(
            interaction, f"{amount} warn(s) have been removed from {user}{reason2}"
        )
    embed = nextcord.Embed(color=0x0DD91A)
    if total_warns <= 2:
        reason2 = f" because of {reason}" if reason else ""
        if not remove:
            embed.add_field(
                name=f"{user} has been warned by {invoker_username}{reason2}",
                value=f"{user} has {3 - total_warns} warns left!",
                inline=False,
            )
        else:
            embed.add_field(
                name=f"{user} now has {amount} warn(s) less {reason2}!",
                value=f"{user} now has a total of {total_warns} warn(s)!",
                inline=False,
            )
        await interaction.send(embed=embed)
    if total_warns >= 3:
        set_user_data(user.id, "warns", 0)
        embed.add_field(
            name=f"{user} exceeded the warn limit!",
            value="He shall be punished with an hour-long mute!",
            inline=False,
        )

        await user.timeout(nextcord.utils.utcnow() + datetime.timedelta(seconds=3600))

        await interaction.send(embed=embed)
        await log(
            interaction, f"{user} was muted for 10 minutes by Warn System{reason2}"
        )


async def log(interaction: nextcord.Interaction, message: str, channel: str = None):
    """Log a message in the #logs channel"""
    logs_channel = nextcord.utils.get(interaction.guild.channels, name="logs")
    embed = nextcord.Embed(color=0x0DD91A, title=message)
    embed.set_footer(
        text=f'Used from the "{channel or interaction.channel.name}" channel'
    )
    await logs_channel.send(embed=embed)


@bot.event
async def on_ready():
    """Runs when the bot is online"""
    logger.info("Logged in as %s", bot.user)
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog.strip('.py')}")
                logger.debug("%s loaded", cog)
            except Exception as e:  # pylint: disable=broad-except
                logger.error(e)
                logger.error("%s couldn't be loaded", cog)
    with open("spam_detect.txt", "a+", encoding="utf-8") as file:
        file.truncate(0)
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name="over the TIJK Server"
        )
    )
    birthday_checker.start()
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+", encoding="utf-8") as file:
            file.truncate(0)


@tasks.loop(seconds=10)
async def birthday_checker():
    """Sends a message when it is someone's birthday"""
    if time.strftime("%H") != "12":
        return

    birthdays = []
    today = datetime.date.today()
    year = today.year
    for user in USER_DATA.find():
        if "birthday" in user:
            birthday2 = user["birthday"].split("-")
            date = datetime.date(year, int(birthday2[1]), int(birthday2[0]))
            if today == date:
                birthdays.append(user["_id"])
    for user in birthdays:
        user = bot.get_user(user)
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Happy birthday {user.name} :tada:",
            value="We hope you will have a great day!",
            inline=False,
        )

        for guild in bot.guilds:
            if user in guild.members:
                await guild.system_channel.send(embed=embed)
    birthdays.clear()
    birthday_checker.cancel()


if __name__ == "__main__":
    slash = os.listdir("slash")
    slash.remove("custom_checks.py")
    for file in slash:
        if file.endswith(".py"):
            try:
                file2 = file.strip(".py")
                bot.load_extension(f"slash.{file2}")
                logger.debug("%s loaded", file)
            except Exception as e:  # pylint: disable=broad-except
                logger.error(e)
                logger.error("%s couldn't be loaded", file)

    bot.run(os.getenv("BotToken"))
    # Anything after this will get executed after the bot is shut down

    # Shutdown the host except if the user specified not to
    if "--no-stop" not in sys.argv[1:] and (
        PtdClient.client.servers.get_server_utilization(PTD_SERVER_ID)["current_state"]
        == "running"
    ):
        PtdClient.client.servers.send_power_action(PTD_SERVER_ID, "stop")

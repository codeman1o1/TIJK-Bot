# TIJK-Bot is made and maintained by codeman1o1 (https://github.com/codeman1o1)

import asyncio
import datetime
import logging
import os
import time

import coloredlogs
import nextcord
import nextcord.ext.commands.errors
from dotenv import load_dotenv
from nextcord import Interaction
from nextcord.ext import commands, tasks
from pymongo import MongoClient
from pydactyl import PterodactylClient

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

intents = nextcord.Intents.none()
intents.guilds = True
intents.members = True
intents.bans = True
intents.presences = True
intents.messages = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(intents=intents)


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        # 0 means block, anything else (e.g. 1) means allow
        return (
            0
            if any(
                blocked in str(record.msg).lower()
                for blocked in ("shard", "websocket", "payload")
            )
            else 1
        )


text_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
handler = logging.FileHandler(filename="nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter(text_format))

logger = logging.getLogger("TIJK Bot")
logger.addHandler(handler)
coloredlogs.install(
    level=logging.DEBUG,
    logger=logger,
    fmt=text_format,
)

nextcord_logger = logging.getLogger("nextcord")
nextcord_logger.addHandler(handler)
coloredlogs.install(
    level=logging.INFO,
    logger=nextcord_logger,
    fmt=text_format,
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

    Args:
        interaction (Interaction): The interaction
        user (nextcord.Member): The user who is warned
        amount (int, optional): The amount of warns to give. Defaults to 1.
        invoker_username (str, optional): The user who warned the user. Defaults to "Warn System".
        reason (str, optional): The reason why the user was warned. Defaults to None.
        remove (bool, optional): If warns should be removed instead of added. Defaults to False.
    """
    from utils.database import get_user_data, set_user_data

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
            except Exception as e:
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
                logger.debug(f"{file} loaded")
            except Exception as e:
                logger.error(e)
                logger.error(f"{file} couldn't be loaded")

    context = os.listdir("views/context_menus")
    for ctx in context:
        if ctx.endswith(".py"):
            try:
                ctx2 = ctx.strip(".py")
                bot.load_extension(f"views.context_menus.{ctx2}")
                logger.debug(f"{ctx} loaded")
            except Exception as e:
                logger.error(e)
                logger.error(f"{ctx} - context couldn't be loaded")

    bot.run(os.getenv("BotToken"))
    # Anything after this will get executed after the bot is shut down

    # Shutdown the host
    if (
        PtdClient.client.servers.get_server_utilization(PTD_SERVER_ID)["current_state"]
        == "running"
    ):
        PtdClient.client.servers.send_power_action(PTD_SERVER_ID, "stop")

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


async def message_filter(message):
    message = message.content.lower()
    message = message.replace(" ", "")
    message = message.replace(".", "")
    message = message.replace(",", "")
    message = message.replace("_", "")
    message = message.replace("@", "a")
    message = message.replace("ä", "a")
    message = message.replace("á", "a")
    message = message.replace("à", "a")
    message = message.replace("â", "a")
    message = message.replace("ã", "a")
    message = message.replace("å", "a")
    message = message.replace("ª", "a")
    message = message.replace("ą", "a")
    message = message.replace("ă", "a")
    message = message.replace("ā", "a")
    message = message.replace("æ", "a")
    message = message.replace("ß", "b")
    message = message.replace("þ", "b")
    message = message.replace("ç", "c")
    message = message.replace("ć", "c")
    message = message.replace("č", "c")
    message = message.replace("ď", "d")
    message = message.replace("đ", "d")
    message = message.replace("3", "e")
    message = message.replace("€", "e")
    message = message.replace("ë", "e")
    message = message.replace("ė", "e")
    message = message.replace("é", "e")
    message = message.replace("è", "e")
    message = message.replace("ê", "e")
    message = message.replace("ē", "e")
    message = message.replace("ę", "e")
    message = message.replace("ě", "e")
    message = message.replace("ĕ", "e")
    message = message.replace("ə", "e")
    message = message.replace("£", "f")
    message = message.replace("ģ", "g")
    message = message.replace("ğ", "g")
    message = message.replace("!", "i")
    message = message.replace("í", "i")
    message = message.replace("ì", "i")
    message = message.replace("ï", "i")
    message = message.replace("¡", "i")
    message = message.replace("î", "i")
    message = message.replace("ī", "i")
    message = message.replace("į", "i")
    message = message.replace("ķ", "k")
    message = message.replace("ĺ", "l")
    message = message.replace("ļ", "l")
    message = message.replace("ľ", "l")
    message = message.replace("ł", "l")
    message = message.replace("ñ", "n")
    message = message.replace("ń", "n")
    message = message.replace("ņ", "n")
    message = message.replace("ň", "n")
    message = message.replace("№", "n")
    message = message.replace("ö", "o")
    message = message.replace("ó", "o")
    message = message.replace("ò", "o")
    message = message.replace("ô", "o")
    message = message.replace("õ", "o")
    message = message.replace("ø", "o")
    message = message.replace("ō", "o")
    message = message.replace("ő", "o")
    message = message.replace("œ", "o")
    message = message.replace("•", "o")
    message = message.replace("○", "o")
    message = message.replace("●", "o")
    message = message.replace("ŕ", "r")
    message = message.replace("ř", "r")
    message = message.replace("$", "s")
    message = message.replace("§", "s")
    message = message.replace("ś", "s")
    message = message.replace("š", "s")
    message = message.replace("ş", "s")
    message = message.replace("ť", "t")
    message = message.replace("ț", "t")
    message = message.replace("ţ", "t")
    message = message.replace("ü", "u")
    message = message.replace("ū", "u")
    message = message.replace("ů", "u")
    message = message.replace("ű", "u")
    message = message.replace("ų", "u")
    message = message.replace("û", "u")
    message = message.replace("ù", "u")
    message = message.replace("ú", "u")
    message = message.replace("₩", "w")
    message = message.replace("ý", "y")
    message = message.replace("¥", "y")
    message = message.replace("ź", "z")
    message = message.replace("ż", "z")
    message = message.replace("ž", "z")
    message = message.encode("ascii", "ignore")
    message = message.decode()
    return message


@bot.event
async def on_ready():
    bl.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}", __file__)
    with open("spam_detect.txt", "r+") as file:
        file.truncate(0)
    cogs = os.listdir("cogs")
    try:
        cogs.remove("__pycache__")
    except ValueError:
        pass
    for c in cogs:
        try:
            c = c.strip(".py")
            bot.load_extension(f"cogs.{c}")
            bl.debug(f"{c}.py loaded!", __file__)
        except:
            bl.error(f"{c}.py couldn't be loaded!", __file__)
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
        documents = UserData.find()
        today = datetime.date.today()
        for k in documents:
            try:
                if k["birthday"]:
                    birthday2 = k["birthday"].split("-")
                    year = today.year
                    date = datetime.date(year, int(birthday2[1]), int(birthday2[0]))
                    if today == date:
                        birthdays.append(k["_id"])
            except KeyError:
                pass
        for member in birthdays:
            embed = nextcord.Embed(color=0x0DD91A)
            member = bot.get_user(member)
            embed.add_field(
                name=f"Happy birthday {member.name}!",
                value=f"We hope you will have a great day!",
                inline=False,
            )
            for guild in bot.guilds:
                await guild.system_channel.send(embed=embed)
        birthdays.clear()
        birthday_checker.cancel()


@bot.event
async def on_message(message):
    cancel = False
    counter = 0
    documents = BotData.find()
    for k in documents:
        forbidden_word_list = k["forbidden_words"]

    filtered_message = await message_filter(message)

    for file in message.attachments:
        if any(
            forbidden_word in file.filename for forbidden_word in forbidden_word_list
        ):
            cancel = True
            try:
                await message.delete()
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Hey, don't send that!",
                    value=f"Because of this action, you received 1 warn",
                    inline=True,
                )
                embed.set_footer(text="This message wil delete itself after 5 seconds")
                await message.channel.send(embed=embed, delete_after=5)
                query = {"_id": message.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": message.author.id, "warns": 1}
                    UserData.insert_one(post)
                    total_warns = 1
                else:
                    user2 = UserData.find(query)
                    warns = 0
                    try:
                        for result in user2:
                            warns = result["warns"]
                    except KeyError:
                        pass
                    warns = warns + 1
                    UserData.update_one(
                        {"_id": message.author.id}, {"$set": {"warns": warns}}
                    )
                    total_warns = warns
                embed = nextcord.Embed(color=0x0DD91A)
                if total_warns <= 8:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has {10 - total_warns} warns left!",
                        inline=False,
                    )
                if total_warns == 9:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                        inline=False,
                    )
                if total_warns >= 10:
                    query = {"_id": message.author.id}
                    if UserData.count_documents(query) == 0:
                        post = {"_id": message.author.id, "warns": 0}
                        UserData.insert_one(post)
                    else:
                        UserData.update_one(
                            {"_id": message.author.id}, {"$set": {"warns": 0}}
                        )
                    embed.add_field(
                        name=f"{message.author.display_name} exceeded the warn limit!",
                        value=f"He shall be punished with a 10 minute mute!",
                        inline=False,
                    )
                    await message.channel.send(embed=embed)
                    muted_role = nextcord.utils.get(
                        message.author.guild.roles, name="Muted"
                    )
                    if not muted_role in message.author.roles:
                        logs_channel = nextcord.utils.get(
                            message.author.guild.channels, name="logs"
                        )
                        await message.author.add_roles(muted_role)
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"User muted!",
                            value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                            inline=False,
                        )
                        await logs_channel.send(embed=embed)
                        await asyncio.sleep(600)
                        await message.author.remove_roles(muted_role)
                        embed = nextcord.Embed(
                            color=0x0DD91A,
                            title=f"{message.author.display_name} is now unmuted!",
                        )
                        await logs_channel.send(embed=embed)
            except nextcord.errors.NotFound:
                bl.warning(
                    f"Tried to delete message but message was not found", __file__
                )
        if file.filename.endswith((".exe", ".dll")):
            cancel = True
            try:
                await message.delete()
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Hey, don't send that!",
                    value=f"Because of this action, you received 1 warn",
                    inline=True,
                )
                embed.set_footer(text="This message wil delete itself after 5 seconds")
                await message.channel.send(embed=embed, delete_after=5)
                query = {"_id": message.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": message.author.id, "warns": 1}
                    UserData.insert_one(post)
                    total_warns = 1
                else:
                    user2 = UserData.find(query)
                    warns = 0
                    try:
                        for result in user2:
                            warns = result["warns"]
                    except KeyError:
                        pass
                    warns = warns + 1
                    UserData.update_one(
                        {"_id": message.author.id}, {"$set": {"warns": warns}}
                    )
                    total_warns = warns
                embed = nextcord.Embed(color=0x0DD91A)
                if total_warns <= 8:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has {10 - total_warns} warns left!",
                        inline=False,
                    )
                if total_warns == 9:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                        inline=False,
                    )
                if total_warns >= 10:
                    query = {"_id": message.author.id}
                    if UserData.count_documents(query) == 0:
                        post = {"_id": message.author.id, "warns": 0}
                        UserData.insert_one(post)
                    else:
                        UserData.update_one(
                            {"_id": message.author.id}, {"$set": {"warns": 0}}
                        )
                    embed.add_field(
                        name=f"{message.author.display_name} exceeded the warn limit!",
                        value=f"He shall be punished with a 10 minute mute!",
                        inline=False,
                    )
                    await message.channel.send(embed=embed)
                    muted_role = nextcord.utils.get(
                        message.author.guild.roles, name="Muted"
                    )
                    if not muted_role in message.author.roles:
                        logs_channel = nextcord.utils.get(
                            message.author.guild.channels, name="logs"
                        )
                        await message.author.add_roles(muted_role)
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"User muted!",
                            value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                            inline=False,
                        )
                        await logs_channel.send(embed=embed)
                        await asyncio.sleep(600)
                        await message.author.remove_roles(muted_role)
                        embed = nextcord.Embed(
                            color=0x0DD91A,
                            title=f"{message.author.display_name} is now unmuted!",
                        )
                        await logs_channel.send(embed=embed)
            except nextcord.errors.NotFound:
                bl.warning(
                    f"Tried to delete message but message was not found", __file__
                )

        if file.filename.endswith(".txt"):
            await file.save("file.txt")
            with open("file.txt") as f:
                lines = f.readlines()
                if any(
                    forbidden_word in lines for forbidden_word in forbidden_word_list
                ):
                    cancel = True
                    try:
                        await message.delete()
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"Hey, don't send that!",
                            value=f"Because of this action, you received 1 warn",
                            inline=True,
                        )
                        embed.set_footer(
                            text="This message wil delete itself after 5 seconds"
                        )
                        await message.channel.send(embed=embed, delete_after=5)
                        query = {"_id": message.author.id}
                        if UserData.count_documents(query) == 0:
                            post = {"_id": message.author.id, "warns": 1}
                            UserData.insert_one(post)
                            total_warns = 1
                        else:
                            user2 = UserData.find(query)
                            warns = 0
                            try:
                                for result in user2:
                                    warns = result["warns"]
                            except KeyError:
                                pass
                            warns = warns + 1
                            UserData.update_one(
                                {"_id": message.author.id}, {"$set": {"warns": warns}}
                            )
                            total_warns = warns
                        embed = nextcord.Embed(color=0x0DD91A)
                        if total_warns <= 8:
                            embed.add_field(
                                name=f"{message.author.display_name} has been warned by Warn System",
                                value=f"{message.author.display_name} has {10 - total_warns} warns left!",
                                inline=False,
                            )
                        if total_warns == 9:
                            embed.add_field(
                                name=f"{message.author.display_name} has been warned by Warn System",
                                value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                                inline=False,
                            )
                        if total_warns >= 10:
                            query = {"_id": message.author.id}
                            if UserData.count_documents(query) == 0:
                                post = {"_id": message.author.id, "warns": 0}
                                UserData.insert_one(post)
                            else:
                                UserData.update_one(
                                    {"_id": message.author.id}, {"$set": {"warns": 0}}
                                )
                            embed.add_field(
                                name=f"{message.author.display_name} exceeded the warn limit!",
                                value=f"He shall be punished with a 10 minute mute!",
                                inline=False,
                            )
                            await message.channel.send(embed=embed)
                            muted_role = nextcord.utils.get(
                                message.author.guild.roles, name="Muted"
                            )
                            if not muted_role in message.author.roles:
                                logs_channel = nextcord.utils.get(
                                    message.author.guild.channels, name="logs"
                                )
                                await message.author.add_roles(muted_role)
                                embed = nextcord.Embed(color=0x0DD91A)
                                embed.add_field(
                                    name=f"User muted!",
                                    value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                                    inline=False,
                                )
                                await logs_channel.send(embed=embed)
                                await asyncio.sleep(600)
                                await message.author.remove_roles(muted_role)
                                embed = nextcord.Embed(
                                    color=0x0DD91A,
                                    title=f"{message.author.display_name} is now unmuted!",
                                )
                                await logs_channel.send(embed=embed)
                    except nextcord.errors.NotFound:
                        bl.warning(
                            f"Tried to delete message but message was not found",
                            __file__,
                        )
                f.close()
            os.remove("file.txt")

    if any(
        forbidden_word in filtered_message for forbidden_word in forbidden_word_list
    ):
        cancel = True
        try:
            await message.delete()
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Hey, don't say that!",
                value=f"Because of this action, you received 1 warn",
                inline=True,
            )
            embed.set_footer(text="This message wil delete itself after 5 seconds")
            await message.channel.send(embed=embed, delete_after=5)
            query = {"_id": message.author.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": message.author.id, "warns": 1}
                UserData.insert_one(post)
                total_warns = 1
            else:
                user2 = UserData.find(query)
                warns = 0
                try:
                    for result in user2:
                        warns = result["warns"]
                except KeyError:
                    pass
                warns = warns + 1
                UserData.update_one(
                    {"_id": message.author.id}, {"$set": {"warns": warns}}
                )
                total_warns = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total_warns <= 8:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has {10 - total_warns} warns left!",
                    inline=False,
                )
            if total_warns == 9:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total_warns >= 10:
                query = {"_id": message.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": message.author.id, "warns": 0}
                    UserData.insert_one(post)
                else:
                    UserData.update_one(
                        {"_id": message.author.id}, {"$set": {"warns": 0}}
                    )
                embed.add_field(
                    name=f"{message.author.display_name} exceeded the warn limit!",
                    value=f"He shall be punished with a 10 minute mute!",
                    inline=False,
                )
                await message.channel.send(embed=embed)
                muted_role = nextcord.utils.get(
                    message.author.guild.roles, name="Muted"
                )
                if not muted_role in message.author.roles:
                    logs_channel = nextcord.utils.get(
                        message.author.guild.channels, name="logs"
                    )
                    await message.author.add_roles(muted_role)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await logs_channel.send(embed=embed)
                    await asyncio.sleep(600)
                    await message.author.remove_roles(muted_role)
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"{message.author.display_name} is now unmuted!",
                    )
                    await logs_channel.send(embed=embed)
        except nextcord.errors.NotFound:
            bl.warning(f"Tried to delete message but message was not found", __file__)

    if filtered_message == "banaan" or filtered_message == "banana":
        await message.channel.send(
            "https://i5.walmartimages.com/asr/209bb8a0-30ab-46be-b38d-58c2feb93e4a_1.1a15fb5bcbecbadd4a45822a11bf6257.jpeg"
        )
    if filtered_message == "bananen" or filtered_message == "bananas":
        await message.channel.send(
            "https://static.libertyprim.com/files/familles/banane-large.jpg?1569271725"
        )

    with open("spam_detect.txt", "r+") as file:
        if not message.author.bot:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1
            file.writelines(f"{str(message.author.id)}\n")
            if counter > 3:
                cancel = True
                query = {"_id": message.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": message.author.id, "warns": 1}
                    UserData.insert_one(post)
                    total_warns = 1
                else:
                    user2 = UserData.find(query)
                    warns = 0
                    try:
                        for result in user2:
                            warns = result["warns"]
                    except KeyError:
                        pass
                    warns = warns + 1
                    UserData.update_one(
                        {"_id": message.author.id}, {"$set": {"warns": warns}}
                    )
                    total_warns = warns
                embed = nextcord.Embed(color=0x0DD91A)
                if total_warns <= 8:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has {10 - total_warns} warns left!",
                        inline=False,
                    )
                if total_warns == 9:
                    embed.add_field(
                        name=f"{message.author.display_name} has been warned by Warn System",
                        value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                        inline=False,
                    )
                if total_warns >= 10:
                    query = {"_id": message.author.id}
                    if UserData.count_documents(query) == 0:
                        post = {"_id": message.author.id, "warns": 0}
                        UserData.insert_one(post)
                    else:
                        UserData.update_one(
                            {"_id": message.author.id}, {"$set": {"warns": 0}}
                        )
                    embed.add_field(
                        name=f"{message.author.display_name} exceeded the warn limit!",
                        value=f"He shall be punished with a 10 minute mute!",
                        inline=False,
                    )
                    await message.channel.send(embed=embed)
                    muted_role = nextcord.utils.get(
                        message.author.guild.roles, name="Muted"
                    )
                    if not muted_role in message.author.roles:
                        logs_channel = nextcord.utils.get(
                            message.author.guild.channels, name="logs"
                        )
                        await message.author.add_roles(muted_role)
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"User muted!",
                            value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                            inline=False,
                        )
                        await logs_channel.send(embed=embed)
                        await asyncio.sleep(600)
                        await message.author.remove_roles(muted_role)
                        embed = nextcord.Embed(
                            color=0x0DD91A,
                            title=f"{message.author.display_name} is now unmuted!",
                        )
                        await logs_channel.send(embed=embed)
                user = message.author
                muted_role = nextcord.utils.get(user.guild.roles, name="Muted")
                owner_role = nextcord.utils.get(user.guild.roles, name="Owner")
                admin_role = nextcord.utils.get(user.guild.roles, name="Admin")
                tijk_bot_developer_role = nextcord.utils.get(
                    user.guild.roles, name="TIJK-Bot developer"
                )
                anti_mute = (owner_role, admin_role, tijk_bot_developer_role)
                if not user.bot:
                    if any(role in user.roles for role in anti_mute):
                        return
                    else:
                        if muted_role in user.roles:
                            return
                        else:
                            await message.author.add_roles(muted_role)
                            embed = nextcord.Embed(color=0x0DD91A)
                            embed.add_field(
                                name=f"You ({message.author.display_name}) have been muted",
                                value=f"You have been muted for 5 minutes.\nIf you think this was a mistake, please contact an owner or admin\nBecause of this action, you received 1 warn",
                                inline=True,
                            )
                            await message.channel.send(embed=embed)
                            await asyncio.sleep(300)
                            await user.remove_roles(muted_role)
                            embed = nextcord.Embed(color=0x0DD91A)
                            embed.add_field(
                                name=f"{message.author.display_name} is now unmuted",
                                value=f"You have been unmuted. Please don't spam again!",
                                inline=True,
                            )
                            await message.channel.send(embed=embed)
    if not cancel:
        if not message.author.bot:
            if not message.content.startswith(".."):
                await bot.process_commands(message)
    user = bot.get_user(message.author.id)
    if not user is None:
        query = {"_id": message.author.id}
        if UserData.count_documents(query) == 0:
            post = {"_id": message.author.id, "messages": 1}
            UserData.insert_one(post)
        else:
            user = UserData.find(query)
            messages = 0
            try:
                for result in user:
                    messages = result["messages"]
            except KeyError:
                pass
            messages = messages + 1
            UserData.update_one(
                {"_id": message.author.id}, {"$set": {"messages": messages}}
            )


@bot.event
async def on_message_edit(before, after):
    documents = BotData.find()
    for k in documents:
        forbidden_list = k["forbidden_words"]

    filtered_message = await message_filter(after)

    for file in after.attachments:
        if file.filename.endswith((".exe", ".dll")):
            try:
                await after.delete()
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Hey, don't send that!",
                    value=f"Because of this action, you received 1 warn",
                    inline=True,
                )
                embed.set_footer(text="This message wil delete itself after 5 seconds")
                await after.channel.send(embed=embed, delete_after=5)
                query = {"_id": after.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": after.author.id, "warns": 1}
                    UserData.insert_one(post)
                    total_warns = 1
                else:
                    user2 = UserData.find(query)
                    warns = 0
                    try:
                        for result in user2:
                            warns = result["warns"]
                    except KeyError:
                        pass
                    warns = warns + 1
                    UserData.update_one(
                        {"_id": after.author.id}, {"$set": {"warns": warns}}
                    )
                    total_warns = warns
                embed = nextcord.Embed(color=0x0DD91A)
                if total_warns <= 8:
                    embed.add_field(
                        name=f"{after.author.display_name} has been warned by Warn System",
                        value=f"{after.author.display_name} has {10 - total_warns} warns left!",
                        inline=False,
                    )
                if total_warns == 9:
                    embed.add_field(
                        name=f"{after.author.display_name} has been warned by Warn System",
                        value=f"{after.author.display_name} has no more warns left! Next time, he shall be punished!",
                        inline=False,
                    )
                if total_warns >= 10:
                    query = {"_id": after.author.id}
                    if UserData.count_documents(query) == 0:
                        post = {"_id": after.author.id, "warns": 0}
                        UserData.insert_one(post)
                    else:
                        UserData.update_one(
                            {"_id": after.author.id}, {"$set": {"warns": 0}}
                        )
                    embed.add_field(
                        name=f"{after.author.display_name} exceeded the warn limit!",
                        value=f"He shall be punished with a 10 minute mute!",
                        inline=False,
                    )
                    await after.channel.send(embed=embed)
                    muted_role = nextcord.utils.get(
                        after.author.guild.roles, name="Muted"
                    )
                    if not muted_role in after.author.roles:
                        logs_channel = nextcord.utils.get(
                            after.author.guild.channels, name="logs"
                        )
                        await after.author.add_roles(muted_role)
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"User muted!",
                            value=f"{after.author.display_name} was muted for 10 minutes by Warn System",
                            inline=False,
                        )
                        await logs_channel.send(embed=embed)
                        await asyncio.sleep(600)
                        await after.author.remove_roles(muted_role)
                        embed = nextcord.Embed(
                            color=0x0DD91A,
                            title=f"{after.author.display_name} is now unmuted!",
                        )
                        await logs_channel.send(embed=embed)
            except nextcord.errors.NotFound:
                bl.warning(
                    f"Tried to delete message but message was not found", __file__
                )

    if any(forbidden_word in filtered_message for forbidden_word in forbidden_list):
        try:
            await after.delete()
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Hey, don't say that!",
                value=f"Because of this action, you received 1 warn",
                inline=True,
            )
            embed.set_footer(text="This message wil delete itself after 5 seconds")
            await after.channel.send(embed=embed, delete_after=5)
            query = {"_id": after.author.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": after.author.id, "warns": 1}
                UserData.insert_one(post)
                total_warns = 1
            else:
                user2 = UserData.find(query)
                warns = 0
                try:
                    for result in user2:
                        warns = result["warns"]
                except KeyError:
                    pass
                warns = warns + 1
                UserData.update_one(
                    {"_id": after.author.id}, {"$set": {"warns": warns}}
                )
                total_warns = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total_warns <= 8:
                embed.add_field(
                    name=f"{after.author.display_name} has been warned by Warn System",
                    value=f"{after.author.display_name} has {10 - total_warns} warns left!",
                    inline=False,
                )
            if total_warns == 9:
                embed.add_field(
                    name=f"{after.author.display_name} has been warned by Warn System",
                    value=f"{after.author.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total_warns >= 10:
                query = {"_id": after.author.id}
                if UserData.count_documents(query) == 0:
                    post = {"_id": after.author.id, "warns": 0}
                    UserData.insert_one(post)
                else:
                    UserData.update_one(
                        {"_id": after.author.id}, {"$set": {"warns": 0}}
                    )
                embed.add_field(
                    name=f"{after.author.display_name} exceeded the warn limit!",
                    value=f"He shall be punished with a 10 minute mute!",
                    inline=False,
                )
                await after.channel.send(embed=embed)
                muted_role = nextcord.utils.get(after.author.guild.roles, name="Muted")
                if not muted_role in after.author.roles:
                    logs_channel = nextcord.utils.get(
                        after.author.guild.channels, name="logs"
                    )
                    await after.author.add_roles(muted_role)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{after.author.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await logs_channel.send(embed=embed)
                    await asyncio.sleep(600)
                    await after.author.remove_roles(muted_role)
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"{after.author.display_name} is now unmuted!",
                    )
                    await logs_channel.send(embed=embed)
        except nextcord.errors.NotFound:
            bl.warning(f"Tried to delete message but message was not found", __file__)


@bot.event
async def on_member_join(member):
    user = bot.get_user(member.id)
    dm = await user.create_dm()
    embed = nextcord.Embed(
        color=0x0DD91A,
        title=f"Hey {member.display_name} :wave:\nWelcome to {member.guild.name}!\nWe hope you enjoy your stay!",
    )
    await dm.send(embed=embed)
    if member.guild.system_channel:
        await member.guild.system_channel.send(embed=embed)
    if not member.bot:
        member_role = nextcord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(member_role)
    elif member.bot:
        bot_role = nextcord.utils.get(member.guild.roles, name="Bot")
        await member.add_roles(bot_role)


@bot.event
async def on_member_update(before, after):
    tijk_bot_developer_role = nextcord.utils.get(
        after.guild.roles, name="TIJK-Bot developer"
    )
    if tijk_bot_developer_role in after.roles:
        info = await bot.application_info()
        owner = await commands.converter.UserConverter().convert(after, str(info.owner))
        if not after.id == owner.id:
            await after.remove_roles(tijk_bot_developer_role)
    if after.nick:
        owner_role = nextcord.utils.get(before.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(before.guild.roles, name="Admin")
        roles = (owner_role, admin_role)
        admin_names = [
            [str(user.name), str(user.display_name)]
            for user in before.guild.members
            if any(role in user.roles for role in roles)
        ]
        admin_names = sum(admin_names, [])
        admin_roles = (owner_role, admin_role)
        if not any(admin_role in after.roles for admin_role in admin_roles):
            if after.nick in admin_names:
                try:
                    user = bot.get_user(int(after.id))
                    if before.nick:
                        await after.edit(nick=before.nick)
                    else:
                        await after.edit(nick=before.name)
                    query = {"_id": after.id}
                    if UserData.count_documents(query) == 0:
                        post = {"_id": after.id, "warns": 1}
                        UserData.insert_one(post)
                    else:
                        user = UserData.find(query)
                        warns = 0
                        try:
                            for result in user:
                                warns = result["warns"]
                        except KeyError:
                            pass
                        warns = warns + 1
                        UserData.update_one(
                            {"_id": after.id}, {"$set": {"warns": warns}}
                        )
                except nextcord.Forbidden:
                    bl.error(f"Couldn't change nickname", __file__)
        admin_names.clear()


@bot.event
async def on_member_remove(member):
    user = bot.get_user(member.id)
    dm = await user.create_dm()
    embed = nextcord.Embed(
        color=0x0DD91A,
        title=f"Bye {member.display_name} :wave:\nIt was great having you!!",
    )
    await dm.send(embed=embed)
    if member.guild.system_channel:
        await member.guild.system_channel.send(embed=embed)


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
        await ctx.send(embed=embed)
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.load_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully loaded {cog.lower()}.py"
        )
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
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.reload_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully reloaded {cog.lower()}.py"
        )
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
            cogs.remove("role_view.py")
        except ValueError:
            pass
        for cog in cogs:
            cog = cogs.strip(".py")
            bot.unload_extension(f"cogs.{cog}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been unloaded!")
    else:
        if cog.lower() == "dev":
            cog = "developer"
        bot.unload_extension(f"cogs.{cog.lower()}")
        embed = nextcord.Embed(
            color=0x0DD91A, title=f"Succesfully unloaded {cog.lower()}.py!"
        )
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
        else:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"The .{command.qualified_name} command is already disabled!",
            )
    if command in disable_prevention:
        embed = nextcord.Embed(color=0x0DD91A, title="Root commands can't be disabled!")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    embed = nextcord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"An error occured!",
        value=f"{error}",
        inline=True,
    )
    await ctx.send(embed=embed)
    bl.error(error, "error-handler")


bot.run(os.environ["BotToken"])

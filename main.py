# TIJK-Bot is made and maintaned by codeman1o1 (https://github.com/codeman1o1)

import os
from dotenv import load_dotenv
import asyncio
import nextcord
from nextcord.ext import commands
import nextcord.ext.commands.errors
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
    print(f"Logged in as:\n{bot.user.name}")
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
            print(f"{c}.py loaded!")
        except:
            print(f"{c}.py couldn't be loaded!")
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name="the TIJK Server"
        )
    )
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@bot.event
async def on_message(message):
    cancel = False
    counter = 0
    abuse_list = ["abuse", "misbruik"]
    message0 = message.content.lower()
    message1 = message0.replace(" ", "")
    message2 = message1.replace("@", "a")
    message3 = message2.replace("3", "e")
    message4 = message3.replace("$", "s")
    message5 = message4.replace("!", "i")
    message6 = message5.replace(".", "")
    message7 = message6.replace("_", "")
    message8 = message7.replace("ä", "a")
    message9 = message8.replace("á", "a")
    message10 = message9.replace("à", "a")
    message11 = message10.replace("â", "a")
    message12 = message11.replace("ã", "a")
    message13 = message12.replace("å", "a")
    message14 = message13.replace("ª", "a")
    message15 = message14.replace("ą", "a")
    message16 = message15.replace("ă", "a")
    message17 = message16.replace("ā", "a")
    message18 = message17.replace("æ", "a")
    message19 = message18.replace("æ", "e")
    message20 = message19.replace("ü", "u")
    message21 = message20.replace("ū", "u")
    message22 = message21.replace("ů", "u")
    message23 = message22.replace("ű", "u")
    message24 = message23.replace("ų", "u")
    message25 = message24.replace("û", "u")
    message26 = message25.replace("ù", "u")
    message27 = message26.replace("ú", "u")
    message28 = message27.replace("ß", "b")
    message29 = message28.replace("§", "s")
    message30 = message29.replace("ś", "s")
    message31 = message30.replace("š", "s")
    message32 = message31.replace("ş", "s")
    message33 = message32.replace("ë", "e")
    message34 = message33.replace("ė", "e")
    message35 = message34.replace("é", "e")
    message36 = message35.replace("è", "e")
    message37 = message36.replace("ê", "e")
    message38 = message37.replace("ē", "e")
    message39 = message38.replace("ę", "e")
    message40 = message39.replace("ě", "e")
    message41 = message40.replace("ĕ", "e")
    message42 = message41.replace("ə", "e")
    message43 = message42.replace("í", "i")
    message44 = message43.replace("ì", "i")
    message45 = message44.replace("ï", "i")
    message46 = message45.replace("¡", "i")
    message47 = message46.replace("î", "i")
    message_final1 = message47.encode("ascii", "ignore")
    message_final2 = message_final1.decode()

    for file in message.attachments:
        if file.filename.endswith((".exe", ".dll")):
            cancel = True
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
                total = 1
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
                total = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total <= 8:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has {10 - total} warns left!",
                    inline=False,
                )
            if total == 9:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total >= 10:
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
                muted = nextcord.utils.get(message.author.guild.roles, name="Muted")
                if not muted in message.author.roles:
                    mo = nextcord.utils.get(
                        message.author.guild.channels, name="moderator-only"
                    )
                    await message.author.add_roles(muted)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await mo.send(embed=embed)
                    await asyncio.sleep(600)
                    await message.author.remove_roles(muted)
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"{message.author.display_name} is now unmuted!",
                    )
                    await mo.send(embed=embed)

    if any(abuse in message_final2 for abuse in abuse_list):
        cancel = True
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Hey, don't say that!",
            value=f"Because of this action, you received 1 warn",
            inline=True,
        )
        embed.set_footer(text="This message wil delete itself after 5 seconds")
        await message.channel.send(embed=embed, delete_after=5)
        await message.delete()
        query = {"_id": message.author.id}
        if UserData.count_documents(query) == 0:
            post = {"_id": message.author.id, "warns": 1}
            UserData.insert_one(post)
            total = 1
        else:
            user2 = UserData.find(query)
            warns = 0
            try:
                for result in user2:
                    warns = result["warns"]
            except KeyError:
                pass
            warns = warns + 1
            UserData.update_one({"_id": message.author.id}, {"$set": {"warns": warns}})
            total = warns
        embed = nextcord.Embed(color=0x0DD91A)
        if total <= 8:
            embed.add_field(
                name=f"{message.author.display_name} has been warned by Warn System",
                value=f"{message.author.display_name} has {10 - total} warns left!",
                inline=False,
            )
        if total == 9:
            embed.add_field(
                name=f"{message.author.display_name} has been warned by Warn System",
                value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                inline=False,
            )
        if total >= 10:
            query = {"_id": message.author.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": message.author.id, "warns": 0}
                UserData.insert_one(post)
            else:
                UserData.update_one({"_id": message.author.id}, {"$set": {"warns": 0}})
            embed.add_field(
                name=f"{message.author.display_name} exceeded the warn limit!",
                value=f"He shall be punished with a 10 minute mute!",
                inline=False,
            )
            await message.channel.send(embed=embed)
            muted = nextcord.utils.get(message.author.guild.roles, name="Muted")
            if not muted in message.author.roles:
                mo = nextcord.utils.get(
                    message.author.guild.channels, name="moderator-only"
                )
                await message.author.add_roles(muted)
                embed = nextcord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"User muted!",
                    value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                    inline=False,
                )
                await mo.send(embed=embed)
                await asyncio.sleep(600)
                await message.author.remove_roles(muted)
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f"{message.author.display_name} is now unmuted!",
                )
                await mo.send(embed=embed)

    if message.content.lower() == "banaan" or message.content.lower() == "banana":
        await message.channel.send(
            "https://i5.walmartimages.com/asr/209bb8a0-30ab-46be-b38d-58c2feb93e4a_1.1a15fb5bcbecbadd4a45822a11bf6257.jpeg"
        )
    if message.content.lower() == "bananen" or message.content.lower() == "bananas":
        await message.channel.send(
            "https://static.libertyprim.com/files/familles/banane-large.jpg?1569271725"
        )

    with open("spam_detect.txt", "r+") as file:
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
                total = 1
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
                total = warns
            embed = nextcord.Embed(color=0x0DD91A)
            if total <= 8:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has {10 - total} warns left!",
                    inline=False,
                )
            if total == 9:
                embed.add_field(
                    name=f"{message.author.display_name} has been warned by Warn System",
                    value=f"{message.author.display_name} has no more warns left! Next time, he shall be punished!",
                    inline=False,
                )
            if total >= 10:
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
                muted = nextcord.utils.get(message.author.guild.roles, name="Muted")
                if not muted in message.author.roles:
                    mo = nextcord.utils.get(
                        message.author.guild.channels, name="moderator-only"
                    )
                    await message.author.add_roles(muted)
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted!",
                        value=f"{message.author.display_name} was muted for 10 minutes by Warn System",
                        inline=False,
                    )
                    await mo.send(embed=embed)
                    await asyncio.sleep(600)
                    await message.author.remove_roles(muted)
                    embed = nextcord.Embed(
                        color=0x0DD91A,
                        title=f"{message.author.display_name} is now unmuted!",
                    )
                    await mo.send(embed=embed)
            user = message.author
            muted = nextcord.utils.get(user.guild.roles, name="Muted")
            owner = nextcord.utils.get(user.guild.roles, name="Owner")
            admin = nextcord.utils.get(user.guild.roles, name="Admin")
            tbdv = nextcord.utils.get(user.guild.roles, name="TIJK-Bot developer")
            anti_mute = [owner, admin, tbdv]
            if not user.bot:
                if any(role in user.roles for role in anti_mute):
                    return
                else:
                    if muted in user.roles:
                        return
                    else:
                        await message.author.add_roles(muted)
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"You ({message.author.display_name}) have been muted",
                            value=f"You have been muted for 5 minutes.\nIf you think this was a mistake, please contact an owner or admin\nBecause of this action, you received 1 warn",
                            inline=True,
                        )
                        await message.channel.send(embed=embed)
                        await asyncio.sleep(300)
                        await user.remove_roles(muted)
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
    abuse_list = ["abuse", "misbruik"]
    message0 = after.content.lower()
    message1 = message0.replace(" ", "")
    message2 = message1.replace("@", "a")
    message3 = message2.replace("3", "e")
    message4 = message3.replace("$", "s")
    message5 = message4.replace("!", "i")
    message6 = message5.replace(".", "")
    message7 = message6.replace("_", "")
    message8 = message7.replace("ä", "a")
    message9 = message8.replace("á", "a")
    message10 = message9.replace("à", "a")
    message11 = message10.replace("â", "a")
    message12 = message11.replace("ã", "a")
    message13 = message12.replace("å", "a")
    message14 = message13.replace("ª", "a")
    message15 = message14.replace("ą", "a")
    message16 = message15.replace("ă", "a")
    message17 = message16.replace("ā", "a")
    message18 = message17.replace("æ", "a")
    message19 = message18.replace("æ", "e")
    message20 = message19.replace("ü", "u")
    message21 = message20.replace("ū", "u")
    message22 = message21.replace("ů", "u")
    message23 = message22.replace("ű", "u")
    message24 = message23.replace("ų", "u")
    message25 = message24.replace("û", "u")
    message26 = message25.replace("ù", "u")
    message27 = message26.replace("ú", "u")
    message28 = message27.replace("ß", "b")
    message29 = message28.replace("§", "s")
    message30 = message29.replace("ś", "s")
    message31 = message30.replace("š", "s")
    message32 = message31.replace("ş", "s")
    message33 = message32.replace("ë", "e")
    message34 = message33.replace("ė", "e")
    message35 = message34.replace("é", "e")
    message36 = message35.replace("è", "e")
    message37 = message36.replace("ê", "e")
    message38 = message37.replace("ē", "e")
    message39 = message38.replace("ę", "e")
    message40 = message39.replace("ě", "e")
    message41 = message40.replace("ĕ", "e")
    message42 = message41.replace("ə", "e")
    message43 = message42.replace("í", "i")
    message44 = message43.replace("ì", "i")
    message45 = message44.replace("ï", "i")
    message46 = message45.replace("¡", "i")
    message47 = message46.replace("î", "i")
    message_final1 = message47.encode("ascii", "ignore")
    message_final2 = message_final1.decode()

    for file in after.attachments:
        if file.filename.endswith((".exe", ".dll")):
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
                    {"_id": after.author.id}, {"$set": {"warns": warns}}
                )

    if any(abuse in message_final2 for abuse in abuse_list):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Hey, don't say that!",
            value=f"Because of this action, you received 1 warn",
            inline=True,
        )
        embed.set_footer(text="This message wil delete itself after 5 seconds")
        await after.channel.send(embed=embed, delete_after=5)
        await after.delete()
        query = {"_id": after.author.id}
        if UserData.count_documents(query) == 0:
            post = {"_id": after.author.id, "warns": 1}
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
            UserData.update_one({"_id": after.author.id}, {"$set": {"warns": warns}})


@bot.event
async def on_member_join(member):
    embed = nextcord.Embed(
        title=f"Hey {member.display_name} :wave:\nWe hope you enjoy your stay!"
    )
    await member.channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    tbdv = nextcord.utils.get(after.guild.roles, name="TIJK-Bot developer")
    if tbdv in after.roles:
        if not after.id == 656950082431615057:
            await after.remove_roles(tbdv)
    admins = []
    if after.nick:
        nick = after.nick
        for user in before.guild.members:
            owner = nextcord.utils.get(user.guild.roles, name="Owner")
            admin = nextcord.utils.get(user.guild.roles, name="Admin")
            roles = [owner, admin]
            if any(role in user.roles for role in roles):
                admins.append(str(user.name))
                admins.append(str(user.display_name))
        adminsR = [owner, admin]
        if not any(admin in after.roles for admin in adminsR):
            if not after.bot:
                if after.nick in admins:
                    try:
                        user = bot.get_user(int(after.id))
                        if before.nick:
                            await after.edit(nick=before.nick)
                        else:
                            await after.edit(nick=before.name)
                        embed = nextcord.Embed(
                            color=0x0DD91A,
                            title=f"Because you tried to change your username to an admin ({nick}) in {after.guild}, you received 1 warn",
                        )
                        await user.send(embed=embed)
                        query = {"_id": after.author.id}
                        if UserData.count_documents(query) == 0:
                            post = {"_id": after.author.id, "warns": 1}
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
                                {"_id": after.author.id}, {"$set": {"warns": warns}}
                            )
                    except nextcord.Forbidden:
                        pass
    admins.clear()


@bot.command(
    name="load_cog", description="Loads a cog", brief="Loads a cog", aliases=["lc"]
)
@commands.is_owner()
async def load_cog(ctx, cog: str = None):
    c = os.listdir("cogs")
    c.remove("__pycache__")
    c = str(c)
    c = c.replace(".py", "")
    c = c.replace("[", "")
    c = c.replace("]", "")
    c = c.replace("'", "")
    c = c.replace(",", "\n>")
    if cog == None:
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {c}",
            inline=False,
        )
        await ctx.send(embed=embed)
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for c in cogs:
            c = c.strip(".py")
            bot.load_extension(f"cogs.{c}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been loaded!")
        await ctx.send(embed=embed)
    else:
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
    c = os.listdir("cogs")
    c.remove("__pycache__")
    c = str(c)
    c = c.replace(".py", "")
    c = c.replace("[", "")
    c = c.replace("]", "")
    c = c.replace("'", "")
    c = c.replace(",", "\n>")
    if cog == None:
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {c}",
            inline=False,
        )
        await ctx.send(embed=embed)
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for c in cogs:
            c = c.strip(".py")
            bot.reload_extension(f"cogs.{c}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been reloaded!")
        await ctx.send(embed=embed)
    else:
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
    c = os.listdir("cogs")
    c.remove("__pycache__")
    c = str(c)
    c = c.replace(".py", "")
    c = c.replace("[", "")
    c = c.replace("]", "")
    c = c.replace("'", "")
    c = c.replace(",", "\n>")
    if cog == None:
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The available cogs are:",
            value=f"> all\n> {c}",
            inline=False,
        )
        await ctx.send(embed=embed)
    elif cog.lower() == "all":
        cogs = os.listdir("cogs")
        try:
            cogs.remove("__pycache__")
        except ValueError:
            pass
        for c in cogs:
            c = c.strip(".py")
            bot.unload_extension(f"cogs.{c}")
        embed = nextcord.Embed(color=0x0DD91A, title=f"All cogs have been unloaded!")
        await ctx.send(embed=embed)
    else:
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
    command2 = command
    command = bot.get_command(command)
    if command == None:
        embed = nextcord.Embed(
            color=0x0DD91A,
        )
        embed.add_field(
            name="An error occured!",
            value=f'Command "{str(command2)}" is not found',
            inline=True,
        )
    if not command.enabled:
        command.enabled = True
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"The .{command.qualified_name} command is now enabled!",
        )
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
    command2 = command
    command = bot.get_command(command)
    cogLoad = bot.get_command("load_cog")
    cogUnload = bot.get_command("unload_cog")
    cmdLoad = bot.get_command("load_command")
    cmdUnload = bot.get_command("unload_command")
    antiDisable = [cogLoad, cogUnload, cmdLoad, cmdUnload]
    if command == None:
        embed = nextcord.Embed(
            color=0x0DD91A,
        )
        embed.add_field(
            name="An error occured!",
            value=f'Command "{str(command2)}" is not found',
            inline=True,
        )
    elif not command in antiDisable:
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
    else:
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


bot.run(os.environ["BotToken"])

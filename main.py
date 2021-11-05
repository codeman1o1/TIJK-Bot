import keep_alive
import sys
import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
import discord.ext.commands.errors
import random
import aiohttp
import requests
import urllib

client = discord.Client()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot.remove_command("help")

hpon = []
admins = []


@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}".format(bot))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="the TIJK Server"
        )
    )
    while True:
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@bot.event
async def on_message(message):
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
            await message.delete()
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Hey, don't send that!",
                value=f"This message wil delete itself after 5 seconds",
                inline=True,
            )
            await message.channel.send(embed=embed, delete_after=5)

    if any(abuse in message_final2 for abuse in abuse_list):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Hey, don't say that!",
            value=f"This message wil delete itself after 5 seconds",
            inline=True,
        )
        await message.channel.send(embed=embed, delete_after=5)
        await message.delete()

    if message.author.id == 861994137413484607:
        return

    if "youtube.com/watch?v=dQw4w9WgXcQ" in message.content.lower():
        await message.delete()
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Rick Roll alert!",
            value=f"This message wil delete itself after 5 seconds",
            inline=True,
        )
        await message.channel.send(embed=embed, delete_after=5)

    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter += 1
        file.writelines(f"{str(message.author.id)}\n")
        if counter > 5:
            user = message.author
            muted = discord.utils.find(lambda r: r.name == "Muted", user.guild.roles)
            owner = discord.utils.find(lambda r: r.name == "Owner", user.guild.roles)
            admin = discord.utils.find(lambda r: r.name == "Admin", user.guild.roles)
            tb_dv = discord.utils.find(
                lambda r: r.name == "TIJK-Bot developer", user.guild.roles
            )
            anti_mute = [owner, admin, tb_dv]
            if any(role in user.roles for role in anti_mute):
                return
            else:
                if muted in user.roles:
                    return
                else:
                    await message.author.add_roles(muted)
                    embed = discord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User muted",
                        value=f"You have been muted for 5 minutes.\nIf you think this was a mistake, please contact JustIanJ or codeman1o1",
                        inline=True,
                    )
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(300)
                    await user.remove_roles(muted)
                    embed = discord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"User unmuted",
                        value=f"You have been unmuted. Please don't spam again!",
                        inline=True,
                    )
                    await message.channel.send(embed=embed)
    await bot.process_commands(message)


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
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Hey, don't send that!",
                value=f"This message wil delete itself after 5 seconds",
                inline=True,
            )
            await after.channel.send(embed=embed, delete_after=5)

    if any(abuse in message_final2 for abuse in abuse_list):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Hey, don't say that!",
            value=f"This message wil delete itself after 5 seconds",
            inline=True,
        )
        await after.channel.send(embed=embed, delete_after=5)
        await after.delete()

    if after.author.id == 861994137413484607:
        return

    if "youtube.com/watch?v=dQw4w9WgXcQ" in after.content.lower():
        await after.delete()
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Rick Roll alert!",
            value=f"This message wil delete itself after 5 seconds",
            inline=True,
        )
        await after.channel.send(embed=embed, delete_after=5)
    await bot.process_commands(after)


@bot.event
async def on_member_update(before, after):
    if after.nick:
        for user in before.guild.members:
            owner = discord.utils.find(lambda r: r.name == "Owner", user.guild.roles)
            admin = discord.utils.find(lambda r: r.name == "Admin", user.guild.roles)
            roles = [owner, admin]
            if any(role in user.roles for role in roles):
                admins.append(str(user.name))
                admins.append(str(user.display_name))
        if any(role.lower() in after.nick.lower() for role in admins):
            if before.nick:
                await after.edit(nick=before.nick)
            else:
                await after.edit(nick=before.name)
    admins.clear()


@bot.command(name="website")
async def website(ctx):
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Visit the official TIJK Bot website now!",
        value=f"https://tijk-bot.codeman1o1.repl.co",
        inline=False,
    )
    await ctx.send(embed=embed)


@bot.command(
    name="github", aliases=["git", "os", "opensource", "open-source", "source"]
)
async def website(ctx):
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"View the official TIJK Bot code now!",
        value=f"https://github.com/codeman1o1/TIJK-Bot",
        inline=False,
    )
    await ctx.send(embed=embed)


@bot.command(name="debug")
@commands.is_owner()
async def debug(ctx, codes=""):
    if codes == "codes":
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"The status codes are the following:",
            value=f"> 200: Ok\n> 301: Permanent Redirect\n> 302: Temporary Redirect\n> 404: Not Found\n> 410: Gone\n> 500: Internal Server Error\n> 503: Service Unavailable",
            inline=False,
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
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
            response = urllib.request.urlopen("https://TIJK-Music.codeman1o1.repl.co")
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


@bot.command(name="api")
async def api(ctx, type: str = "help", *, subtype: str = ""):
    types = ["help", "animal", "mc", "joke", "pokedex", "pd", "lyrics", "meme"]
    type = type.lower()
    subtype = subtype.lower()
    if type in types:
        if type == "help":
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Help with the .api command",
                value=f"The .api command gets information from API's.\n**I do not own the API's so I can't help you with something if it is a problem with the API!!**\nThe current available commands are:\n> animal\n> minecraft/mc\n> joke\n> pokedex/pd\n> meme",
                inline=False,
            )
            await ctx.send(embed=embed)
        if type == "animal":
            animals = ["dog", "cat", "panda", "red_panda", "bird", "fox", "koala"]
            subtype = subtype.replace(" ", "_")
            if subtype.lower() in animals:
                async with aiohttp.ClientSession() as session:
                    request = await session.get(
                        f"https://some-random-api.ml/img/{subtype}"
                    )
                    info = await request.json()
                await ctx.send(info["link"])
            else:
                if subtype == "":
                    subtype = "That"
                embed = discord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Can't request image!",
                    value=f"{subtype} is not a valid animal type **for the API**\nValid animal types are:\n> Dog\n> Cat\n> Panda\n> Red Panda\n> Bird\n> Fox\n> Koala",
                    inline=False,
                )
                await ctx.send(embed=embed)
        if type == "minecraft" or type == "mc":
            try:
                async with aiohttp.ClientSession() as session:
                    request = await session.get(
                        f"https://some-random-api.ml/mc?username={subtype}"
                    )
                    info = await request.json()
                name_history = info["name_history"]
                for i in name_history:
                    if "[{" in str(name_history):
                        name_history = ""
                    name_history = (
                        str(name_history)
                        + "\nName: "
                        + i["name"]
                        + "\nChanged at: "
                        + i["changedToAt"]
                        + "\n"
                    )
                embed = discord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Username",
                    value=info["username"],
                    inline=False,
                )
                embed.add_field(
                    name=f"UUID",
                    value=info["uuid"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Name History",
                    value=name_history,
                    inline=False,
                )
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Can't request info for {subtype}",
                    value=info["error"],
                    inline=False,
                )
                await ctx.send(embed=embed)
        if type == "joke":
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://some-random-api.ml/joke")
                info = await request.json()
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Here is a joke!",
                value=info["joke"],
                inline=False,
            )
            await ctx.send(embed=embed)
        if type == "pokedex" or type == "pd":
            try:
                async with aiohttp.ClientSession() as session:
                    request = await session.get(
                        f"https://some-random-api.ml/pokedex?pokemon={subtype}"
                    )
                    info = await request.json()
                type = str(info["type"])
                type = type.replace("[", "")
                type = type.replace("]", "")
                type = type.replace("'", "")
                species = str(info["species"])
                species = species.replace("[", "")
                species = species.replace("]", "")
                species = species.replace("'", "")
                species = species.replace(",", "")
                abilities = str(info["abilities"])
                abilities = abilities.replace("[", "")
                abilities = abilities.replace("]", "")
                abilities = abilities.replace("'", "")
                gender = str(info["gender"])
                gender = gender.replace("[", "")
                gender = gender.replace("]", "")
                gender = gender.replace("'", "")
                egg_groups = str(info["egg_groups"])
                egg_groups = egg_groups.replace("[", "")
                egg_groups = egg_groups.replace("]", "")
                egg_groups = egg_groups.replace("'", "")
                sprites = info["sprites"]
                stats = info["stats"]
                hp = stats["hp"]
                attack = stats["attack"]
                defense = stats["defense"]
                sp_atk = stats["sp_atk"]
                sp_def = stats["sp_def"]
                speed = stats["speed"]
                total = stats["total"]
                family = info["family"]
                evolutionStage = str(family["evolutionStage"])
                evolutionLine = str(family["evolutionLine"])
                if evolutionLine == "[]":
                    familyText = f"Evolution Stage: {evolutionStage}\nThis Pokémon has no evolution line"
                else:
                    evolutionLine = evolutionLine.replace("[", "")
                    evolutionLine = evolutionLine.replace("]", "")
                    evolutionLine = evolutionLine.replace("'", "")
                    evolutionLine = evolutionLine.replace(",", " ->")
                    familyText = f"Evolution Stage: {evolutionStage}\nEvolution Line: {evolutionLine}"
                embed = discord.Embed(color=0x0DD91A)
                # Possible options: normal or animated
                embed.set_thumbnail(url=sprites["normal"])
                embed.add_field(
                    name=f"Name",
                    value=info["name"].capitalize(),
                    inline=False,
                )
                embed.add_field(
                    name=f"ID",
                    value=info["id"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Type",
                    value=type,
                    inline=False,
                )
                embed.add_field(
                    name=f"Species",
                    value=species,
                    inline=False,
                )
                embed.add_field(
                    name=f"Abilities",
                    value=abilities,
                    inline=False,
                )
                embed.add_field(
                    name=f"Height",
                    value=info["height"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Weight",
                    value=info["weight"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Base Experience",
                    value=info["base_experience"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Gender",
                    value=gender,
                    inline=False,
                )
                embed.add_field(
                    name=f"Egg Groups",
                    value=egg_groups,
                    inline=False,
                )
                embed.add_field(
                    name=f"Stats",
                    value=f"HP: {hp}\nAttack: {attack}\nDefense: {defense}\nSpecial Attack: {sp_atk}\nSpecial Defense: {sp_def}\nSpeed: {speed}\nTotal: {total}",
                    inline=False,
                )
                embed.add_field(
                    name=f"Family",
                    value=familyText,
                    inline=False,
                )
                embed.add_field(
                    name=f"Description",
                    value=info["description"],
                    inline=False,
                )
                embed.add_field(
                    name=f"Generation",
                    value=info["generation"],
                    inline=False,
                )
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0x0DD91A)
                embed.add_field(
                    name=f"Can't request info for the Pokémon {subtype}",
                    value=info["error"],
                    inline=False,
                )
                await ctx.send(embed=embed)
        if type == "meme":
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://some-random-api.ml/meme")
                info = await request.json()
            embed = discord.Embed(color=0x0DD91A, title=info["caption"])
            embed.set_image(url=info["image"])
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"That is not a valid .api comand",
            value=f"The current available commands are:\n> animal\n> minecraft/mc\n> joke\n> pokedex/pd\n> meme",
            inline=False,
        )
        await ctx.send(embed=embed)


@bot.command(name="hypixelparty", aliases=["hypixelp", "hpparty", "hpp"])
async def hypixelrandom(ctx):
    for user in ctx.guild.members:
        if not user.bot:
            if user.status != discord.Status.offline:
                hping = discord.utils.find(
                    lambda r: r.name == "hypixel ping", ctx.guild.roles
                )
                if hping in user.roles:
                    hpon.append(str(user.name) + "#" + str(user.discriminator))
    randomInt = random.randint(0, len(hpon) - 1)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Party leader chosen!",
        value=f"{hpon[randomInt]} will be the party leader!",
        inline=True,
    )
    await ctx.send(embed=embed)
    hpon.clear()


@bot.command(name="shutdown", aliases=["stop"])
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def shutdown(ctx):
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"TIJK Bot was shut down",
        value=f"TIJK Bot was shut down by {ctx.author.name}#{ctx.author.discriminator}",
        inline=True,
    )
    await ctx.send(embed=embed)
    codeman1o1 = bot.get_user(656950082431615057)
    dm = await codeman1o1.create_dm()
    await dm.send(embed=embed)
    print("TIJK Bot was shut down by " + ctx.author.display_name)
    await ctx.bot.close()


@bot.command(name="readtherules", aliases=["rtr"])
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def read_the_rules(ctx, rule_number: int, user: discord.Member):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Please read rule number {rule_number} {user.display_name}",
        value=f"Please don't break the rules",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="mute")
@commands.bot_has_permissions(manage_roles=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def mute(ctx, user: discord.Member):
    muted = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
    owner = discord.utils.find(lambda r: r.name == "Owner", user.guild.roles)
    admin = discord.utils.find(lambda r: r.name == "Admin", user.guild.roles)
    mute_protection = [owner, admin]
    if not muted in user.roles:
        if not any(role in user.roles for role in mute_protection):
            await user.add_roles(muted)
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"User muted!",
                value=f"{user.display_name} is now muted\nType .unmute {user.display_name} to unmute",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Coul not mute {user.display_name}!",
                value=f"You can't mute the owner or an admin!",
                inline=True,
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Could not mute {user.display_name}",
            value=f"{user.display_name} is already muted!",
            inline=True,
        )
        await ctx.send(embed=embed)


@bot.command(name="unmute")
@commands.bot_has_permissions(manage_roles=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def unmute(ctx, user: discord.Member):
    muted = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
    if muted in user.roles:
        await user.remove_roles(muted)
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"User unmuted!",
            value=f"{user.display_name} is now unmuted",
            inline=True,
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Could not unmute {user.display_name}",
            value=f"{user.display_name} is not muted!",
            inline=True,
        )
        await ctx.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx, roundNr: int = 1):
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Pong!",
        value=f"The latency is {round(bot.latency, roundNr)}",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="nick")
@commands.bot_has_permissions(manage_nicknames=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def nick(ctx, user: discord.Member, *, name):
    original_name = user.display_name
    await user.edit(nick=name)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Nickname changed!",
        value=f"{original_name}'s nickname has been changed to {name}",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="assignrole", aliases=["ar", "assignr", "arole"])
@commands.bot_has_permissions(manage_roles=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def assignrole(ctx, role: discord.Role, user: discord.Member):
    if not role in user.roles:
        await user.add_roles(role)
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Role assigned!",
            value=f"Role {role} has been assigned to {user.display_name}",
            inline=True,
        )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Could not assign that role!",
            value=f"{user.display_name} already has the {role} role",
            inline=True,
        )
        await ctx.send(embed=embed)


@bot.command(name="removerole", aliases=["rr", "remover", "rrole"])
@commands.bot_has_permissions(manage_roles=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def removerole(ctx, role: discord.Role, user: discord.Member):
    if role in user.roles:
        await user.remove_roles(role)
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Role removed!",
            value=f"Role {role} has been removed from {user.display_name}",
            inline=True,
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Could not remove role!",
            value=f"{user.display_name} does not have the {role} role!",
            inline=True,
        )
        await ctx.send(embed=embed)


@bot.command(name="restart")
@commands.has_any_role("TIJK-Bot developer")
async def restart(ctx):
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"TIJK Bot is restarting...",
        value=f"TIJK Bot was restarted by {ctx.author.display_name}",
        inline=True,
    )
    await ctx.send(embed=embed)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="Restarting..."
        )
    )
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)
    os.execv(sys.executable, ["python"] + sys.argv)


@bot.command(name="clear")
@commands.bot_has_permissions(manage_messages=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"{amount} messages cleared!",
        value=f"This message wil delete itself after 5 seconds",
        inline=True,
    )
    await ctx.send(embed=embed, delete_after=5)


@bot.command(name="status")
@commands.is_owner()
async def status(ctx, type, *, text: str = "the TIJK Server"):
    if type == "watching":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=text)
        )
    elif type == "playing":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=text)
        )
    elif type == "streaming":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.streaming, name=text)
        )
    elif type == "listening":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=text)
        )
    elif type == "competing":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.competing, name=text)
        )
    elif type == "reset":
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=text)
        )
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Status changed!",
            value=f"Reset the status to **watching the TIJK Server**",
            inline=True,
        )
        await ctx.send(embed=embed)
        return

    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Could not change te status!",
            value=f"{type} is not a valid activity",
            inline=True,
        )
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"Status changed!",
        value=f"Changed the status to **{type} {text}**",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="admin")
@commands.cooldown(1, 30, commands.BucketType.user)
async def admin(ctx, admin: discord.Member, *, message):
    ownerR = discord.utils.find(lambda r: r.name == "Owner", ctx.guild.roles)
    adminR = discord.utils.find(lambda r: r.name == "Admin", ctx.guild.roles)
    roles = [ownerR, adminR]
    if any(roles in admin.roles for roles in roles):
        if admin == ctx.author:
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Bruh",
                value=f"Get some help",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Someone needs your help!",
                value=f"{ctx.author} needs your help with {message}",
                inline=True,
            )
            await admin.send(embed=embed)
            embed = discord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Asked for help!",
                value=f"Asked {admin.display_name} for help with the  message {message}",
                inline=True,
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"That is not an admin!",
            value=f"{admin.display_name} is not an admin!",
            inline=True,
        )
        await ctx.send(embed=embed)


@bot.command(name="kick")
@commands.bot_has_permissions(kick_members=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.kick(reason=reason)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"User kicked!",
        value=f"{user.display_name} has been kicked with the reason {reason}",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="ban")
@commands.bot_has_permissions(ban_members=True)
@commands.has_any_role("Owner", "Admin", "TIJK-Bot developer")
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.ban(reason=reason)
    embed = discord.Embed(color=0x0DD91A)
    embed.add_field(
        name=f"User banned!",
        value=f"{user.display_name} has been banned with the reason {reason}",
        inline=True,
    )
    await ctx.send(embed=embed)


@bot.command(name="help")
async def help(ctx, category=None):
    if category == None:
        embed = discord.Embed(
            title=f"I am TIJK Bot, a custom coded bot for the TIJK Server made by codeman1o1",
            color=0x0DD91A,
        )
        embed.add_field(
            name=f"If you want to see the help command, please send",
            value=f".help general/admin/developer/all",
            inline=False,
        )
        await ctx.send(embed=embed)

    if category.lower() == "general":
        embed = discord.Embed(
            title="I am TIJK Bot, a custom coded bot for the TIJK Server made by codeman1o1",
            color=0x0DD91A,
        )
        embed.add_field(
            name="If you need help with any of our bots please type",
            value="- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- m.help for TIJK "
            "Music (TIJK Bot module)",
            inline=False,
        )
        embed.add_field(name="admin", value=".admin <admin> <message>", inline=True)
        embed.add_field(name="api", value=".api <type> <subtype>", inline=True)
        embed.add_field(name="github", value=".github", inline=True)
        embed.add_field(name="help", value=".help <category>", inline=True)
        embed.add_field(name="hypixelparty", value=".hpp", inline=True)
        embed.add_field(name="ping", value=".ping <roundNr>", inline=True)
        embed.add_field(name="website", value=".website", inline=True)
        await ctx.send(embed=embed)
    if category.lower() == "admin":
        embed = discord.Embed(
            title="I am TIJK Bot, a custom coded bot for the TIJK Server made by codeman1o1",
            color=0x0DD91A,
        )
        embed.add_field(
            name="If you need help with any of our bots please type",
            value="- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- m.help for TIJK "
            "Music (TIJK Bot module)",
            inline=False,
        )
        embed.add_field(name="assignrole", value=".ar <role> <user>", inline=True)
        embed.add_field(name="ban", value=".ban <user> <reason>", inline=True)
        embed.add_field(name="clear", value=".clear <amount>", inline=True)
        embed.add_field(name="github", value=".github", inline=True)
        embed.add_field(name="kick", value=".kick <user> <reason>", inline=True)
        embed.add_field(name="mute", value=".mute <user>", inline=True)
        embed.add_field(name="nick", value=".nick <user> <nickname>", inline=True)
        embed.add_field(name="readtherules", value=".rtr <number> <user>", inline=True)
        embed.add_field(name="removerole", value=".rr <role> <user>", inline=True)
        embed.add_field(name="shutdown", value=".stop", inline=True)
        embed.add_field(name="unmute", value=".unmute <user>", inline=True)
        await ctx.send(embed=embed)
    if category.lower() == "developer":
        embed = discord.Embed(
            title="I am TIJK Bot, a custom coded bot for the TIJK Server made by codeman1o1",
            color=0x0DD91A,
        )
        embed.add_field(
            name="If you need help with any of our bots please type",
            value="- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- m.help for TIJK "
            "Music (TIJK Bot module)",
            inline=False,
        )
        embed.add_field(name="debug", value=".debug <codes>", inline=True)
        embed.add_field(name="github", value=".github", inline=True)
        embed.add_field(name="restart", value=".restart", inline=True)
        embed.add_field(name="shutdown", value=".stop", inline=True)
        embed.add_field(name="status", value=".status <type> <text>", inline=True)
        await ctx.send(embed=embed)
    if category.lower() == "all":
        embed = discord.Embed(
            title="I am TIJK Bot, a custom coded bot for the TIJK Server made by codeman1o1",
            color=0x0DD91A,
        )
        embed.add_field(
            name="If you need help with any of our bots please type",
            value="- !help for MEE6\n- pls help for Dank Memer\n- s!help for Statisfy\n- m.help for TIJK "
            "Music (TIJK Bot module)",
            inline=False,
        )
        embed.add_field(name="admin", value=".admin <admin> <message>", inline=True)
        embed.add_field(name="api", value=".api <type> <subtype>", inline=True)
        embed.add_field(name="assignrole", value=".ar <role> <user>", inline=True)
        embed.add_field(name="ban", value=".ban <user> <reason>", inline=True)
        embed.add_field(name="clear", value=".clear <amount>", inline=True)
        embed.add_field(name="debug", value=".debug <codes>", inline=True)
        embed.add_field(name="github", value=".github", inline=True)
        embed.add_field(name="help", value=".help <category>", inline=True)
        embed.add_field(name="hypixelparty", value=".hpp", inline=True)
        embed.add_field(name="kick", value=".kick <user> <reason>", inline=True)
        embed.add_field(name="mute", value=".mute <user>", inline=True)
        embed.add_field(name="nick", value=".nick <user> <nickname>", inline=True)
        embed.add_field(name="ping", value=".ping <roundNr>", inline=True)
        embed.add_field(name="readtherules", value=".rtr <number> <user>", inline=True)
        embed.add_field(name="removerole", value=".rr <role> <user>", inline=True)
        embed.add_field(name="restart", value=".restart", inline=True)
        embed.add_field(name="shutdown", value=".stop", inline=True)
        embed.add_field(name="status", value=".status <type> <text>", inline=True)
        embed.add_field(name="unmute", value=".unmute <user>", inline=True)
        embed.add_field(name="website", value=".website", inline=True)
        await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"That is not a command!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"You forgot an argument!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Please enter the argument correctly!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingAnyRole):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"You do not have the required role!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"I do not have the required permissions!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"This command is on cooldown!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)

    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"You can't do that!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)


keep_alive.keep_alive()
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))
BotToken = os.environ["BotToken"]
bot.run(BotToken)

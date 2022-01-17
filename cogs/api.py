import os

import aiohttp
import nextcord
import requests
from nextcord.ext import commands
from datetime import datetime
from mojang import MojangAPI
import math

from main import HYPIXEL_API_KEY


class api(commands.Cog, name="API", description="A seperate cog for the API command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(
        name="api",
        description="Uses API's to get information",
        brief="Uses API's to get information",
        invoke_without_command=True,
    )
    async def api(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Help with the .api command",
            value="The .api command gets information from API's.\n**I do not own any of the API's, so if there occurs an issue, I can most likely not help you with it.**\nType `.help api` for all available subcommands",
            inline=False,
        )

        await ctx.send(embed=embed)

    @api.command(
        name="animal",
        description="Uses an animal API to get information",
        brief="Uses an animal API to get information",
    )
    async def animal_api(self, ctx, *, animal):
        animals = ("dog", "cat", "panda", "red_panda", "bird", "fox", "koala")
        animal = animal.replace(" ", "_")
        if animal.lower() in animals:
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://some-random-api.ml/img/{animal}")
                info = await request.json()
            await ctx.send(info["link"])
        elif animal.lower() not in animals:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Can't request image!",
                value=f"{animal} is not a valid animal type __for the API__\nValid animal types are:\n> Dog\n> Cat\n> Panda\n> Red Panda\n> Bird\n> Fox\n> Koala",
                inline=False,
            )

            await ctx.send(embed=embed)

    @api.command(
        name="minecraft",
        description="Uses a Minecraft API to get information",
        brief="Uses an Minecraft API to get information",
        aliases=["mc"],
    )
    async def mc_api(self, ctx, *, username):
        embed = nextcord.Embed(color=0x0DD91A)
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f"https://some-random-api.ml/mc?username={username}"
                )
                info = await request.json()
            name_history2 = ""
            for k in info["name_history"]:
                name_history2 = (
                    name_history2
                    + "\nName: "
                    + k["name"]
                    + "\nChanged at: "
                    + k["changedToAt"]
                    + "\n"
                )
            embed.add_field(name="Username", value=info["username"], inline=False)
            embed.add_field(name="UUID", value=info["uuid"], inline=False)
            embed.add_field(name="Name History", value=name_history2, inline=False)
        except KeyError:
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name=f"Can't request info for {username}",
                value="Error provided by the API:\n" + info["error"],
                inline=False,
            )
        await ctx.send(embed=embed)

    @api.command(
        name="joke",
        description="Uses a joke API to get information",
        brief="Uses an joke API to get information",
    )
    async def joke_api(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/joke")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(name="Here is a joke!", value=info["joke"], inline=False)
        await ctx.send(embed=embed)

    @api.command(
        name="meme",
        description="Uses an meme API to get information",
        brief="Uses an meme API to get information",
    )
    async def meme_api(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/meme")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A, title=info["caption"])
        embed.set_image(url=info["image"])
        await ctx.send(embed=embed)

    @api.command(
        name="pokedex",
        description="Uses a Pokémon API to get information",
        brief="Uses a Pokémon API to get information",
        aliases=["pd", "pokemon", "pm"],
    )
    async def pokedex_api(self, ctx, *, name):
        embed = nextcord.Embed(color=0x0DD91A)
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f"https://some-random-api.ml/pokedex?pokemon={name}"
                )
                info = await request.json()
            type = ""
            for k in info["type"]:
                type = type + k + ", "
            type = type[:-2]
            species = ""
            for k in info["species"]:
                species = species + k + " "
            abilities = ""
            for k in info["abilities"]:
                abilities = abilities + k + ", "
            abilities = abilities[:-2]
            gender = ""
            for k in info["gender"]:
                gender = gender + k + ", "
            gender = gender[:-2]
            egg_groups = ""
            for k in info["egg_groups"]:
                egg_groups = egg_groups + k + ", "
            egg_groups = egg_groups[:-2]
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
            evolutionStage = family["evolutionStage"]
            evolutionLine = family["evolutionLine"]
            if not evolutionLine:
                familyText = f"This Pokémon has no evolution line"
            else:
                evolutionLine2 = ""
                for k in evolutionLine:
                    evolutionLine2 = evolutionLine2 + k + " -> "
                evolutionLine2 = evolutionLine2[:-4]
                familyText = f"Evolution Stage: {evolutionStage}\nEvolution Line: {evolutionLine2}"
            # Possible options: "normal" or "animated"
            embed.set_thumbnail(url=sprites["normal"])
            embed.add_field(name="Name", value=info["name"].capitalize(), inline=True)
            embed.add_field(name="ID", value=info["id"], inline=True)
            embed.add_field(name="Type", value=type, inline=True)
            embed.add_field(name="Species", value=species, inline=True)
            embed.add_field(name="Abilities", value=abilities, inline=True)
            embed.add_field(name="Height", value=info["height"], inline=True)
            embed.add_field(name="Weight", value=info["weight"], inline=True)
            embed.add_field(
                name="Base Experience", value=info["base_experience"], inline=True
            )

            embed.add_field(name="Gender", value=gender, inline=True)
            embed.add_field(name="Egg Groups", value=egg_groups, inline=True)
            embed.add_field(
                name="Stats",
                value=f"HP: {hp}\nAttack: {attack}\nDefense: {defense}\nSpecial Attack: {sp_atk}\nSpecial Defense: {sp_def}\nSpeed: {speed}\nTotal: {total}",
                inline=True,
            )

            embed.add_field(name="Family", value=familyText, inline=True)
            embed.add_field(
                name="Description",
                value=info["description"].replace(". ", ".\n"),
                inline=True,
            )

            embed.add_field(name="Generation", value=info["generation"], inline=True)
        except KeyError:
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name=f"Can't request info for the Pokémon {name}",
                value="Error provided by the API:\n" + info["error"],
                inline=True,
            )
        await ctx.send(embed=embed)

    @api.command(
        name="hypixel",
        description="Gets information from the official Hypixel API",
        brief="Get information from the official Hypixel API",
        aliases=["hp"],
    )
    async def hypixel(self, ctx, username: str):
        uuid = MojangAPI.get_uuid(username)
        data = requests.get(
            f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
        ).json()
        data_friends = requests.get(
            f"https://api.hypixel.net/friends?key={HYPIXEL_API_KEY}&uuid={uuid}"
        ).json()
        data_guild = requests.get(
            f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&player={uuid}"
        ).json()
        if data["success"] == True:
            player_data = data["player"]
            if "rank" in player_data:
                rank = player_data["rank"]
            elif "monthlyPackageRank" in player_data:
                rank = player_data["monthlyPackageRank"].replace("_PLUS", "+")
            elif "newPackageRank" in player_data:
                rank = player_data["newPackageRank"].replace("_PLUS", "+")
            else:
                rank = ""
            display_name = data["player"]["displayname"]
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Here is information for **{rank} {display_name}**:",
            )
            if "lastLogout" in player_data:
                logouttime = player_data["lastLogout"]
                logintime = player_data["lastLogin"]
                if logouttime < logintime:
                    embed.add_field(
                        name="Last online:",
                        value=f"{display_name} is currently online",
                        inline=False,
                    )
                else:
                    offline_for = datetime.fromtimestamp(
                        datetime.now().timestamp() - (logouttime / 1000)
                    ).strftime("%d days and %H hours")
                    embed.add_field(
                        name="Last online:",
                        value=datetime.fromtimestamp(logouttime / 1000).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        + "\nOffline for: "
                        + offline_for,
                        inline=False,
                    )
            else:
                embed.add_field(
                    name="Last online:",
                    value="This is not enabled for this player",
                    inline=False,
                )
            embed.add_field(
                name="Friends:", value=len(data_friends["records"]), inline=False
            )
            if data_guild["success"] == True and data_guild["guild"] is not None:
                name = data_guild["guild"]["name"]
                members = str(len(data_guild["guild"]["members"]))
                embed.add_field(
                    name="Guild:",
                    value=f"{name} ({members} members)",
                    inline=False,
                )
            else:
                embed.add_field(
                    name="Guild:",
                    value=f"{display_name} is not in a guild",
                    inline=False,
                )
            if "socialMedia" in player_data and "links" in player_data["socialMedia"]:
                social_media = "".join(
                    f"{k.capitalize()}: {i}\n"
                    for k, i in player_data["socialMedia"]["links"].items()
                )
                if social_media == "":
                    social_media = "This player has no Social Media linked"
                embed.add_field(name="Social Media", value=social_media, inline=False)
            else:
                embed.add_field(
                    name="Social Media",
                    value="This player has no Social Media linked",
                    inline=False,
                )
            network_experience = player_data["networkExp"]
            network_level = (math.sqrt((2 * network_experience) + 30625) / 50) - 2.5
            network_level = round(network_level, 2)
            embed.add_field(name="Network Level", value=network_level, inline=False)
            karma = player_data["karma"]
            embed.add_field(name="Karma", value=f"{karma:,}", inline=False)
        else:
            error = data["cause"]
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name="An error occured!", value=f"Error provided by the API:\n{error}"
            )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(api(bot))

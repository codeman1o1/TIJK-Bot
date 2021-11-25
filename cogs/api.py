import nextcord
from nextcord.ext import commands
import aiohttp
import requests
import urllib.request
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(os.path.join(os.getcwd() + "\.env"))


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
            name=f"Help with the .api command",
            value=f"The .api command gets information from API's.\nI do not own any of the API's, so if there occurs an issue, I cannot help you with it.\nType .help api for all available subcommands",
            inline=False,
        )
        await ctx.send(embed=embed)

    @api.command(
        name="help", description="Help command for .api", brief="Help command for .api"
    )
    async def help_api(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Help with the .api command",
            value=f"The .api command gets information from API's.\n**I do not own any of the API's, so if there occurs an issue, I cannot help you with it.**\nType .help api for all available subcommands",
            inline=False,
        )
        await ctx.send(embed=embed)

    @api.command(
        name="animal",
        description="Uses an animal API to get information",
        brief="Uses an animal API to get information",
    )
    async def animal_api(self, ctx, *, animal):
        animals = ["dog", "cat", "panda", "red_panda", "bird", "fox", "koala"]
        animal = animal.replace(" ", "_")
        if animal.lower() in animals:
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://some-random-api.ml/img/{animal}")
                info = await request.json()
            await ctx.send(info["link"])
        else:
            if animal == "":
                subtype = "That"
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Can't request image!",
                value=f"{subtype} is not a valid animal type **for the API**\nValid animal types are:\n> Dog\n> Cat\n> Panda\n> Red Panda\n> Bird\n> Fox\n> Koala",
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
        except KeyError:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"Can't request info for {username}",
                value=info["error"],
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
            request = await session.get(f"https://some-random-api.ml/joke")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name=f"Here is a joke!",
            value=info["joke"],
            inline=False,
        )
        await ctx.send(embed=embed)

    @api.command(
        name="meme",
        description="Uses an meme API to get information",
        brief="Uses an meme API to get information",
    )
    async def meme_api(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f"https://some-random-api.ml/meme")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A, title=info["caption"])
        embed.set_image(url=info["image"])
        await ctx.send(embed=embed)

    @api.command(
        name="pokedex",
        description="Uses a Pokémon API to get information",
        brief="Uses a Pokémon API to get information",
        aliases=["pd"],
    )
    async def pokedex_api(self, ctx, *, name):
        embed = nextcord.Embed(color=0x0DD91A)
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f"https://some-random-api.ml/pokedex?pokemon={name}"
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
            # Possible options: normal or animated
            embed.set_thumbnail(url=sprites["normal"])
            embed.add_field(
                name=f"Name",
                value=info["name"].capitalize(),
                inline=True,
            )
            embed.add_field(
                name=f"ID",
                value=info["id"],
                inline=True,
            )
            embed.add_field(
                name=f"Type",
                value=type,
                inline=True,
            )
            embed.add_field(
                name=f"Species",
                value=species,
                inline=True,
            )
            embed.add_field(
                name=f"Abilities",
                value=abilities,
                inline=True,
            )
            embed.add_field(
                name=f"Height",
                value=info["height"],
                inline=True,
            )
            embed.add_field(
                name=f"Weight",
                value=info["weight"],
                inline=True,
            )
            embed.add_field(
                name=f"Base Experience",
                value=info["base_experience"],
                inline=True,
            )
            embed.add_field(
                name=f"Gender",
                value=gender,
                inline=True,
            )
            embed.add_field(
                name=f"Egg Groups",
                value=egg_groups,
                inline=True,
            )
            embed.add_field(
                name=f"Stats",
                value=f"HP: {hp}\nAttack: {attack}\nDefense: {defense}\nSpecial Attack: {sp_atk}\nSpecial Defense: {sp_def}\nSpeed: {speed}\nTotal: {total}",
                inline=True,
            )
            embed.add_field(
                name=f"Family",
                value=familyText,
                inline=True,
            )
            embed.add_field(
                name=f"Description",
                value=info["description"].replace(". ", ".\n"),
                inline=True,
            )
            embed.add_field(
                name=f"Generation",
                value=info["generation"],
                inline=True,
            )
        except KeyError:
            embed.add_field(
                name=f"Can't request info for the Pokémon {name}",
                value=info["error"],
                inline=True,
            )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(api(bot))

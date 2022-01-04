import os

import aiohttp
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

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


def setup(bot: commands.Bot):
    bot.add_cog(api(bot))

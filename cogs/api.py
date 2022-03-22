import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from datetime import datetime
from mojang import MojangAPI
import math

from main import HYPIXEL_API_KEY


class api(commands.Cog, name="API"):
    """A separate cog for the API command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="api", invoke_without_command=True)
    async def api(self, ctx: Context):
        """Uses API's to get information"""
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Help with the .api command",
            value="The .api command gets information from API's.\n**I do not own any of the API's, so if there occurs an issue, I can most likely not help you with it.**\nType `.help api` for all available subcommands",
            inline=False,
        )
        embed.add_field(
            name="Credits:",
            value="`.api activity`: https://www.boredapi.com\n`.api animal`: https://some-random-api.ml\n`.api hypixel`: https://api.hypixel.net\n`.api joke`: https://some-random-api.ml\n`.api meme`: https://some-random-api.ml\n`.api minecraft`: https://some-random-api.ml\n`.api pokedex`: https://some-random-api.ml",
            inline=True,
        )
        await ctx.send(embed=embed)

    @api.command(name="animal")
    async def animal_api(self, ctx: Context, *, animal: str):
        """Uses an animal API to get information"""
        animals = ("dog", "cat", "panda", "red_panda", "bird", "fox", "koala")
        animal = animal.replace(" ", "_")
        if animal.lower() in animals:
            async with aiohttp.ClientSession() as session:
                request = await session.get(f"https://some-random-api.ml/img/{animal}")
                info = await request.json()
            await ctx.send(info["link"])
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name="Can't request image!",
                value=f"{animal} is not a valid animal type __for the API__\nValid animal types are:\n> Dog\n> Cat\n> Panda\n> Red Panda\n> Bird\n> Fox\n> Koala",
                inline=False,
            )

            await ctx.send(embed=embed)

    @api.command(name="minecraft", aliases=["mc"])
    async def mc_api(self, ctx: Context, *, username: str):
        """Uses a Minecraft API to get information"""
        embed = nextcord.Embed(color=0x0DD91A)
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f"https://some-random-api.ml/mc?username={username}"
                )
                info = await request.json()
            name_history2 = ""
            for item in info["name_history"]:
                name_history2 = (
                    name_history2
                    + "\nName: "
                    + item["name"]
                    + "\nChanged at: "
                    + item["changedToAt"]
                    + "\n"
                )
            embed.add_field(name="Username", value=info["username"], inline=False)
            embed.add_field(name="UUID", value=info["uuid"], inline=False)
            embed.add_field(name="Name History", value=name_history2, inline=False)
        except:
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name=f"Can't request info for {username}",
                value="Error provided by the API:\n" + info["error"],
                inline=False,
            )
        await ctx.send(embed=embed)

    @api.command(name="joke")
    async def joke_api(self, ctx: Context):
        """Uses a joke API to get information"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/joke")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(name="Here is a joke!", value=info["joke"], inline=False)
        await ctx.send(embed=embed)

    @api.command(name="meme")
    async def meme_api(self, ctx: Context):
        """Uses a meme API to get information"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/meme")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A, title=info["caption"])
        embed.set_image(url=info["image"])
        await ctx.send(embed=embed)

    @api.command(name="pokedex", aliases=["pd", "pokemon", "pm"])
    async def pokedex_api(self, ctx: Context, *, name: str):
        """Uses a Pokémon API to get information"""
        embed = nextcord.Embed(color=0x0DD91A)
        try:
            async with aiohttp.ClientSession() as session:
                request = await session.get(
                    f"https://some-random-api.ml/pokedex?pokemon={name}"
                )
                info = await request.json()
            type = ", ".join(info["type"])
            species = " ".join(info["species"])
            abilities = ", ".join(info["abilities"])
            gender = ", ".join(info["gender"])
            egg_groups = ", ".join(info["egg_groups"])
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
            evolution_stage = family["evolutionStage"]
            if evolution_line := family["evolutionLine"]:
                evolution_line2 = ""
                for data in evolution_line:
                    evolution_line2 = evolution_line2 + data + " -> "
                evolution_line2 = evolution_line2[:-4]
                family_text = f"Evolution Stage: {evolution_stage}\nEvolution Line: {evolution_line2}"
            else:
                family_text = "This Pokémon has no evolution line"
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

            embed.add_field(name="Family", value=family_text, inline=True)
            embed.add_field(
                name="Description",
                value=info["description"].replace(". ", ".\n"),
                inline=True,
            )

            embed.add_field(name="Generation", value=info["generation"], inline=True)
        except:
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name=f"Can't request info for the Pokémon {name}",
                value="Error provided by the API:\n" + info["error"],
                inline=True,
            )
        await ctx.send(embed=embed)

    @api.command(name="hypixel", aliases=["hp"])
    async def hypixel(self, ctx: Context, username: str):
        """Gets information from the official Hypixel API"""
        uuid = MojangAPI.get_uuid(username)
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
            )
            data = await request.json()

        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f"https://api.hypixel.net/friends?key={HYPIXEL_API_KEY}&uuid={uuid}"
            )
            data_friends = await request.json()

        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&player={uuid}"
            )
            data_guild = await request.json()

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
                if not social_media:
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
                name="An error occurred!", value=f"Error provided by the API:\n{error}"
            )
        await ctx.send(embed=embed)

    @api.group(name="activity", invoke_without_command=True)
    async def activity_api(self, ctx: Context):
        """Sends a random activity you can do"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://www.boredapi.com/api/activity")
            data = await request.json()

        embed = nextcord.Embed(color=0x0DD91A)
        activity = data["activity"]
        if data["link"] != "":
            activity = activity + "\nLink: " + data["link"]
        embed.add_field(name="Here is a random activity", value=activity, inline=True)
        await ctx.send(embed=embed)

    @activity_api.command(name="alone")
    async def alone_activity_api(self, ctx: Context):
        """Sends a random activity you can do alone"""
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                "https://www.boredapi.com/api/activity?participants=1"
            )
            data = await request.json()

        embed = nextcord.Embed(color=0x0DD91A)
        activity = data["activity"]
        if data["link"] != "":
            activity = activity + "\nLink: " + data["link"]
        embed.add_field(
            name="Here is a random activity that you can do alone",
            value=activity,
            inline=True,
        )
        await ctx.send(embed=embed)

    @activity_api.command(name="free")
    async def free_activity_api(self, ctx: Context):
        """Sends a random activity you can do for free"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://www.boredapi.com/api/activity?price=0")
            data = await request.json()

        embed = nextcord.Embed(color=0x0DD91A)
        activity = data["activity"]
        if data["link"] != "":
            activity = activity + "\nLink: " + data["link"]
        embed.add_field(
            name="Here is a random activity that is free", value=activity, inline=True
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(api(bot))

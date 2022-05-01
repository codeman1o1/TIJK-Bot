from datetime import datetime
import math
import os
from PIL import Image
import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
from mojang import MojangAPI
import requests

from main import SLASH_GUILDS, HYPIXEL_API_KEY


class Api(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def embed_with_mc_head(
        self, interaction: Interaction, embed: nextcord.Embed, username: str
    ):
        uuid = MojangAPI.get_uuid(username)
        if not uuid:
            embed = nextcord.Embed(color=0xFFC800, title="That is not a user!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        profile = MojangAPI.get_profile(uuid)
        skin_url = profile.skin_url
        skin = Image.open(requests.get(skin_url, stream=True).raw)
        head_img = skin.crop((8, 8, 16, 16))
        head_img = head_img.resize((128, 128), Image.NEAREST)
        head_img.save("head_img.png")
        head_img.close()
        file = nextcord.File("head_img.png")
        embed.set_thumbnail(url="attachment://head_img.png")
        await interaction.response.send_message(embed=embed, file=file)
        os.remove("head_img.png")

    @slash(guild_ids=SLASH_GUILDS)
    async def api(self, interaction: Interaction):
        """This will never get called since it has slash commands"""
        pass

    @api.subcommand(name="animal", inherit_hooks=True)
    async def animal_api(
        self,
        interaction: Interaction,
        animal=SlashOption(
            choices={
                "dog": "dog",
                "cat": "cat",
                "panda": "panda",
                "red panda": "red_panda",
                "bird": "bird",
                "fox": "fox",
                "koala": "koala",
            },
            description="The animal",
            required=True,
        ),
    ):
        """Uses an API to get information about an animal"""
        async with aiohttp.ClientSession() as session:
            request = await session.get(f"https://some-random-api.ml/img/{animal}")
            info = await request.json()
        await interaction.response.send_message(info["link"])

    @api.subcommand(name="hypixel", inherit_hooks=True)
    async def hypixel_api(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description="The username of the user", required=True
        ),
    ):
        """Gets information from the official Hypixel API"""
        uuid = MojangAPI.get_uuid(username)
        if not uuid:
            embed = nextcord.Embed(color=0xFFC800, title="That is not a user!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
            )
            friends_request = await session.get(
                f"https://api.hypixel.net/friends?key={HYPIXEL_API_KEY}&uuid={uuid}"
            )
            guild_request = await session.get(
                f"https://api.hypixel.net/guild?key={HYPIXEL_API_KEY}&player={uuid}"
            )
            data = await request.json()
            data_friends = await friends_request.json()
            data_guild = await guild_request.json()

        if data["success"]:
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
            if data_guild["success"] and data_guild["guild"] is not None:
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
            await self.embed_with_mc_head(interaction, embed, username)
        else:
            error = data["cause"]
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name="An error occurred!", value=f"Error provided by the API:\n{error}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @api.subcommand(name="minecraft", inherit_hooks=True)
    async def minecraft_api(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description="The username of the user", required=True
        ),
    ):
        """Gets information from the Mojang API"""
        uuid = MojangAPI.get_uuid(username)
        if not uuid:
            embed = nextcord.Embed(color=0xFFC800, title="That is not a user!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = nextcord.Embed(color=0x0DD91A)
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
        await self.embed_with_mc_head(interaction, embed, username)

    @api.subcommand(name="joke", inherit_hooks=True)
    async def joke_api(self, interaction: Interaction):
        """Gets a random joke from an API"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/joke")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(name="Here is a joke!", value=info["joke"], inline=False)
        await interaction.response.send_message(embed=embed)

    @api.subcommand(name="meme", inherit_hooks=True)
    async def meme_api(self, interaction: Interaction):
        """Gets a random meme from an API"""
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/meme")
            info = await request.json()
        embed = nextcord.Embed(color=0x0DD91A, title=info["caption"])
        embed.set_image(url=info["image"])
        await interaction.response.send_message(embed=embed)

    @api.subcommand(name="pokedex", inherit_hooks=True)
    async def pokedex_api(
        self,
        interaction: Interaction,
        name: str = SlashOption(description="The name of the Pokémon", required=True),
    ):
        """Uses an API to get information about a Pokémon"""
        embed = nextcord.Embed(color=0x0DD91A)
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                f"https://some-random-api.ml/pokedex?pokemon={name}"
            )
            info: dict = await request.json()

        if "error" in info:
            embed = nextcord.Embed(color=0xFFC800, title=info["error"])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        pokemon_type = ", ".join(info["type"])
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
            family_text = (
                f"Evolution Stage: {evolution_stage}\nEvolution Line: {evolution_line2}"
            )
        else:
            family_text = "This Pokémon has no evolution line"
        # Possible options: "normal" or "animated"
        embed.set_thumbnail(url=sprites["normal"])
        embed.add_field(name="Name", value=info["name"].capitalize(), inline=True)
        embed.add_field(name="ID", value=info["id"], inline=True)
        embed.add_field(name="Type", value=pokemon_type, inline=True)
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

        await interaction.response.send_message(embed=embed)

    @api.subcommand(name="activity", inherit_hooks=True)
    async def activity_api(
        self,
        interaction: Interaction,
        extra_option=SlashOption(
            description="Extra configurable options",
            choices=["alone", "free"],
            required=False,
        ),
    ):
        """Gets a random activity from an API"""
        url = "https://www.boredapi.com/api/activity"
        extra_text = ""
        if extra_option == "alone":
            url = "https://www.boredapi.com/api/activity?participants=1"
            extra_text = " that you can do alone"
        elif extra_option == "free":
            url = "https://www.boredapi.com/api/activity?price=0"
            extra_text = " that you can do for free"
        async with aiohttp.ClientSession() as session:
            request = await session.get(url)
            data = await request.json()

        embed = nextcord.Embed(color=0x0DD91A)
        activity = data["activity"]
        if data["link"] != "":
            activity = activity + "\nLink: " + data["link"]
        embed.add_field(
            name=f"Here is a random activity{extra_text}", value=activity, inline=True
        )
        await interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Api(bot))

import os
import uuid
from typing import Literal

import aiohttp
import nextcord
import requests
from mojang import MojangAPI
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands
from PIL import Image


async def embed_with_mc_head(
    interaction: Interaction, embed: nextcord.Embed, username: str
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


class Api(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash()
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

    @api.subcommand(name="minecraft", inherit_hooks=True)
    async def minecraft_api(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description="The username of the user", required=True
        ),
    ):
        """Gets information from the Mojang API"""
        mc_uuid = MojangAPI.get_uuid(username)
        user = MojangAPI.get_profile(mc_uuid)
        if not mc_uuid or not user:
            embed = nextcord.Embed(color=0xFFC800, title="That is not a user!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(
            name="UUID", value=user.id + "\n" + str(uuid.UUID(user.id)), inline=False
        )
        await embed_with_mc_head(interaction, embed, username)

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
        hp = stats["hp"]  # pylint: disable=invalid-name
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
        extra_option: Literal["alone", "free"] = SlashOption(
            description="Extra configurable options",
            required=False,
        ),
    ):
        """Gets a random activity from an API"""
        url = "http://www.boredapi.com/api/activity"
        extra_text = ""
        if extra_option == "alone":
            url += "?participants=1"
            extra_text = " that you can do alone"
        elif extra_option == "free":
            url += "?price=0"
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

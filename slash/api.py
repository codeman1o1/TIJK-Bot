from datetime import datetime
from PIL import Image
import math
import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, slash_command as slash
from nextcord.application_command import SlashOption
from mojang import MojangAPI
import requests
import os

from main import SLASH_GUILDS, HYPIXEL_API_KEY


class api_slash(
    commands.Cog, name="API Slash commands", description="API slash commands"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    async def api(self, interaction: Interaction):
        """This will never get called since it has slash commands"""
        pass

    @api.subcommand(
        name="animal",
        description="Uses an animal API to get information",
        inherit_hooks=True,
    )
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
        async with aiohttp.ClientSession() as session:
            request = await session.get(f"https://some-random-api.ml/img/{animal}")
            info = await request.json()
        await interaction.response.send_message(info["link"])

    @api.subcommand(
        name="hypixel",
        description="Gets information from the official Hypixel API",
        inherit_hooks=True,
    )
    async def hypixel_api(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description="The username of the user", required=True
        ),
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
            embed.set_thumbnail(url="attachment://head_img.png")
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
        else:
            error = data["cause"]
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name="An error occurred!", value=f"Error provided by the API:\n{error}"
            )
        await interaction.response.send_message(embed=embed, file=file)
        os.remove("head_img.png")

    @api.subcommand(
        name="minecraft",
        description="Gets information from the Mojang API",
        inherit_hooks=True,
    )
    async def minecraft_api(
        self,
        interaction: Interaction,
        username: str = SlashOption(
            description="The username of the user", required=True
        ),
    ):
        uuid = MojangAPI.get_uuid(username)
        if not uuid:
            embed = nextcord.Embed(color=0xFFC800, title="That is not a user!")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        try:
            profile = MojangAPI.get_profile(uuid)
            skin_url = profile.skin_url
            skin = Image.open(requests.get(skin_url, stream=True).raw)
            head_img = skin.crop((8, 8, 16, 16))
            head_img = head_img.resize((128, 128), Image.NEAREST)
            head_img.save("head_img.png")
            head_img.close()
            file = nextcord.File("head_img.png")
            embed = nextcord.Embed(color=0x0DD91A)
            embed.set_thumbnail(url="attachment://head_img.png")
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
            await interaction.response.send_message(file=file, embed=embed)
            os.remove("head_img.png")
        except Exception:
            embed = nextcord.Embed(color=0xFF0000)
            embed.add_field(
                name=f"Can't request info for {username}",
                value="Error provided by the API:\n" + info["error"],
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(api_slash(bot))

import json
import os
import random
from typing import List, Literal

import asyncio
import docker
import nextcord
import pymongo
from docker.errors import DockerException
from docker.models.containers import Container
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands
import youtube_dl

from main import USER_DATA, logger

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

HAMSTEREN_URL = "https://www.youtube.com/watch?v=0fn4X2TLxNc"

try:
    DOCKER_CLIENT = docker.from_env()
except DockerException:
    # Docker is most likely not installed
    DOCKER_CLIENT = None


def get_8ball_responses():
    root = os.path.abspath(os.getcwd())
    with open(
        os.path.join(root, "8ball_responses.json"), "r", encoding="utf-8"
    ) as file:
        eight_ball_responses = file.read()
    return tuple(json.loads(eight_ball_responses)["responses"])  # type: ignore[arg-type]


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash()
    async def headsortails(self, interaction: Interaction):
        """Flip a coin"""
        hot = random.choice(("heads", "tails"))
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await interaction.response.send_message(embed=embed)

    @slash()
    async def respect(
        self,
        interaction: Interaction,
        text: str = SlashOption(description="What you respect", required=False),
    ):
        """Press F to pay respect"""
        hearts = ("❤️", "🧡", "💛", "💚", "💙", "💜", "🤎")
        reason = f"for **{text}** " if text else ""
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"**{interaction.user.name}** has paid their respect {reason}{random.choice(hearts)}",
        )
        await interaction.response.send_message(embed=embed)

    @slash()
    async def rockpaperscissors(
        self,
        interaction: Interaction,
        choice: Literal["rock", "paper", "scissors"] = SlashOption(
            description="Your choice",
            required=True,
        ),
    ):
        """Play rock paper scissors"""
        embed = nextcord.Embed(color=0x0DD91A)
        random_choice = random.choice(("rock", "paper", "scissors"))
        if choice == random_choice:
            wlt = "it is a tie"
        elif choice == "paper":
            if random_choice == "rock":
                wlt = "you win"
            elif random_choice == "scissors":
                wlt = "I win"
        elif choice == "rock":
            if random_choice == "paper":
                wlt = "I win"
            elif random_choice == "scissors":
                wlt = "you win"
        elif choice == "scissors":
            if random_choice == "paper":
                wlt = "you win"
            elif random_choice == "rock":
                wlt = "I win"
        embed.add_field(
            name=f"You had {choice} and I had {random_choice}",
            value=f"That means that {wlt}!",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @slash()
    async def messages(self, interaction: Interaction):
        """Show the amount of messages each user has sent"""
        embed = nextcord.Embed(color=0x0DD91A)
        for user in USER_DATA.find().sort("messages", pymongo.DESCENDING):
            if "messages" in user:
                messages = user["messages"]
                user = self.bot.get_user(int(user["_id"]))
                embed.add_field(
                    name=f"{user} has sent",
                    value=f"{messages} messages",
                    inline=False,
                )
        if len(embed.fields) == 0:
            embed = nextcord.Embed(
                color=0x0DD91A, title="Nobody has sent any messages!"
            )
        await interaction.response.send_message(embed=embed)

    @slash()
    async def eightball(
        self,
        interaction: Interaction,
        question=SlashOption(description="Question", required=True),
    ):
        """Ask 8ball a question"""
        embed = nextcord.Embed(color=0x0DD91A, title=question)
        embed.description = random.choice(get_8ball_responses())
        await interaction.response.send_message(embed=embed)

    if DOCKER_CLIENT is not None:

        @slash(name="start-server", guild_ids=(870973430114181141, 1022468050164924497))
        async def start_server(
            self,
            interaction: Interaction,
            server: str = SlashOption(description="The server to start", required=True),
        ):
            """Start a Minecraft server"""
            minecraft_server: Container = DOCKER_CLIENT.containers.get(server)
            if minecraft_server.status != "exited":
                await interaction.response.send_message(
                    "Server is already running!", ephemeral=True
                )
                return

            minecraft_server.start()
            embed = nextcord.Embed(color=0x0DD91A, title="Server starting!")
            await interaction.response.send_message(embed=embed)

        @start_server.on_autocomplete("server")
        async def server_autocomplete(self, interaction: Interaction, server: str):
            mc_containers: List[Container] = DOCKER_CLIENT.containers.list(
                all=True,
                filters={
                    "ancestor": "itzg/minecraft-server",
                    "label": "allow_remote_start=true",
                },
            )
            await interaction.response.send_autocomplete(
                [container.name for container in mc_containers]
            )

    @slash()
    async def hamsteren(self, interaction: Interaction):
        """Hamsteren"""
        if not isinstance(interaction.channel, nextcord.VoiceChannel):
            await interaction.response.send_message(
                "You must be in a voice channel to use this command!", ephemeral=True
            )
            return

        if (
            interaction.user.voice is None
            or interaction.user.voice.channel is None
            or interaction.user.voice.channel != interaction.channel
        ):
            await interaction.response.send_message(
                "You must be in this voice channel to use this command!", ephemeral=True
            )
            return

        if interaction.guild.voice_client is None:
            voice_client = await interaction.channel.connect()
        else:
            voice_client = interaction.guild.voice_client
            if voice_client.channel != interaction.channel:
                await voice_client.move_to(interaction.channel)

        player = await YTDLSource.from_url(
            HAMSTEREN_URL, loop=self.bot.loop, stream=True
        )
        try:
            voice_client.play(
                player,
                after=lambda e: logger.error(f"Player error: {e}")
                if e is not None
                else voice_client.disconnect(),
            )
        except nextcord.ClientException:
            await interaction.response.send_message(
                "We zijn al aan het hamsteren!", ephemeral=True
            )
            return
        await interaction.response.send_message("We gaan hamsteren!")


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))

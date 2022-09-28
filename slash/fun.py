import json
import os
import random
from typing import List, Literal

import docker
import nextcord
import pymongo
from docker.models.containers import Container
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands

from main import USER_DATA

DOCKER_CLIENT = docker.from_env()


def get_8ball_responses():
    root = os.path.abspath(os.getcwd())
    with open(
        os.path.join(root, "8ball_responses.json"), "r", encoding="utf-8"
    ) as file:
        eight_ball_responses = file.read()
    return tuple(json.loads(eight_ball_responses)["responses"])  # type: ignore[arg-type]


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

    @slash(guild_ids=(870973430114181141, 1022468050164924497))
    async def start_server(
        self,
        interaction: Interaction,
        server: str = SlashOption(description="The server to start", required=True),
    ):
        """Start a Minecraft server"""
        MINECRAFT_SERVER: Container = DOCKER_CLIENT.containers.get(server)
        if MINECRAFT_SERVER.status != "exited":
            await interaction.response.send_message(
                "Server is already running!", ephemeral=True
            )
            return

        MINECRAFT_SERVER.start()
        embed = nextcord.Embed(color=0x0DD91A, title="Server starting!")
        await interaction.response.send_message(embed=embed)

    @start_server.on_autocomplete("server")
    async def server_autocomplete(self, interaction: Interaction, server: str):
        MC_CONTAINERS: List[Container] = DOCKER_CLIENT.containers.list(
            all=True,
            filters={
                "ancestor": "itzg/minecraft-server",
                "label": "allow_remote_start=true",
            },
        )
        await interaction.response.send_autocomplete(
            [container.name for container in MC_CONTAINERS]
        )


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))

import json
import os
import random
from typing import Literal

import nextcord
import pymongo
from nextcord import Interaction
from nextcord import slash_command as slash
from nextcord.application_command import SlashOption
from nextcord.ext import commands

from main import SLASH_GUILDS, USER_DATA


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

    @slash(guild_ids=SLASH_GUILDS)
    async def headsortails(self, interaction: Interaction):
        """Flip a coin"""
        hot = random.choice(("heads", "tails"))
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    async def f(
        self,
        interaction: Interaction,
        text: str = SlashOption(description="what you respect", required=False),
    ):
        """Press F to pay respect"""
        hearts = ("❤", "💛", "💚", "💙", "💜")
        reason = f"for **{text}** " if text else ""
        await interaction.response.send_message(
            f"**{interaction.user.name}** has paid their respect {reason}{random.choice(hearts)}"
        )

    @slash(guild_ids=SLASH_GUILDS)
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

    @slash(guild_ids=SLASH_GUILDS)
    async def messages(self, interaction: Interaction):
        """Show the amount of messages everyone has sent"""
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
        if embed.fields == 0:
            embed = nextcord.Embed(
                color=0x0DD91A, title="Nobody has sent any messages!"
            )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    async def eightball(
        self,
        interaction: Interaction,
        question=SlashOption(description="Question", required=True),
    ):
        """Ask 8ball a question"""
        embed = nextcord.Embed(color=0x0DD91A, title=question)
        embed.description = random.choice(get_8ball_responses())
        await interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))

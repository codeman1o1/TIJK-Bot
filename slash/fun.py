import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.ext import commands
from nextcord.application_command import SlashOption
import pymongo
import os
import json

from main import SLASH_GUILDS, USER_DATA

root = os.path.abspath(os.getcwd())
eight_ball_responses = open(os.path.join(root, "8ball_responses.json"))
eight_ball_responses = tuple(json.load(eight_ball_responses)["responses"])


class fun_slash(commands.Cog, name="Fun Slash"):
    """Fun slash commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(guild_ids=SLASH_GUILDS)
    async def headsortails(self, interaction: Interaction):
        """Flip a coin"""
        hot = random.randint(0, 1)
        if hot == 0:
            hot = "heads"
        if hot == 1:
            hot = "tails"
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    async def rockpaperscissors(
        self,
        interaction: Interaction,
        choice=SlashOption(
            description="Your choice",
            choices=["rock", "paper", "scissors"],
            required=True,
        ),
    ):
        """Play rock paper scissors"""
        embed = nextcord.Embed(color=0x0DD91A)
        random_number = random.randint(0, 2)
        if random_number == 0:
            random_number = "rock"
        if random_number == 1:
            random_number = "paper"
        if random_number == 2:
            random_number = "scissors"
        if choice == "paper":
            if random_number == "paper":
                win_lose_or_tie = "it is a tie"
            elif random_number == "rock":
                win_lose_or_tie = "you win"
            elif random_number == "scissors":
                win_lose_or_tie = "I win"
        elif choice == "rock":
            if random_number == "paper":
                win_lose_or_tie = "I win"
            elif random_number == "rock":
                win_lose_or_tie = "it is a tie"
            elif random_number == "scissors":
                win_lose_or_tie = "you win"
        elif choice == "scissors":
            if random_number == "paper":
                win_lose_or_tie = "you win"
            elif random_number == "rock":
                win_lose_or_tie = "I win"
            elif random_number == "scissors":
                win_lose_or_tie = "it is a tie"
        embed.add_field(
            name=f"You had {choice} and I had {random_number}",
            value=f"That means that {win_lose_or_tie}!",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @slash(guild_ids=SLASH_GUILDS)
    async def messages(self, interaction: Interaction):
        """Show the amount of messages everone has sent"""
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
        embed.description = random.choice(eight_ball_responses)
        await interaction.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(fun_slash(bot))

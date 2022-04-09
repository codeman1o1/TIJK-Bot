import random
import nextcord
from nextcord import Interaction, slash_command as slash
from nextcord.ext import commands
from nextcord.application_command import SlashOption

from main import SLASH_GUILDS


class fun_slash(commands.Cog, name="Fun Slash", description="Fun slash commands"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash(description="Flips a coin", guild_ids=SLASH_GUILDS)
    async def headsortails(self, interaction: Interaction):
        hot = random.randint(0, 1)
        if hot == 0:
            hot = "heads"
        if hot == 1:
            hot = "tails"
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await interaction.response.send_message(embed=embed)

    @slash(description="Play rock paper scissors", guild_ids=SLASH_GUILDS)
    async def rockpaperscissors(
        self,
        interaction: Interaction,
        choice=SlashOption(
            description="Your choice",
            choices=["rock", "paper", "scissors"],
            required=True,
        ),
    ):
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


def setup(bot: commands.Bot):
    bot.add_cog(fun_slash(bot))

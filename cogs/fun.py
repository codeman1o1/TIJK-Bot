import asyncio
import os
import json
import random
import socket
import struct

import nextcord
import pymongo
from nextcord.ext import commands
from nextcord.ext.commands import Context

from main import USER_DATA

root = os.path.abspath(os.getcwd())
eight_ball_responses = open(os.path.join(root, "8ball_responses.json"))
eight_ball_responses = tuple(json.load(eight_ball_responses)["responses"])


class fun(commands.Cog, name="Fun"):
    """Fun commands that everyone can use"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="headsortails", aliases=["hot", "fac"])
    async def headsortails(self, ctx: Context):
        """Flips a coin"""
        hot = random.randint(0, 1)
        if hot == 0:
            hot = "heads"
        if hot == 1:
            hot = "tails"
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await ctx.send(embed=embed)

    @commands.command(name="rockpaperscissors", aliases=["rps"])
    async def rockpaperscissors(self, ctx: Context, choice: str):
        """Play Rock Paper Scissors"""
        embed = nextcord.Embed(color=0x0DD91A)
        choice = choice.lower()
        if choice == "scissor":
            choice = "scissors"
        rock_paper_scissors_choices = ("rock", "paper", "scissors")
        if choice in rock_paper_scissors_choices:
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
        else:
            embed.add_field(
                name=f"{choice} is not a valid option!",
                value="You can choose between\n> Rock\n> Paper\n> Scissor(s)",
                inline=False,
            )

        await ctx.send(embed=embed)

    @commands.command(name="hack")
    async def hack(self, ctx: Context, user: str):
        """Hack someone (totally real)"""
        msg = await ctx.send(f"`Hacking {user}`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Getting IP-addres...\n10% done`")
        delay = round(random.uniform(2, 5), 2)
        ip = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))
        await asyncio.sleep(delay)
        await msg.edit(content=f"`IP-addres found: {ip}\n20% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Buying data from the dark web...\n30% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Installing trojan on PC...\n40% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Getting into OS...\n50% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Installing 24 virusses on PC...\n60% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Slowly taking RAM...\n70% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Showing personal data to scare you...\n80% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Deleting Windows...\n90% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content="`Deletion complete, Windows was removed...\n100% done`")

        delay = round(random.uniform(1, 2), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`{user} has been totally legitimately hacked.`")

    @commands.command(name="messages", aliases=["msg"])
    async def messages(self, ctx: Context):
        """Shows the amount of messages everyone has sent"""
        embed = nextcord.Embed(color=0x0DD91A)
        for user in USER_DATA.find().sort("messages", pymongo.DESCENDING):
            try:
                user = self.bot.get_user(int(user["_id"]))
                message = user["messages"]
                embed.add_field(
                    name=f"{user} has sent",
                    value=f"{message} messages",
                    inline=False,
                )
            except KeyError:
                pass
        if embed.fields == 0:
            embed = nextcord.Embed(
                color=0x0DD91A, title="Nobody has sent any messages!"
            )
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def eight_ball(self, ctx: Context, question: str):
        """Ask 8ball a question"""
        random_int = random.randint(0, len(eight_ball_responses) - 1)
        embed = nextcord.Embed(color=0x0DD91A, title=eight_ball_responses[random_int])
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))

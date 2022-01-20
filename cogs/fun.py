import asyncio
import os
import random
import socket
import struct

import nextcord
import pymongo
from nextcord.ext import commands

from main import USER_DATA


class fun(
    commands.Cog,
    name="Fun",
    description="Fun commands that everyone can use",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="headsortails",
        description="Flips a coin",
        brief="Flips a coin",
        aliases=["hot","fac"],
    )
    async def headsortails(self, ctx):
        hot = random.randint(0, 1)
        if hot == 0:
            hot = "heads"
        if hot == 1:
            hot = "tails"
        embed = nextcord.Embed(color=0x0DD91A, title=f"It is {hot}!")
        await ctx.send(embed=embed)

    @commands.command(
        name="rockpaperscissors",
        description="Play Rock Paper Scissors",
        brief="Play Rock Paper Scissors",
        aliases=["rps"],
    )
    async def rockpaperscissors(self, ctx, choice):
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

    @commands.command(
        name="hack",
        description="Hack someone (totally real)",
        brief="Hack someone (totally real)",
    )
    async def hack(self, ctx, user):
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

    @commands.command(
        name="messages",
        description="Shows the amount of messages everyone has sent!",
        brief="Shows the amount of messages everyone set",
        aliases=["msg"],
    )
    async def messages(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        for k in USER_DATA.find().sort("messages", pymongo.DESCENDING):
            try:
                user = self.bot.get_user(int(k["_id"]))
                message = k["messages"]
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


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))

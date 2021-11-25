import nextcord
from nextcord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
import random
import asyncio
import os
import socket
import struct

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


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
        aliases=["hot"],
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
        choice = choice.lower()
        if choice == "scissor":
            choice = "scissors"
        rpsChoices = ["rock", "paper", "scissors"]
        if choice.lower() in rpsChoices:
            rps = random.randint(0, 2)
            if rps == 0:
                rps = "rock"
            if rps == 1:
                rps = "paper"
            if rps == 2:
                rps = "scissors"
            if choice == "rock":
                if rps == "rock":
                    wl = "it is a tie"
                if rps == "paper":
                    wl = "I win"
                if rps == "scissors":
                    wl = "you win"
            if choice == "paper":
                if rps == "rock":
                    wl = "you win"
                if rps == "paper":
                    wl = "it is a tie"
                if rps == "scissors":
                    wl = "I win"
            if choice == "scissors":
                if rps == "rock":
                    wl = "I win"
                if rps == "paper":
                    wl = "you win"
                if rps == "scissors":
                    wl = "it is a tie"
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"You had {choice} and I had {rps}",
                value=f"That means that {wl}!",
                inline=False,
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"{choice} is not a valid option!",
                value=f"You can choose between\n> Rock\n> Paper\n> Scissor(s)",
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.command(name="glinko", description="Glinko", brief="Glinko")
    async def glinko(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A, title="Glanko")
        await ctx.send(embed=embed)

    @commands.command(name="glanko", description="Glanko", brief="Glanko")
    async def glanko(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A, title="Glinko")
        await ctx.send(embed=embed)

    @commands.command(
        name="GlinkoGlanko", description="GlinkoGlanko", brief="GlinkoGlanko"
    )
    async def glinkoglanko(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A, title="GlankoGlinko")
        await ctx.send(embed=embed)

    @commands.command(
        name="GlankoGlinko", description="GlankoGlinko", brief="GlankoGlinko"
    )
    async def glankoglinko(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A, title="GlinkoGlanko")
        await ctx.send(embed=embed)

    @commands.command(
        name="hack",
        description="Hack someone (totally real)",
        brief="Hack someone (totally real)",
    )
    async def hack(self, ctx, user: nextcord.Member):
        msg = await ctx.send(f"`Hacking {user.name}#{user.discriminator}...`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Getting IP-addres...\n10% done`")
        delay = round(random.uniform(2, 5), 2)
        ip = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))
        await asyncio.sleep(delay)
        await msg.edit(content=f"`IP-addres found: {ip}\n20% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Buying data from the dark web...\n30% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Installing trojan on PC...\n40% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Getting into OS...\n50% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Installing 24 virusses on PC...\n60% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Slowly taking RAM...\n70% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Showing personal data to scare you...\n80% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(content=f"`Deleting Windows...\n90% done`")
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(
            content=f"`Deletion complete, Windows was removed...\n100% done`"
        )
        delay = round(random.uniform(2, 5), 2)
        await asyncio.sleep(delay)
        await msg.edit(
            content=f"`{user.name}#{user.discriminator} has been totally legitimately hacked.`"
        )

    @commands.command(
        name="messages",
        description="Shows the amount of messages everyone has sent!",
        brief="Shows the amount of messages everyone set",
        aliases=["msg"],
    )
    async def messages(self, ctx, user: nextcord.Member = None):
        async with ctx.typing():
            embed = nextcord.Embed(color=0x0DD91A)
            indexes = UserData.find()
            for k in indexes:
                user = self.bot.get_user(int(k["_id"]))
                if not user is None:
                    messages = k["messages"]
                    embed.add_field(
                        name=f"{user} has sent",
                        value=f"{messages} messages",
                        inline=False,
                    )
                if user is None:
                    UserData.delete_one({"_id": k["_id"]})
        try:
            await ctx.send(embed=embed)
        except:
            embed = nextcord.Embed(
                color=0x0DD91A, title=f"Nobody has sent any messages!"
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))

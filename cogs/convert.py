import nextcord
from nextcord.ext import commands
import os
from PIL import Image


class convert(
    commands.Cog, name="Convert", description="A seperate cog for the convert command"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(
        name="convert",
        description="Convert things",
        brief="Convert things",
        invoke_without_command=True,
        aliases=["cv"],
    )
    async def convert(self, ctx):
        embed = nextcord.Embed(color=0x0DD91A)
        embed.add_field(
            name="Help with the convert command",
            value="Type `.help convert` for all available subcommands",
            inline=False,
        )
        await ctx.send(embed=embed)

    @convert.command(
        name="jpg",
        description="Convert PNG files to JPG images",
        brief="Convert PNG files to JPG images",
        aliases=["jpeg"],
    )
    async def jpg(self, ctx):
        if ctx.message.attachments:
            for file in ctx.message.attachments:
                if file.filename.endswith(".png"):
                    JPG_NAME = file.filename.replace(".png", ".jpg")
                    await file.save(file.filename)
                    image = Image.open(file.filename)
                    image = image.convert("RGB")
                    image.save(JPG_NAME, format="JPEG")
                    image.close()
                    with open(JPG_NAME, "rb") as f:
                        image_jpg = nextcord.File(f)
                        await ctx.reply(file=image_jpg, mention_author=False)
                    os.remove(JPG_NAME)
                    os.remove(file.filename)
                else:
                    embed = nextcord.Embed(
                        color=0xFFC800, title="This file is not a PNG file"
                    )
                    await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="You do not have a file attached to this message!"
            )
            await ctx.send(embed=embed)

    @convert.command(
        name="png",
        description="Convert JPG/JPEG files to PNG images",
        brief="Convert JPG/JPEG files to PNG images",
    )
    async def png(self, ctx):
        if ctx.message.attachments:
            for file in ctx.message.attachments:
                if file.filename.endswith((".jpg", ".jpeg")):
                    if file.filename.endswith(".jpg"):
                        PNG_NAME = file.filename.replace(".jpg", ".png")
                    elif file.filename.endswith(".jpeg"):
                        PNG_NAME = file.filename.replace(".jpeg", ".png")
                    await file.save(file.filename)
                    image = Image.open(file.filename)
                    image = image.convert("RGB")
                    image.save(PNG_NAME, format="PNG")
                    image.close()
                    with open(PNG_NAME, "rb") as f:
                        image_png = nextcord.File(f)
                        await ctx.reply(file=image_png, mention_author=False)
                    os.remove(PNG_NAME)
                    os.remove(file.filename)
                else:
                    embed = nextcord.Embed(
                        color=0xFFC800, title="This file is not a JPG or a JPEG file"
                    )
                    await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0xFFC800, title="You do not have a file attached to this message!"
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(convert(bot))

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.application_command import SlashOption


class developer_slash(
    commands.Cog,
    name="Developer Slash Commands",
    description="Slash commands for developers",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="embed",
        description="Generate an embed",
        guild_ids=[870973430114181141, 865146077236822017],
    )
    async def title(
        self,
        interaction: Interaction,
        title: str = SlashOption(
            name="title", description="The title of the embed", required=False
        ),
        color: int = SlashOption(
            name="color",
            description="The color of the embed",
            choices={"green": 0x0DD91A, "orange": 0xFFC800, "red": 0xFF0000},
            required=False,
        ),
        name1: str = SlashOption(
            name="name1", description="The name of the 1st field", required=False
        ),
        value1: str = SlashOption(
            name="value1", description="The value of the 1st field", required=False
        ),
        name2: str = SlashOption(
            name="name2", description="The name of the 2nd field", required=False
        ),
        value2: str = SlashOption(
            name="value2", description="The value of the 2nd field", required=False
        ),
        name3: str = SlashOption(
            name="name3", description="The name of the 3d field", required=False
        ),
        value3: str = SlashOption(
            name="value3", description="The value of the 3d field", required=False
        ),
    ):
        if self.bot.is_owner(interaction.user):
            try:
                if not color:
                    color = 0x0DD91A
                if title:
                    embed = nextcord.Embed(color=color, title=title)
                else:
                    embed = nextcord.Embed(color=color)
                if name1 and value1:
                    embed.add_field(
                        name=name1,
                        value=value1,
                        inline=False,
                    )
                if name2 and value2:
                    embed.add_field(
                        name=name2,
                        value=value2,
                        inline=False,
                    )
                if name3 and value3:
                    embed.add_field(
                        name=name3,
                        value=value3,
                        inline=False,
                    )
                await interaction.response.send_message(embed=embed)
            except nextcord.errors.HTTPException:
                await interaction.response.send_message(
                    "The embed is invalid", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                "You do not have permission to perform this task", ephemeral=True
            )


def setup(bot):
    bot.add_cog(developer_slash(bot))

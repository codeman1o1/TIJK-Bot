import nextcord
from nextcord.ext import commands
from nextcord.interactions import Interaction
from cogs.event_handler import event_handler


class general_ctx(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.user_command(
        name="Warn user", guild_ids=[870973430114181141, 865146077236822017]
    )
    async def warn(self, interaction: Interaction, user: nextcord.Member):
        await interaction.response.send_message(
            f"Warned {user.display_name}", ephemeral=True
        )
        await event_handler.warn_system(interaction, user)


def setup(bot: commands.Bot):
    bot.add_cog(general_ctx(bot))

import nextcord
from nextcord.ext import commands
from nextcord.interactions import Interaction
from cogs.event_handler import event_handler


class admin_ctx(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.user_command(
        name="Warn user", guild_ids=[870973430114181141, 865146077236822017]
    )
    async def warn(self, interaction: Interaction, user: nextcord.Member):
        owner_role = nextcord.utils.get(interaction.user.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(interaction.user.guild.roles, name="Admin")
        tijk_bot_developer_role = nextcord.utils.get(
            interaction.user.guild.roles, name="TIJK-Bot developer"
        )
        admin_roles = (owner_role, admin_role, tijk_bot_developer_role)
        if any(role in interaction.user.roles for role in admin_roles):
            await interaction.response.send_message(
                f"Warned {user.display_name}", ephemeral=True
            )
            await event_handler.warn_system(
                interaction, user, invoker_username=interaction.user.display_name
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to perform this task", ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(admin_ctx(bot))

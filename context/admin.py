import nextcord
from nextcord.ext import commands
from nextcord.interactions import Interaction

from main import warn_system, full_name


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
            await warn_system(interaction, user, 1, interaction.user.display_name)
        else:
            await interaction.response.send_message(
                "You do not have permission to perform this task", ephemeral=True
            )

    @nextcord.user_command(
        name="Show user information", guild_ids=[870973430114181141, 865146077236822017]
    )
    async def user_info(self, interaction: Interaction, user: nextcord.Member):
        owner_role = nextcord.utils.get(interaction.user.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(interaction.user.guild.roles, name="Admin")
        tijk_bot_developer_role = nextcord.utils.get(
            interaction.user.guild.roles, name="TIJK-Bot developer"
        )
        admin_roles = (owner_role, admin_role, tijk_bot_developer_role)
        if any(role in interaction.user.roles for role in admin_roles):
            if user is not None:
                embed = nextcord.Embed(
                    color=0x0DD91A, title=f"Here is information for {user.name}"
                )
                if user.avatar:
                    embed.set_thumbnail(url=user.avatar)
                embed.add_field(name="Name", value=await full_name(user), inline=True)
                embed.add_field(name="In mutual guilds", value=len(user.mutual_guilds))
            else:
                embed = nextcord.Embed(
                    color=0xFFC800, title="I can not acces that user!"
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "You do not have permission to perform this task", ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(admin_ctx(bot))

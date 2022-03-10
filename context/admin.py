from re import I
import nextcord
from nextcord.ext import commands
from nextcord.interactions import Interaction

from main import warn_system
from main import USER_DATA
from views.profile_picture import profile_picture


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
            await interaction.response.send_message(f"Warned {user}", ephemeral=True)
            await warn_system(interaction, user, 1, interaction.user)
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
                    embed.set_thumbnail(url=user.display_avatar)
                embed.add_field(name="Name", value=user, inline=True)
                if user.nick:
                    embed.add_field(name="Nickname", value=user.nick, inline=True)
                embed.add_field(name="ID", value=user.id, inline=True)
                embed.add_field(
                    name="Account created at",
                    value=user.created_at.strftime("%d %b %Y"),
                    inline=True,
                )
                embed.add_field(
                    name=f"Joined {user.guild.name} at",
                    value=user.joined_at.strftime("%d %b %Y"),
                    inline=True,
                )
                if user.timeout:
                    embed.add_field(name="Timeout", value=user.timeout, inline=True)
                embed.add_field(
                    name="Top role", value=user.top_role.mention, inline=True
                )
                rolesList: list = user.roles
                rolesList.reverse()
                roles = ", ".join(role.mention for role in rolesList)
                embed.add_field(name="Roles", value=roles, inline=True)
                public_flagsList: list = user.public_flags.all()
                if public_flagsList:
                    public_flags = ", ".join(flag.name for flag in public_flagsList)
                    embed.add_field(
                        name="Public flags", value=public_flags, inline=True
                    )
                embed.add_field(
                    name="In mutual guilds", value=len(user.mutual_guilds), inline=True
                )
                messages = USER_DATA.find_one({"_id": user.id})["messages"] or 0
                warns = USER_DATA.find_one({"_id": user.id})["warns"] or 0
                embed.add_field(name="Messages sent", value=messages, inline=True)
                embed.add_field(name="Total warns", value=warns, inline=True)
                if user.guild_permissions:
                    permissions = ", ".join(
                        name for name, value in user.guild_permissions if value
                    )
                    embed.add_field(
                        name="Permissions in guild", value=permissions, inline=True
                    )
                await interaction.response.send_message(
                    embed=embed,
                    view=profile_picture(user.display_avatar.url),
                    ephemeral=True,
                )
            else:
                embed = nextcord.Embed(
                    color=0xFFC800, title="I can not access that user!"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "You do not have permission to perform this task", ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(admin_ctx(bot))

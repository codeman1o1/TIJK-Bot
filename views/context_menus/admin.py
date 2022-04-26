import nextcord
from nextcord.ext import commands
from nextcord.interactions import Interaction
from slash.custom_checks import is_admin, is_mod
from views.buttons.link import Link

from main import SLASH_GUILDS, USER_DATA, warn_system


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.user_command(name="Warn user", guild_ids=SLASH_GUILDS)
    @is_mod()
    async def warn(self, interaction: Interaction, user: nextcord.Member):
        await interaction.response.send_message(f"Warned {user}", ephemeral=True)
        await warn_system(interaction, user, 1, interaction.user)

    @nextcord.user_command(name="Show user information", guild_ids=SLASH_GUILDS)
    @is_admin()
    async def user_info(self, interaction: Interaction, user: nextcord.Member):
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
        if user.communication_disabled_until:
            embed.add_field(
                name="Timed out until",
                value=user.communication_disabled_until.strftime("%H:%M:%S %d %b %Y"),
                inline=True,
            )
        embed.add_field(name="Top role", value=user.top_role.mention, inline=True)
        roles_list: list = user.roles
        roles_list.reverse()
        roles = ", ".join(role.mention for role in roles_list)
        embed.add_field(name="Roles", value=roles, inline=True)
        public_flags_list: list = user.public_flags.all()
        if public_flags_list:
            public_flags = ", ".join(flag.name for flag in public_flags_list)
            embed.add_field(name="Public flags", value=public_flags, inline=True)
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
            embed.add_field(name="Permissions in guild", value=permissions, inline=True)
        await interaction.response.send_message(
            embed=embed,
            view=Link(user.display_avatar.url, "Download profile picture"),
            ephemeral=True,
        )


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))

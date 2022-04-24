from urllib.parse import quote

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.application_checks import *  # noqa: F403
from nextcord.ext.commands import CommandError, CommandNotFound, Context

from main import logger
from slash.custom_checks import CustomCheckError  # noqa: F403
from views.buttons.link import link_button


class error_handler(commands.Cog, name="Error Handler"):
    """A cog for customized error messages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound) and not ctx.message.content.startswith(
            ".."
        ):
            embed = nextcord.Embed(
                color=0xFFC800,
                title="Text based commands are removed from TIJK Bot. Please use slash commands instead",
            )
            embed.set_footer(text="This message will delete itself after 10 seconds")
            await ctx.send(embed=embed, delete_after=10)

    @commands.Cog.listener()
    async def on_application_command_error(
        self, interaction: Interaction, error: CommandError
    ):
        """Called when a slash command error occurs"""
        if isinstance(error, ApplicationMissingAnyRole):
            if error.missing_roles == ["Owner", "Admin", "TIJK-Bot developer"]:
                embed = nextcord.Embed(
                    color=0xFF0000, title="You must be an admin to do this!"
                )

            else:
                missing_roles = ", ".join(error.missing_roles)
                embed = nextcord.Embed(
                    color=0xFF0000,
                    title=f"You are missing any of the following roles: {missing_roles}",
                )

        elif isinstance(error, ApplicationNotOwner):
            OWNER = self.bot.get_user(self.bot.owner_id)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"Only the owner of TIJK Bot ({OWNER}) can do this!",
            )

        elif isinstance(error, ApplicationBotMissingAnyRole):
            MISSING_ROLES = ", ".join(error.missing_roles)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing any of the following role(s): {MISSING_ROLES}",
            )

        elif isinstance(error, ApplicationBotMissingRole):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing the following role: {error.missing_role}",
            )

        elif isinstance(error, ApplicationBotMissingPermissions):
            missing_permissions = ", ".join(error.missing_permissions)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing the following permission(s): {missing_permissions}",
            )

        elif isinstance(error, CustomCheckError):
            embed = nextcord.Embed(color=0xFF0000, title=error.message)

        else:
            embed = nextcord.Embed(color=0xFF0000, title="An unknown error occurred!")
            embed.add_field(
                name="Error:",
                value=error,
                inline=True,
            )
            embed.set_footer(text="Click the button below to report this error")
            await interaction.send(
                embed=embed,
                view=link_button(
                    f"https://github.com/codeman1o1/TIJK-Bot/issues/new?assignees=&labels=bug&template=error.yaml&title=%5BERROR%5D+{quote(str(error))}",
                    "Report error",
                ),
            )
            logger.error(error)
            return

        await interaction.send(embed=embed)
        logger.error(error)


def setup(bot: commands.Bot):
    bot.add_cog(error_handler(bot))

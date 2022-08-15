from urllib.parse import quote

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.application_checks import (
    ApplicationBotMissingAnyRole,
    ApplicationBotMissingPermissions,
    ApplicationBotMissingRole,
    ApplicationMissingAnyRole,
    ApplicationNotOwner,
)

from main import logger
from slash.custom_checks import CustomCheckError
from views.buttons.link import Link


class ErrorHandler(commands.Cog):
    """A cog for customized error messages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(
        self, interaction: Interaction, error: commands.CommandError
    ):
        """Called when a slash command error occurs"""
        embed = nextcord.Embed(color=0xFF0000)

        if isinstance(error, ApplicationMissingAnyRole):
            missing_roles = ", ".join(error.missing_roles)
            embed.title = f"You are missing any of the following roles: {missing_roles}"

        elif isinstance(error, ApplicationNotOwner):
            owner = self.bot.get_user(self.bot.owner_id)
            embed.title = f"Only the owner of TIJK Bot ({owner}) can do this!"

        elif isinstance(error, ApplicationBotMissingAnyRole):
            missing_roles = ", ".join(error.missing_roles)
            embed.title = f"I am missing any of the following role(s): {missing_roles}"

        elif isinstance(error, ApplicationBotMissingRole):
            embed.title = f"I am missing the following role: {error.missing_role}"

        elif isinstance(error, ApplicationBotMissingPermissions):
            missing_permissions = ", ".join(error.missing_permissions)
            embed.title = (
                f"I am missing the following permission(s): {missing_permissions}"
            )

        elif isinstance(error, CustomCheckError):
            embed.title = error.message

        else:
            embed.title = "An unknown error occurred!"
            embed.add_field(
                name="Error:",
                value=error,
                inline=True,
            )
            embed.set_footer(text="Click the button below to report this error")
            await interaction.send(
                embed=embed,
                view=Link(
                    f"https://github.com/codeman1o1/TIJK-Bot/issues/new?assignees=&labels=bug&template=error.yaml&title=%5BERROR%5D+{quote(str(error))}",
                    "Report error on GitHub",
                ),
            )
            logger.error(error)
            return

        await interaction.send(embed=embed)
        logger.error(error)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))

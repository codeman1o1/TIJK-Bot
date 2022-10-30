import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.utils import get

from utils.database import get_bot_data, get_user_data


class ButtonRoles(nextcord.ui.View):
    def __init__(self, bot: commands.Bot = None, guild: nextcord.Guild = None):
        super().__init__(timeout=None)
        if guild:
            for buttonrole in get_bot_data("buttonroles"):
                if get(guild.roles, id=buttonrole):
                    self.add_item(
                        AddButton(
                            label=get(guild.roles, id=buttonrole).name,
                            style=ButtonStyle.primary,
                            custom_id=f"button:buttonroles.{str(buttonrole)}",
                        )
                    )

        if bot:
            for guild2 in bot.guilds:
                for buttonrole in get_bot_data("buttonroles"):
                    if get(guild2.roles, id=buttonrole):
                        self.add_item(
                            AddButton(
                                label=get(guild2.roles, id=buttonrole).name,
                                style=ButtonStyle.primary,
                                custom_id=f"button:buttonroles.{str(buttonrole)}",
                            )
                        )

    @staticmethod
    async def handle_click(
        button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        role_id = int(button.custom_id.replace("button:buttonroles.", "", 1))
        if role := get(
            interaction.guild.roles,
            id=role_id,
        ):
            bans = get_user_data(interaction.user.id, "buttonroles_bans")
            if role_id in bans:
                await interaction.response.send_message(
                    f'You have been banned from using the "{role.name}" button role',
                    ephemeral=True,
                )
                return

            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f'The "{role.name}" role has successfully been added!',
                    ephemeral=True,
                )

            else:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f'The "{role.name}" role has successfully been removed!',
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                f'The "{role.name}" role is not found\nPlease contact an admin to fix this',
                ephemeral=True,
            )


class AddButton(nextcord.ui.Button):
    async def callback(self, interaction: nextcord.Interaction):
        await self.view.handle_click(self, interaction)

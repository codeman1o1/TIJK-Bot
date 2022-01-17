import os

import nextcord
from nextcord import ButtonStyle

from main import BOT_DATA


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for role in BOT_DATA.find()[0]["roles"]:
            self.add_item(
                AddButton(label=role, style=ButtonStyle.primary, custom_id=role)
            )

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        role = nextcord.utils.get(interaction.guild.roles, name=button.label)

        if role not in interaction.user.roles:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f'The "{button.label}" role has successfully been added!',
                    ephemeral=True,
                )
            except AttributeError:
                await interaction.response.send_message(
                    f'The "{button.label}" role is not found\nPlease contact an admin to fix this',
                    ephemeral=True,
                )

        else:
            try:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f'The "{button.label}" role has successfully been removed!',
                    ephemeral=True,
                )
            except AttributeError:
                await interaction.response.send_message(
                    f'The "{button.label}" role is not found\nPlease contact an admin to fix this',
                    ephemeral=True,
                )


class AddButton(nextcord.ui.Button):
    async def callback(self, interaction: nextcord.Interaction):
        await self.view.handle_click(self, interaction)
